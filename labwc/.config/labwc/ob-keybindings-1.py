#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
from os import system
import xml.etree.ElementTree as et
from os.path import exists, join, expanduser, isfile, isabs
from xdg import IconTheme, BaseDirectory

_name      = "sobmenu"
# rcfile = join(expanduser("~"), ".config/openbox/rc.xml")
rcfile = join(expanduser("~"), ".config/labwc/rc.xml")
cache      = BaseDirectory.save_cache_path(_name)
icon_cache = BaseDirectory.save_cache_path(_name + "/icons")

def get_system_theme():
    gtkrc = join(expanduser("~"), ".config/gtk-3.0/settings.ini")
    theme = ""
    with open(gtkrc, "r") as fin:
        for line in fin:
            if line.startswith("gtk-icon-theme-name"):
                theme = line.strip().split("=")[1].replace('\"', '')
    return theme.lower()

#
def convert_cache_icon(icon, icon_path):

    system("rsvg-convert --output=" + icon + " " + icon_path)

    if exists(icon):
        return icon
    else:
        return "None"

#
def get_app_icon(icon_name):

    icontheme = get_system_theme()

    cached_icon = join( icon_cache, icon_name + ".png" )
    if exists( cached_icon ):
        return cached_icon

    icon_path = IconTheme.getIconPath( icon_name, theme=icontheme, size=24 )

    if icon_path and icon_path.endswith( ".svg" ):
        icon_path = convert_cache_icon( cached_icon, icon_path )
    elif icon_path and ( icon_path.endswith( ".png" ) or icon_path.endswith( ".xpm" )):
        return icon_path
    else:
        return "None"
#

def get_keybindings(rcfilepath):

    rctree = et.parse(rcfile)
    rcroot = rctree.getroot()
    pmroot = et.Element("openbox_pipe_menu")

    keys_counter = 1

    keybinds = rcroot.findall("{*}keyboard/{*}keybind")

    desks_menu = et.SubElement(pmroot, "menu",{
        "id": "desks-menu",
        "label": "Switching Desktops"
            })

    desktop_icon = get_app_icon("desktop")
    if desktop_icon:
        desks_menu.set('icon', desktop_icon)

    wins_menu =  et.SubElement(pmroot, "menu", {
        "id": "wins-menu",
        "label": "Switching Windows"
            })

    win_icon = get_app_icon("window")
    if win_icon:
        wins_menu.set('icon', win_icon)

    menus_menu =  et.SubElement(pmroot, "menu", {
        "id": "menus-menu",
        "label": "Menus"
            })

    menu_icon = get_app_icon("show-menu")
    if menu_icon:
        menus_menu.set('icon', menu_icon)

    cmds_menu =  et.SubElement(pmroot, "menu", {
        "id": "cmds-menu",
        "label": "Runnings Applications and Commands"
            })

    run_icon = get_app_icon("system-run")
    if run_icon:
        cmds_menu.set('icon', run_icon)

    for keybind in keybinds:
        item = et.Element("item",{
            'id': str(keys_counter)
            })

        label = keybind.get('key') + ": "

        actions = keybind.findall("{*}action")

        for action in actions:
            label += action.get('name') + " "

            ac_children = action.findall("*")
            if not ac_children:
                continue
            for child in ac_children:
                #child_tag = child.tag.split("}")[1]
                child_tag = ""
                child_spl = child.tag.split("}")
                if len(child_spl) > 1:
                    child_tag = child_spl[1]
                else:
                    child_tag = child.tag

                if child_tag == "to":
                    label += child.text + " "
                    item.set('label', label)
                    if desktop_icon:
                        item.set('icon', desktop_icon)
                    desks_menu.append(item)
                elif child_tag == "command":
                    label += "'" + child.text + "' "
                    item.set('label', label)
                    if run_icon:
                        item.set('icon', run_icon)
                    cmds_menu.append(item)
                elif child_tag == "menu":
                    label += child.text + " "
                    item.set('label', label)
                    if menu_icon:
                        item.set('icon', menu_icon)
                    menus_menu.append(item)
                elif child_tag == "finalactions":
                    finalactions = child.findall("*")
                    for finalaction in finalactions:
                        label += finalaction.get("name") + " "
                    item.set('label', label)
                    if win_icon:
                        item.set('icon', win_icon)
                    wins_menu.append(item)
                elif child_tag == "direction":
                    label += child.text + " "
                    item.set('label', label)
                    if win_icon:
                        item.set('icon', win_icon)
                    wins_menu.append(item)

        if not ac_children:
            item.set('label', label)
            if run_icon:
                item.set('icon', run_icon)
            cmds_menu.append(item)
        keys_counter += 1

    et.dump(pmroot)


if __name__ == "__main__":
    get_keybindings(rcfile)
