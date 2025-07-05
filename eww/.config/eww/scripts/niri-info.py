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

infos = {}
workspaces = []
windows = []
# keyboard_layouts = {}

for line in file:
    event = json.loads(line)

    if changed := event.get("WorkspacesChanged"):
        workspaces = changed["workspaces"]
    elif activated := event.get("WorkspaceActivated"):
        focused = activated["focused"]
        ws_output = workspaces[activated["id"]]["output"]
        for ws in workspaces:
            got_activated = ws["id"] == activated["id"]
            if ws["output"] == ws_output:
                ws["is_active"] = got_activated
            if focused:
                ws["is_focused"] = got_activated
    elif changed := event.get("WindowsChanged"):
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
    # elif changed := event.get("KeyboardLayoutsChanged"):
    #     keyboard_layouts = changed["keyboard_layouts"]
    # elif switched := event.get("KeyboardLayoutSwitched"):
    #     keyboard_layouts["current_idx"] = switched["idx"]

    infos["workspaces"] = workspaces
    infos["windows"] = windows
    # infos["keyboard_layouts"] = keyboard_layouts
    print(json.dumps(infos))




