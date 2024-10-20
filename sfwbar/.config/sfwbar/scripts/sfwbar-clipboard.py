#!/usr/bin/env python3

import sqlite3
from os.path import exists, join, expanduser

clipboard = join( expanduser("~"), ".clipboard.sqlite" )
if not exists(clipboard):
    #msg = f"'{clipboard}' does not exist"
    system("wl-clipboard-history")

con = sqlite3.connect(clipboard)
cur = con.cursor()
res = cur.execute("SELECT COUNT(*) FROM ( SELECT contents FROM c GROUP BY contents )")
count = res.fetchone()[0]

print('''PopUp "ClipboardPopup" {
  AutoClose = true
  style = "clip_pop_style"

  grid "ClipboardPopupGrid" {
   style = "clip_pop_grid_style"
   #css = "* { -GtkWidget-direction: bottom; -GtkWidget-max-width: 400px; - }"

   grid "ClipboardHeder" {
     style = "clip_header_style"

     label "count_label" {
       value = "''' + str(count) + ''' Items present"
       css = "* { -GtkWidget-align: 0;  -GtkWidget-hexpand: true; }"
     }
     button "clipitem_clearall" {
       style = "clip_item_button_style"
       value = "edit-delete-shred"
       action[1] = 'sqlite3 ''' + clipboard + ''' "DELETE FROM c"'
       tooltip = "Clear All items in clipboard history"
     }
    }
''')

res = cur.execute("SELECT MAX(id), REPLACE(contents, '', '') FROM c GROUP BY contents ORDER BY id DESC LIMIT 10")
#res = cur.execute("SELECT * FROM c")
items = res.fetchall()


if items:
    for item in items:
        sitem = item[1].replace('"', '\\"').replace("'", "\\'").replace("\\", '\\\\')
        lines = sitem.split("\n")
        if lines and len(lines) > 3:
            sitem = ""
            for line in lines[:3]:
                sitem += line + "\n"
            sitem += "..."
        item_grid = '''    grid {
        style = "clip_item_style"
        label {
            style = "clip_item_label_style"
            value = "''' + sitem.rstrip('\n') + '''"
            action[1] = Exec 'bash -c "wl-clipboard-history -p ''' + str(item[0]) + ''' | wl-copy"'
        }
        button {
            style = "clip_item_button_style"
            value = "edit-delete"
            action[1] = "sqlite3 ''' + clipboard + ''' 'DELETE FROM c WHERE ID = '''+ str(item[0]) + ''''"
            tooltip = "Click to remove the item from clipboard history."
        }
        }
    '''
        print(item_grid)

print("}\n }")
