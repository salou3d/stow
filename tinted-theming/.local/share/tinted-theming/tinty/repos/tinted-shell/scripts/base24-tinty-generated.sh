#!/usr/bin/env sh
# tinted-shell (https://github.com/tinted-theming/tinted-shell)
# Scheme name: Tinty Generated 
# Scheme author: Tinty
# Template author: Tinted Theming (https://github.com/tinted-theming)
export BASE24_THEME="tinty-generated"

color00="0d/27/32" # Base 00 - Black
color01="e5/17/3e" # Base 08 - Red
color02="1e/bc/89" # Base 0B - Green
color03="ed/b4/7d" # Base 0A - Yellow
color04="17/38/c3" # Base 0D - Blue
color05="86/2c/60" # Base 0E - Magenta
color06="14/ec/d4" # Base 0C - Cyan
color07="ae/ad/a3" # Base 06 - White
color08="42/53/57" # Base 02 - Bright Black
color09="d0/b4/99" # Base 12 - Bright Red
color10="4b/b4/a9" # Base 14 - Bright Green
color11="46/93/7a" # Base 13 - Bright Yellow
color12="6f/42/5c" # Base 16 - Bright Blue
color13="90/49/56" # Base 17 - Bright Magenta
color14="42/53/97" # Base 15 - Bright Cyan
color15="c9/c4/b6" # Base 07 - Bright White
color16="d9/90/70" # Base 09
color17="b6/24/40" # Base 0F
color18="27/3d/44" # Base 01
color19="42/53/57" # Base 02
color20="78/80/7d" # Base 04
color21="ae/ad/a3" # Base 06
color_foreground="93/97/90" # Base 05
color_background="0d/27/32" # Base 00

if [ -n "$TMUX" ] || [ "${TERM%%[-.]*}" = "tmux" ]; then
  # Tell tmux to pass the escape sequences through
  # (Source: http://permalink.gmane.org/gmane.comp.terminal-emulators.tmux.user/1324)
  put_template() { printf '\033Ptmux;\033\033]4;%d;rgb:%s\033\033\\\033\\' "$@"; }
  put_template_var() { printf '\033Ptmux;\033\033]%d;rgb:%s\033\033\\\033\\' "$@"; }
  put_template_custom() { printf '\033Ptmux;\033\033]%s%s\033\033\\\033\\' "$@"; }
elif [ "${TERM%%[-.]*}" = "screen" ]; then
  # GNU screen (screen, screen-256color, screen-256color-bce)
  put_template() { printf '\033P\033]4;%d;rgb:%s\007\033\\' "$@"; }
  put_template_var() { printf '\033P\033]%d;rgb:%s\007\033\\' "$@"; }
  put_template_custom() { printf '\033P\033]%s%s\007\033\\' "$@"; }
elif [ "${TERM%%-*}" = "linux" ]; then
  put_template() { [ "$1" -lt 16 ] && printf "\e]P%x%s" "$1" "$(echo "$2" | sed 's/\///g')"; }
  put_template_var() { true; }
  put_template_custom() { true; }
else
  put_template() { printf '\033]4;%d;rgb:%s\033\\' "$@"; }
  put_template_var() { printf '\033]%d;rgb:%s\033\\' "$@"; }
  put_template_custom() { printf '\033]%s%s\033\\' "$@"; }
fi

# 16 color space
put_template 0  "$color00"
put_template 1  "$color01"
put_template 2  "$color02"
put_template 3  "$color03"
put_template 4  "$color04"
put_template 5  "$color05"
put_template 6  "$color06"
put_template 7  "$color07"
put_template 8  "$color08"
put_template 9  "$color09"
put_template 10 "$color10"
put_template 11 "$color11"
put_template 12 "$color12"
put_template 13 "$color13"
put_template 14 "$color14"
put_template 15 "$color15"

# foreground / background / cursor color
if [ -n "$ITERM_SESSION_ID" ]; then
  # iTerm2 proprietary escape codes
  put_template_custom Pg 939790 # foreground
  put_template_custom Ph 0d2732 # background
  put_template_custom Pi 939790 # bold color
  put_template_custom Pj 425357 # selection color
  put_template_custom Pk 939790 # selected text color
  put_template_custom Pl 939790 # cursor
  put_template_custom Pm 0d2732 # cursor text
else
  put_template_var 10 "$color_foreground"
  if [ "$BASE24_SHELL_SET_BACKGROUND" != false ]; then
    put_template_var 11 "$color_background"
    if [ "${TERM%%-*}" = "rxvt" ]; then
      put_template_var 708 "$color_background" # internal border (rxvt)
    fi
  fi
  put_template_custom 12 ";7" # cursor (reverse video)
fi

# clean up
unset put_template
unset put_template_var
unset put_template_custom
unset color00
unset color01
unset color02
unset color03
unset color04
unset color05
unset color06
unset color07
unset color08
unset color09
unset color10
unset color11
unset color12
unset color13
unset color14
unset color16
unset color17
unset color18
unset color19
unset color20
unset color21
unset color15
unset color_foreground
unset color_background

# Optionally export variables
if [ -n "$TINTED_SHELL_ENABLE_BASE24_VARS" ]; then
  export BASE24_COLOR_00_HEX="0d2732"
  export BASE24_COLOR_01_HEX="273d44"
  export BASE24_COLOR_02_HEX="425357"
  export BASE24_COLOR_03_HEX="5d6a6a"
  export BASE24_COLOR_04_HEX="78807d"
  export BASE24_COLOR_05_HEX="939790"
  export BASE24_COLOR_06_HEX="aeada3"
  export BASE24_COLOR_07_HEX="c9c4b6"
  export BASE24_COLOR_08_HEX="e5173e"
  export BASE24_COLOR_09_HEX="d99070"
  export BASE24_COLOR_0A_HEX="edb47d"
  export BASE24_COLOR_0B_HEX="1ebc89"
  export BASE24_COLOR_0C_HEX="14ecd4"
  export BASE24_COLOR_0D_HEX="1738c3"
  export BASE24_COLOR_0E_HEX="862c60"
  export BASE24_COLOR_0F_HEX="b62440"
  export BASE24_COLOR_10_HEX="b04b5e"
  export BASE24_COLOR_11_HEX="be9a8a"
  export BASE24_COLOR_12_HEX="d0b499"
  export BASE24_COLOR_13_HEX="46937a"
  export BASE24_COLOR_14_HEX="4bb4a9"
  export BASE24_COLOR_15_HEX="425397"
  export BASE24_COLOR_16_HEX="6f425c"
  export BASE24_COLOR_17_HEX="904956"
fi
