#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Openbox right menu genetator inspired from 'obamenu'

from os.path import exists, join, expanduser, isfile, isdir, islink, isabs, dirname, abspath, realpath
from os import system, environ
import xml.etree.ElementTree as ET
from glob import glob
from xdg import BaseDirectory, DesktopEntry, IconTheme
import concurrent.futures as cf
import time, argparse, sys

_name      = "sobmenu"
cache      = BaseDirectory.save_cache_path(_name)
icon_cache = BaseDirectory.save_cache_path(_name + "/icons" )
data_dir   = join( BaseDirectory.xdg_config_home, "openbox" )

MAIN_CATS  = ('AudioVideo', 'Development', 'Education', 'Game', 'Graphics', 'Network', 'Office', 'Settings', 'System', 'Utility', 'Other')

ALIASES    = {"AudioVideo" : "Multimedia", "Utility": "Utilities", "Game": "Games"}

TERMINAL   = "konsole" # change this to your favorite terminal
FILE_MANAGER = "dolphin"

# ----------------------------------------------------------------------
#
class Category(object):
    def __init__(self):
        self.name = ""
        self.icon = ""
        self.apps = []

    def set_name(self, name):
        self.name = name

    def set_icon(self, icon):
        self.icon = icon

    def set_apps(self, apps):
        self.apps = apps

class AppDe(DesktopEntry.DesktopEntry):

    def __init__(self, de_name):
        super(AppDe, self).__init__(de_name)
        self.icon = ""
        self.fname = ""

    def get_icon(self):
        return self.icon

    def set_icon(self, icon):
        self.icon = icon

#
def get_terminal():
    return TERMINAL if TERMINAL else environ["TERM"]

def get_system_theme():
    gtkrc = join(expanduser("~"), ".config/gtk-3.0/settings.ini")
    #gtkrc = join(expanduser("~"), ".gtkrc-2.0")
    theme = ""
    if not exists(gtkrc):
        gtkrc = join(expanduser("~"), ".gtkrc-2.0")
        if not exists(gtkrc):
            return "hicolor"
    with open(gtkrc, "r") as fin:
        for line in fin:
            if line.startswith("gtk-icon-theme-name"):
                theme = line.strip().split("=")[1].replace('\"', '').strip()
    return theme.lower()

#
def convert_cache_icon(icon, icon_path):

    system("rsvg-convert --output=" + icon + " " + icon_path)

    if exists(icon):
        return icon
    else:
        return ""

#
def get_icon( icon, theme ):

    cached_icon = join( icon_cache, icon + ".png" )
    if exists( cached_icon ):
        return cached_icon

    icon_path = IconTheme.getIconPath( icon, theme=theme, size=24 )

    if icon_path and icon_path.endswith( ".svg" ):
        return convert_cache_icon( cached_icon, icon_path )
    elif icon_path and ( icon_path.endswith( ".png" ) or icon_path.endswith( ".xpm" )):
        return icon_path
    else:
        return ""

#
def process_apps(desk_entry, uicons):

    if desk_entry.getHidden() or desk_entry.getNoDisplay():
        return

    item = ET.Element("item", {
        "label": desk_entry.getName(),
        "icon" : desk_entry.get_icon() if uicons else ""
        })

    itemaction = ET.SubElement(item, 'action', {
        'name': 'Execute'
            })

    command = ET.SubElement(itemaction, 'command')
    text = desk_entry.getExec().replace("%U", "")

    if desk_entry.getTerminal():
        command.text = get_terminal() + " -e " + text
    else:
        command.text = text

    return item

#
def build_apps_menu(categories, entries, theme, pipe, uicons):

    icon = get_icon( "homerun", theme ) if uicons else ""
    if pipe:
        app_menu = ET.Element("openbox_pipe_menu")
    else:
        app_menu = ET.Element('menu', attrib={
            "id": "apps-menu",
            "label": "Applications",
            "icon" : icon
            })

    menu_dict = {}

    for cat in sorted( categories.keys() ):

        menu_dict[cat] = ET.SubElement(app_menu, "menu", {
            "id" : "openbox-" + cat,
            "label" : cat,
            "icon" : categories[cat].icon
            })

        with cf.ThreadPoolExecutor() as executor:
            results = executor.map(process_apps,
                                   [ entries[i] for i in categories[cat].apps ],
                                   [ uicons for _ in categories[cat].apps ]
                                   )

            for result in results:
                if result:
                    menu_dict[cat].append(result)

    return app_menu

