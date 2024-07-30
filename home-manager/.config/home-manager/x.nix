{ config, pkgs, ... }:

{

  imports = [
    ./picom.nix
   ];

  xsession.enable = true;
  xsession.windowManager.command = "openbox-session";

#   qt = {
#    enable = true;
#    platformTheme = "qtct";
#    style.name = "breeze";
#  };

#   services.redshift = {
#     #enable = true;
#     #tray = true;
#     provider = "manual";
#     latitude = 35.7808;
#     longitude = -5.8176;
#     temperature.night = 3600;
#     temperature.day = 3600;
#   };

  services.xcape = {
      enable = true;
      mapExpression = {
        Super_L = "Control_L|Super_L|R";
      };
  };

  programs = {
    tint2.enable = true;
    feh.enable = true;
    #rofi.enable = true;
    #rofi.theme = "/home/salo/.local/share/rofi/themes/breeze-dark.rasi";

  };

  home.packages = with pkgs; [
    xorg.libX11 xorg.libX11.dev xorg.libxcb  xorg.libXft xorg.libXinerama
    xorg.xinit xorg.xinput xorg.xev
    obconf lxappearance networkmanagerapplet
    wmctrl xkbmon xclip lightlocker xsettingsd scrot
    xdotool jgmenu conky
    gxkb redshift clipit

  ];

  # openbox config
  #home.file."config/openbox" = {
  #  recursive = true;
  #  source = config/openbox;
  #  target = ".config/openbox";
  #};

  # tint2 config
  #home.file."config/tint2" = {
  #  recursive = true;
  #  source = config/tint2;
  #  target = ".config/tint2";
  #};

  # jgmenu config
  #home.file."config/jgmenu" = {
  #  recursive = true;
  #  source = config/jgmenu;
  #  target = ".config/jgmenu";
  #};

}
