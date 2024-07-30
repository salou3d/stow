{ config, pkgs, ... }:

{

  services.wlsunset = {
    enable = true;
    latitude = "35.7808";
    longitude = "-5.8176";
    gamma = "1.0";
    temperature.day = 3901;
    temperature.night = 3900;
  };

  services.swayidle.enable = true;
  services.swayidle = {
      events = [
        { event = "before-sleep"; command = "${pkgs.swaylock}/bin/swaylock  -f"; }
        { event = "after-resume"; command = "${pkgs.wlopm}/bin/wlopm --on \*";}
      ];
      timeouts = [
        { timeout = 500; command = "${pkgs.swaylock}/bin/swaylock -f"; }
        { timeout = 600; command = "${pkgs.wlopm}/bin/wlopm --off \*"; }
      ];
  };

  programs.swaylock = {
      enable = true;
      settings = {
        color = "#31363B";
        ignore-empty-password = true;
        show-keyboard-layout = true;
        indicator-caps-lock = true;
        font-size = 24;
        indicator-idle-visible = false;
        indicator-radius = 100;
        line-color = "ffffff";
        show-failed-attempts = true;
      };
    };

  programs = {
    waybar.enable = true;
    #rofi.enable = true;
    #rofi.theme = "/home/salw/.local/share/rofi/themes/breeze-dark.rasi";
    # wlogout.layout = ;
  };

  programs.wlogout = {
    enable = true;
#     layout = [
#        {
#         label = "lock";
#         action = "swaylock -f";
#         text = "Lock";
#         keybind = "l";
#         circular = true;
#       }
#       {
#         label = "logout";
#         action = "loginctl terminate-user $USER";
#         text = "Log out";
#         keybind = "e";
#         circular = true;
#       }
#       {
#         label = "hibernate";
#         action = "systemctl hibernate";
#         text = "Hibernate";
#         keybind = "h";
#         circular = true;
#       }
#       {
#         label = "suspend";
#         action = "systemctl suspend";
#         text = "Suspend";
#         keybind = "s";
#         circular = true;
#       }
#       {
#         label = "reboot";
#         action = "systemctl reboot";
#         text = "Reboot";
#         keybind = "r";
#         circular = true;
#       }
#       {
#         label = "shutdown";
#         action = "systemctl poweroff";
#         text = "Shutdown";
#         keybind = "q";
#         circular = true;
#       }
#     ];
  };

  home.packages = with pkgs; [
    # mako like == dunst
    wtype wlrctl lswt waylevel
    wlr-randr wlopm wev wl-clipboard slurp grim swaybg
#    keyd
    eww-wayland sfwbar ironbar
    wdisplays
  ];

}