#
def build_ob_menu(wmanager, theme, uicons):

    icon = get_icon("openbox", theme) if uicons else ""
    wm = ""
    if wmanager:
        wm = wmanager.capitalize()
    else:
        wm = "WM"

    ob_menu = ET.Element('menu', attrib={
        "id"   : "openbox-pref-menu",
        "label": wm,
        "icon" : icon
        })

    if wmanager == "openbox":
        icon = get_icon("obconf", theme)  if uicons else ""
        item = ET.SubElement(ob_menu, "item", attrib={
            "label" : "Openbox Configuration Manager",
            "icon" : icon
            })
        action = ET.SubElement(item, 'action', attrib={ "name": "Execute" })
        command = ET.SubElement(action, "command")
        command.text = "obconf"

        sun = ET.SubElement(action, "startupnotify")
        sun_enable = ET.SubElement(sun, "enabled")
        sun_enable.text = "yes"

    icon = get_icon("configure", theme)  if uicons else ""
    act_ob_menu = ET.SubElement(ob_menu, "menu", attrib={
        "id": "ob-commands",
        "label": "{} commands".format( wm ),
        "icon" : icon
        })

    recf_item = ET.SubElement(act_ob_menu, "item", attrib={
        "label": "Reconfigure " + wm
        })

    recf_exec = ET.SubElement(recf_item, "action", attrib={ "name": "Reconfigure" })

    rest_item = ET.SubElement(act_ob_menu, "item", attrib={
        "label": "Restart " + wm
        })

    rest_exec = ET.SubElement(rest_item, "action", attrib={ "name": "Restart" })

    icon = get_icon( "keyboard", theme ) if uicons else ""
    keys_menu = ET.SubElement(ob_menu, "menu", attrib={
        "id": "ob-keybinds-menu",
        "label": wm + " Keybindings",
        "icon": icon,
        "execute": join( data_dir, "ob-keybindings-1.py" )
        })

    return ob_menu

#
def build_session_menu(theme, uicons):

    icon = get_icon("system-log-out", theme)  if uicons else ""

    power_menu = ET.Element('menu', attrib={
        "id"   : "session-menu",
        "label": "Session",
        "icon" : icon
        })

    session_actions = {
        "Logout": ["log-out", "Execute"],
        "Hibernate" : ["hibernate", "Execute"],
        "Suspend" : ["suspend-hibernate", "Execute"],
        "Reboot" : ["reboot", "Execute"],
        "Shutdown": ["shutdown", "Execute"],
        "Lock": ["system-lock-screen", "Execute"]}

    for act in session_actions:

        icon = get_icon("system-" + session_actions[act][0] , theme )  if uicons else ""

        item = ET.SubElement(power_menu, "item", {
            "label": act,
            "icon" : icon
            })

        action = ET.SubElement(item, "action", {
            "name": session_actions[act][1]
            })

        text = ""
        command = ET.SubElement(action, "command")
        text = "so-confirm-logout-yad.sh " + act.lower()
        command.text = text


    return power_menu

#
def build_favs( theme, uicons ):

    icon = get_icon( "system-run", theme )  if uicons else ""
    item = ET.Element('item', attrib={
        "id": "rofi-run",
        "label": "Run command",
        "icon": icon
        })
    action = ET.SubElement(item, "action", attrib={ "name": "Execute" })
    command = ET.SubElement(action, "command")
    command.text = "rofi -show run"

    icon = get_icon( "system-file-manager", theme )  if uicons else ""
    item1 = ET.Element('item', attrib={
        "id": "fav-file-manager",
        "label": "File Manager",
        "icon": icon
        })
    action1 = ET.SubElement(item1, "action", attrib={ "name": "Execute" })
    command1 = ET.SubElement(action1, "command")
    command1.text = FILE_MANAGER

    icon = get_icon( "utilities-terminal", theme )  if uicons else ""
    item2 = ET.Element('item', attrib={
        "id": "fav-terminal",
        "label": "Terminal",
        "icon": icon
        })
    action2 = ET.SubElement(item2, "action", attrib={ "name": "Execute" })
    command2 = ET.SubElement(action2, "command")
    command2.text = get_terminal()

    icon = get_icon( "internet-web-browser" , theme )  if uicons else ""
    item3 = ET.Element('item', attrib={
        "id": "fav-browser",
        "label": "Web Browser",
        "icon": icon
        })
    action3 = ET.SubElement(item3, "action", attrib={ "name": "Execute" })
    command3 = ET.SubElement(action3, "command")
    command3.text = "xdg-open http:///"

    return item, item1, item2, item3

