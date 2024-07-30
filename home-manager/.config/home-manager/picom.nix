{ config, pkgs, ... }:

{

  services.picom = {
    enable = true;
    backend = "glx";
    fade = true;
    fadeSteps = [ 0.023 0.035 ];
    fadeDelta = 10;

    shadow = true;
    shadowOpacity = .30;
    shadowOffsets = [ (-5) (-5) ];
    shadowExclude = [
      "name = 'Notification'"
      "class_g = 'Conky'"
      "class_g ?= 'Notify-osd'"
      "class_g = 'Cairo-clock'"
      "class_g = 'dwm'"
      "class_g = 'firefox'"
      "class_g *?= 'slop'"
      "_GTK_FRAME_EXTENTS@:c"
    ];

    settings = {
      "dithered-present" = false;
      "mark-wmwin-focused" = true;
      "mark-ovredir-focused" = true;
      #"detect-rounded-corners" = false;
      "detect-rounded-corners" = true;
      "detect-client-opacity" = false;
      "use-ewmh-active-win" = true;
      "unredir-if-possible" = false;
      "detect-transient" = true;
      "glx-no-stencil" = true;
      "xrender-sync-fence" = true;
      "window-shader-fg" = "default";
      "transparent-clipping" = false;
      "log-level" = "warn";

      "shadow-radius" = 12;
      "inactive-opacity-override" = true;
      "focus-exclude" = [
        "class_g = 'Cairo-clock'"
      ];
      "animations" = true;
      "animation-stiffness-in-tag" = 125;
      "animation-stiffness-tag-change" = 60.0;
      "animation-window-mass" = 0.4;
      "animation-dampening" = 15;
      "animation-clamping" = true;
      "animation-for-open-window" = "zoom";
      "animation-for-unmap-window" = "squeeze-bottom";
      "animation-for-transient-window" = "slide-up";
      "animation-for-prev-tag" = "minimize";
      "enable-fading-prev-tag" = true;
      "animation-for-next-tag" = "slide-in-center";
      "enable-fading-next-tag" = true;


      "corner-radius" = 10;
      "round-borders" = 10;
      blur = {
        method = "dual_kawase";
        strength = 9;
        background = true;
        background-frame = false;
        background-fixed = false;
      };
      "blur-background-exclude" = [
        "window_type = 'dock'"
        "window_type = 'desktop'"
        "_GTK_FRAME_EXTENTS@:c"
        "class_g = 'FireFox'"
        "class_g = 'Thunderbird'"
        "class_g = 'Discord'"
        "class_g = 'Dunst'"
        "class_g = 'Peek'"
        "class_g *?= 'slop'"
      ];
    };

    wintypes = {
      tooltip = { fade = true; shadow = true; opacity = 0.8; focus = true; "full-shadow" = false; };
      dock = { shadow = false; clip-shadow-above = true; };
      dnd = { shadow = false; };
      "popup_menu" = { opacity = 0.8; };
      "dropdown_menu" = { opacity = 0.8; };
    };

    opacityRules = [
      "100:class_g = 'St' && focused"
      "50:class_g = 'St' && !focused"
      "100:fullscreen"
    ];
  };

}
