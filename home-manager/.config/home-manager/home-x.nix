{ config, pkgs, ... }:

{

  imports = [
    ./x.nix
   ];

  # Home Manager needs a bit of information about you and the paths it should
  # manage.
  home.username = "salo";
  home.homeDirectory = "/home/salo";

  # You can also manage environment variables but you will have to manually
  # source
  #
  #  ~/.nix-profile/etc/profile.d/hm-session-vars.sh
  #
  # or
  #
  #  /etc/profiles/per-user/sal/etc/profile.d/hm-session-vars.sh
  #
  # if you don't want to manage your shell through Home Manager.
  home.sessionVariables = {
    # EDITOR = "emacs";
  };

  home.keyboard = null;

#   home.file."local/bin" = {
#     recursive = true;
#     source = local/bin;
#     target = ".local/bin";
#   };

# end of home.nix
}
