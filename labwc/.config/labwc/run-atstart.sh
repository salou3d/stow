#!/usr/bin/env bash

if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
    if [ -z "$XDG_RUNTIME_DIR" ] || ! [ -S "$XDG_RUNTIME_DIR/bus" ] || ! [ -O "$XDG_RUNTIME_DIR/bus" ]; then
        eval "$(dbus-launch --sh-syntax --exit-with-session)" || echo "start session: error executing dbus-launch" >&2
    fi
fi

dbus-update-activation-environment --systemd DISPLAY WAYLAND_DISPLAY > /dev/null 2>&1 &

/usr/libexec/polkit-kde-authentication-agent-1 &

# /usr/libexec/geoclue-2.0/demos/agent &
# /usr/libexec/geoclue-2.0/demos/where-am-i -a 4

#gmenudbusmenuproxy &

if ! pgrep xsettingsd; then
    xsettingsd &
fi

if ! pgrep swayosd-server; then
    swayosd-server &
fi

if systemctl --user is-active dunst.service; then
    systemctl --user stop dunst.service
fi

if ! systemctl --user is-active swaync.service; then
    systemctl --user restart swaync.service
fi

if ! systemctl --user is-active flatpak-session-helper.service; then
    systemctl --user restart flatpak-session-helper.service
fi

if ! systemctl --user is-active dconf.service; then
    systemctl --user restart dconf.service
fi

if ! systemctl --user is-active flatpak-portal.service; then
    systemctl --user restart flatpak-portal.service
fi

if ! pgrep wl-paste; then
    wl-clipboard-history -t &
fi
