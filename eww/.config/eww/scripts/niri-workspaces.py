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

workspaces = []

for line in file:
    event = json.loads(line)

    if changed := event.get("WorkspacesChanged"):
        workspaces = sorted(changed["workspaces"], key=lambda ws: ws["idx"])
    elif activated := event.get("WorkspaceActivated"):
        focused = activated["focused"]
        ws_output = None
        for ws in workspaces:
            got_activated = ws["id"] == activated["id"]
            # if ws["output"] == ws_output:
            ws["is_active"] = got_activated
            if focused:
                ws["is_focused"] = got_activated
    else:
        continue

    print(json.dumps(workspaces))




