#!/bin/bash
case $(wofi -d -L 6 -l 3 -W 100 -x -100 -y 10 \
    -D dynamic_lines=true << EOF | sed 's/^ *//'
    Shutdown
    Reboot
    Log off
    Sleep
    Lock
    Cancel
EOF
) in
    "Shutdown")
        so-confirm-logout-yad.sh shutdown
        ;;
    "Reboot")
        so-confirm-logout-yad.sh reboot
        ;;
    "Sleep")
        so-confirm-logout-yad.sh suspend
        ;;
    "Lock")
        loginctl lock-session
        ;;
    "Log off")
        so-confirm-logout-yad.sh logout
        ;;
esac
