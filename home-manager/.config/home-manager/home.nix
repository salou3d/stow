{ config, pkgs, ... }:

{

  imports = [
    #./home-x.nix
    #./x.nix
    ./wl.nix
   ];

  home.stateVersion = "23.11";

  # Let Home Manager install and manage itself.
  programs.home-manager.enable = true;

  xdg.enable = true;
  xdg.userDirs.enable = true;
  xdg.userDirs.createDirectories = true;

}
