#!/usr/bin/env python3

import json
import os
import sys
from socket import AF_UNIX, SHUT_WR, socket

niri_socket = socket(AF_UNIX)
niri_socket.connect(os.environ["NIRI_SOCKET"])
file = niri_socket.makefile("rw")

file.write('"EventStream"')
file.flush()
niri_socket.shutdown(SHUT_WR)

output = None
if len(sys.argv) > 1:
    output = sys.argv[1]

windows = []

for line in file:
    event = json.loads(line)

    if changed := event.get("WindowsChanged"):
        windows = changed["windows"]
    elif activated := event.get("WorkspaceActiveWindowChanged"):
        for w in windows:
            if w["id"] == activated["active_window_id"]:
                w["is_focused"] = True
            else:
                w["is_focused"] = False

    elif activated := event.get("WindowOpenedOrChanged"):
        for w in windows:
            flag = False
            if w["id"] == activated["window"]["id"]:
                w["is_focused"] = True
                flag = True
            else:
                w["is_focused"] = False

            if not flag:
                windows.append( activated["window"] )
    elif activated := event.get("WindowFocusChanged"):
        pass

    print(json.dumps(windows))