#
def build_root_menu( categories, applications, wmanager, theme, pipe, uicons ):

    pipe_str = 'openbox_pipe_menu'

    if not pipe:
        pipe_str = 'menu'

    pipe_menu = ET.Element(pipe_str, attrib={
         'xmlns': "http://openbox.org/",
         'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
         'xsi:schemaLocation': "http://openbox.org/",
         })

    sep = ET.SubElement(pipe_menu, "separator", attrib={ "label": "Openbox 3 Menu" })

    for item in build_favs( theme, uicons ):
        pipe_menu.append(item)

    sep = ET.SubElement(pipe_menu, "separator")

    pipe_menu.append( build_apps_menu( categories, applications, theme, not pipe, uicons ) )

    pipe_menu.append( build_ob_menu( wmanager, theme, uicons ) )

    sep = ET.SubElement(pipe_menu, "separator")
    pipe_menu.append( build_session_menu( theme, uicons ) )
    sep = ET.SubElement(pipe_menu, "separator")

    return pipe_menu

#
def build_menu_file( categories, applications, wmanager, theme, pipe, uicons ):

    xmenu = ET.Element('openbox_menu', attrib={
        'xmlns': 'http://openbox.org/',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:schemaLocation': 'http://openbox.org/'
        })

    execute_str = join( data_dir, realpath( sys.argv[0] ) )
    execute_str += ' -i' if uicons else ''

    if pipe:
        menup = ET.SubElement( xmenu, 'menu', attrib={
            'id': 'root-menu',
            'label': 'Openbox 3',
            'execute': execute_str + ' -p'
            })
    else:

        rootmenu = ET.SubElement( xmenu, 'menu', attrib={
            'id': 'root-menu',
            'label': 'Openbox 3'
            })

        sep = ET.SubElement(rootmenu, "separator", attrib={ "label": "Openbox 3 Menu" })

        for fav in build_favs( theme, uicons ):
            rootmenu.append( fav )

        sep = ET.SubElement(rootmenu, "separator")

        if wmanager == "openbox":
            appsmenu = ET.SubElement( rootmenu, 'menu', attrib={
                'id': 'apps-menu',
                'label': 'Applications',
                'icon': get_icon( "homerun", theme ) if uicons else "" ,
                'execute': execute_str + ' -s'
                })
        else:
            appsmenu = ET.SubElement( rootmenu, 'menu', attrib={
                'id': 'apps-menu',
                'label': 'Applications',
                'icon': get_icon( "homerun", theme ) if uicons else "" ,
                })
            appsmenu.append( build_apps_menu( categories, applications, theme, not pipe, uicons ) )

        rootmenu.append( build_ob_menu( wmanager, theme, uicons ) )

        sep = ET.SubElement(rootmenu, "separator")

        rootmenu.append( build_session_menu( theme, uicons ) )

        sep = ET.SubElement( rootmenu, "separator" )

    return xmenu

#
def update_menu_file( menufile, menu ):

    et = ET.ElementTree(menu)
    ET.indent(et)

    et.write( menufile, encoding="UTF-8", xml_declaration=True )

#
def cache_menu(catsdict, appsdict, cachefile):

    # caching category as: # CategoryName;CategoryIcon,ApplicationsList
    # caching apps as: DesktopFilePath;ApplicationName;Comment;Exec;Terminal;Type;Icon;IconName;display

    with open(cachefile, "w") as fout:
        for cat in catsdict:
            c = ""
            for a in catsdict[cat].apps:
                c += a + ":"
            line = "# {};{};{}\n".format(cat, catsdict[cat].icon, c)
            fout.write(line)
        for app in appsdict:
            line = "{};{};{};{};{};{};{};{};{};".format(appsdict[app].getFileName(), appsdict[app].getName(), appsdict[app].getComment(), appsdict[app].getExec(), appsdict[app].getTerminal(), appsdict[app].getType(), appsdict[app].get_icon(), appsdict[app].getIcon(), appsdict[app].getNoDisplay())
            for cat in appsdict[app].getCategories():
                line += cat + ":"
            line += "\n"
            fout.write(line)

#
def read_cached_menu(cachefile, theme, uicons):
    categories = {}
    apps = {}
    with open(cachefile, "r") as fin:
        for line in fin:
            if line.startswith("#"):
                cat = Category()
                attrs = line.replace("# ", "").strip().split(";")
                appslist = attrs[-1][0:-1].split(":")
                cat.name, cat.apps = attrs[0], appslist
                cat.icon = attrs[1] if uicons else ""
                categories[cat.name] = cat

            else:
                # caching apps as: DesktopFilePath;ApplicationName;Comment;Exec;Terminal;Type;Icon;IconName;display
                attrs = line.strip().split(";")
                cats = attrs[-1][0:-1].split(":")
                app = AppDe(None)
                app.content['Desktop Entry'] = {}

                app.fname = attrs[0]
                app.set("Name", attrs[1])
                app.set("Comment", attrs[2])
                app.set("Exec", attrs[3])
                app.set("Terminal", attrs[4])
                app.set("Type", attrs[5])
                if uicons:
                    if attrs[6]:
                        app.set_icon(attrs[6])
                    else:
                        app.set_icon( get_icon( attrs[7], theme ))
                else:
                    app.set_icon("")
                app.set("Icon", attrs[7])
                app.set("Display", attrs[8])
                app.set("Categories", cats)

                apps[app.getName()] = app

    return categories, apps

