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
active_window = {"title": "..."}

for line in file:
    event = json.loads(line)

    if changed := event.get("WindowsChanged"):
        windows = changed["windows"]
        for w in windows:
            if w["is_focused"]:
                active_window["title"] = w["title"]
                # active_window = w["title"]
                break
    elif activated := event.get("WorkspaceActiveWindowChanged"):
        for w in windows:
            if w["id"] == activated["active_window_id"]:
                w["is_focused"] = True
                active_window["title"] = w["title"]
                # active_window = w["title"]
            else:
                w["is_focused"] = False

    elif activated := event.get("WindowOpenedOrChanged"):
        flag = False
        for w in windows:
            if w["id"] == activated["window"]["id"]:
                w["is_focused"] = True
                flag = True
            else:
                w["is_focused"] = False

        if not flag:
            windows.append( activated["window"] )

        active_window["title"] = activated["window"]["title"]
        # active_window = activated["window"]["title"]
    elif changed := event.get("WindowFocusChanged"):
        for w in windows:
            if w["id"] == changed["id"]:
                active_window["title"] = w["title"]
                # active_window = w["title"]
                break

    print(json.dumps(active_window))
    # print(active_window)