#
def prepare_dicts(uicons):

    desktop_entries = {}
    theme = get_system_theme()
    categories = {}
    for cat in MAIN_CATS:
        categories[cat] = []

    for ddir in BaseDirectory.xdg_data_dirs:
        ad = join(ddir, "applications")
        if exists(ad):
            desk_files = glob(ad + "/*.desktop")
            if desk_files:
                for df in desk_files:
                    desk_entry = AppDe(df)
                    if not desk_entry.getNoDisplay() and desk_entry.getName():
                        desktop_entries[desk_entry.getName()] = desk_entry
                        if not desk_entry.getCategories():
                            categories["Other"].append(desk_entry.getName())
                        else:
                            i = 0
                            for c in desk_entry.getCategories():
                                if c in MAIN_CATS:
                                    i += 1
                                    categories[c].append(desk_entry.getName())
                            if i == 0:
                                categories["Other"].append(desk_entry.getName())

    cats = {}
    for cat in categories:
        if categories[cat]:
            cn = cat
            if cat in ALIASES:
                cn = ALIASES[cat]
            c = Category()
            c.set_name(cn)
            c.set_apps(categories[cat])
            cats[cn] = c

    if uicons:
        with cf.ThreadPoolExecutor() as tpe:
            cicons = { i: tpe.submit(get_icon,
                                    "applications-" + i.lower(),
                                    theme
                                    ) for i in cats
            }

            aicons = { i: tpe.submit(get_icon,
                                    desktop_entries[i].getIcon(),
                                    theme
                                    ) for i in desktop_entries
                    }

            for c in cicons:
                cats[c].set_icon( cicons[c].result() )

            for a in aicons:
                desktop_entries[a].set_icon( aicons[a].result() )

    return cats, desktop_entries, theme

#
def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--icons", action="store_true", help="Include icons")
    parser.add_argument("-w", "--winowmanager", metavar='str', type=str, help="For which window manager to make the menu, 'openbox' or 'labwc'")

    parser.add_argument("-m", "--menu", action="store_true", help="Make a new menu.xml")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--pipe", action="store_true", help="Generate a dynamic menu (pipe)\nThe whole menu will be generated each time")
    group.add_argument("-s", "--static", action="store_true", help="Generate a static menu\nOnly Applications will be generated each time")

    soargs = parser.parse_args()

    wmanager = soargs.winowmanager
    useicons = soargs.icons
    pipe = soargs.pipe

    if not pipe and not soargs.static:
        return

    cats_dict, apps_dict, theme = {}, {}, ""
    sobmenu_cache = join( cache, "sobmenu-cache.txt" )

    if soargs.menu:

        if wmanager:
            if wmanager in [ 'openbox', 'labwc' ]:
                data_dir = join( BaseDirectory.xdg_config_home, wmanager )

            else:
                print(f"not a recognized window manager: '{wmanager}'.")
                print("Possible ones are: openbox or labwc")
                exit(0)
        else:
            print(f"No window manager where given with the option -m.")
            print("Possible ones are: -w openbox or -w labwc")
            exit(0)

        theme = get_system_theme()
        cats_dict, apps_dict, theme = prepare_dicts( useicons )
        cache_menu(cats_dict, apps_dict, sobmenu_cache)
        menu = build_menu_file( cats_dict, apps_dict, wmanager, theme, pipe, useicons )
        update_menu_file( join( data_dir, "menu.xml" ), menu )
        system( f"{wmanager} --reconfigure" )
        return

    if exists(sobmenu_cache):
        cats_dict, apps_dict = read_cached_menu( sobmenu_cache, theme, useicons )
    else:
        cats_dict, apps_dict, theme = prepare_dicts( useicons )
        cache_menu(cats_dict, apps_dict, sobmenu_cache)

    if not soargs.menu:
        if pipe:
            ET.dump( build_root_menu( cats_dict, apps_dict, wmanager, theme, pipe, useicons ))
        elif not pipe and soargs.static:
            ET.dump( build_apps_menu( cats_dict, apps_dict, theme, not pipe, useicons ) )

if __name__ == "__main__":
    main()
