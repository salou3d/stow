use std::collections::HashMap;
use std::sync::Arc;
use std::sync::Mutex;

use pinnacle_api::input;
use pinnacle_api::input::Bind;
use pinnacle_api::input::Keysym;
use pinnacle_api::input::XkbConfig;
use pinnacle_api::input::{Mod, MouseButton};
use pinnacle_api::layout;
use pinnacle_api::layout::generators::Corner;
use pinnacle_api::layout::generators::CornerLocation;
use pinnacle_api::layout::generators::Cycle;
use pinnacle_api::layout::generators::Dwindle;
use pinnacle_api::layout::generators::Fair;
use pinnacle_api::layout::generators::MasterSide;
use pinnacle_api::layout::generators::MasterStack;
use pinnacle_api::layout::generators::Spiral;
use pinnacle_api::layout::LayoutGenerator;
use pinnacle_api::layout::LayoutNode;
use pinnacle_api::output;
use pinnacle_api::pinnacle;
use pinnacle_api::pinnacle::Backend;
use pinnacle_api::process::Command;
use pinnacle_api::signal::WindowSignal;
use pinnacle_api::tag;
use pinnacle_api::util::{Axis, Batch};
use pinnacle_api::window;

async fn config() {
    // Change the mod key to `Alt` when running as a nested window.
    let mod_key = match pinnacle::backend() {
        Backend::Tty => Mod::SUPER,
        Backend::Window => Mod::ALT,
    };

    let terminal = "konsole";

    //------------------------
    // Mousebinds            |
    //------------------------

    // `mod_key + left click` starts moving a window
    input::mousebind(mod_key, MouseButton::Left)
        .on_press(|| {
            window::begin_move(MouseButton::Left);
        })
        .group("Mouse")
        .description("Start an interactive window move");

    // `mod_key + right click` starts resizing a window
    input::mousebind(mod_key, MouseButton::Right)
        .on_press(|| {
            window::begin_resize(MouseButton::Right);
        })
        .group("Mouse")
        .description("Start an interactive window resize");

    //------------------------
    // Keybinds              |
    //------------------------

    // `mod_key + s` shows the bindings overlay
    #[cfg(feature = "snowcap")]
    input::keybind(mod_key, 's')
        .on_press(|| {
            pinnacle_api::snowcap::BindOverlay::new().show();
        })
        .group("Compositor")
        .description("Show the bindings overlay");

    // `mod_key + shift + q` quits Pinnacle
    #[cfg(not(feature = "snowcap"))]
    {
        input::keybind(mod_key | Mod::CTRL | Mod::SHIFT, Keysym::Escape)
            .set_as_quit()
            .group("Compositor")
            .description("Quit Pinnacle");
        input::keybind(mod_key, Keysym::Escape)
            .on_press(move || {
                Command::new("wleave").spawn();
            })
            .group("Process")
            .description("Spawn (wleave) the logout menu");
    }
    #[cfg(feature = "snowcap")]
    {
        // `mod_key + shift + q` shows the quit prompt
        input::keybind(mod_key, Keysym::Escape)
            .on_press(|| {
                pinnacle_api::snowcap::QuitPrompt::new().show();
            })
            .group("Compositor")
            .description("Show quit prompt");

        // `mod_key + ctrl + shift + q` for the hard shutdown
        input::keybind(mod_key | Mod::CTRL, Keysym::Escape)
            .on_press(move || {
                Command::new("wleave").spawn();
            })
            .group("Process")
            .description("Spawn (wleave) the logout menu");

        input::keybind(mod_key | Mod::CTRL | Mod::SHIFT, Keysym::Escape)
            .set_as_quit()
            .group("Compositor")
            .description("Quit Pinnacle without prompt");
    }

    // `mod_key + ctrl + r` reloads the config
    input::keybind(mod_key | Mod::CTRL, 'r')
        .set_as_reload_config()
        .group("Compositor")
        .description("Reload the config");

    // `mod_key + shift + c` closes the focused window
    input::keybind(mod_key, 'q')
        .on_press(|| {
            if let Some(window) = window::get_focused() {
                window.close();
            }
        })
        .group("Window")
        .description("Close the focused window");

    // `mod_key + Return` spawns the default terminal
    input::keybind(mod_key, Keysym::BackSpace)
        .on_press(move || {
            Command::new(terminal).spawn();
        })
        .group("Process")
        .description("Spawn a terminal");

    // `mod_key SHIFT + Return` spawns the kitty terminal
    input::keybind(mod_key | Mod::SHIFT, Keysym::BackSpace)
        .on_press(move || {
            Command::new("kitty").spawn();
        })
        .group("Process")
        .description("Spawn a kitty terminal");

    // `mod_key + Return` spawns Albert Launcher
    input::keybind(mod_key, Keysym::Return)
        .on_press(move || {
            Command::new("albert").args(["toggle"]).spawn();
            // Command::new(["albert", "toggle"]).spawn();
        })
        .group("Process")
        .description("Spawn an alfred launcher");

    // `mod_key SHIFT + Return` spawns rofi
    input::keybind(mod_key | Mod::SHIFT, Keysym::Return)
        .on_press(move || {
            Command::new("rofi").args(["-show", "drun", "-show-icons"]).spawn();
        })
        .group("Process")
        .description("Spawn Rofi");

    // `mod_key CTRL + Return` spawns walker
    input::keybind(mod_key | Mod::CTRL, Keysym::Return)
        .on_press(move || {
            Command::new("walker").spawn();
        })
        .group("Process")
        .description("Spawn walker launcher");

    // `mod_key ALT + Return` spawns rofi
    input::keybind(mod_key | Mod::ALT, Keysym::Return)
        .on_press(move || {
            Command::with_shell(["bash", "-c"], "cliphist list | rofi -dmenu | cliphist decode | wl-copy").spawn();
        })
        .group("Process")
        .description("Spawn clipboard history using cliphist/rofi");

    // `mod_key + l` spawns hyprlock
    input::keybind(mod_key, 'l')
    .on_press(move || {
        Command::new("hyprlock").spawn();
    })
    .group("Process")
    .description("Lock screen with hyprlock");

    // `mod_key CTRL + i` kills swayidle
    input::keybind(mod_key | Mod::CTRL, 'i')
    .on_press(move || {
        Command::with_shell(["bash", "-c"], "pidof swayidle && pkill swayidle").spawn();
    })
    .group("Process")
    .description("Kill (swayidle) to deactivate idle-ing");

    // `mod_key SHIFT + i` restart swayidle
    input::keybind(mod_key | Mod::SHIFT, 'i')
    .on_press(move || {
        Command::with_shell(["bash", "-c"], "pidof swayidle || swayidle").spawn();
    })
    .group("Process")
    .description("Restart (swayidle) idle-ing");

    // SCREEN SHOTS AND RECORDING
    input::keybind(mod_key, 'o')
        .on_press(move || {
            Command::new("screen-rec.sh").args(["-o"]).spawn();
        })
        .group("Process")
        .description("Restart (swayidle) idle-ing");

    input::keybind(mod_key | Mod::CTRL, 'o')
        .on_press(move || {
            Command::new("screen-rec.sh").args(["-g"]).spawn();
        })
        .group("Process")
        .description("Restart (swayidle) idle-ing");

    // Shots
    input::keybind(Mod::empty(), Keysym::Print)
        .on_press(move || {
            Command::with_shell(["bash", "-c"], "wayshot -f $(xdg-user-dir PICTURES)/$(date +%m-%d-%Y_%H-%M-%S).png").spawn();
        })
        .group("Process")
        .description("Take a Screenshot of the current output/screen");

    input::keybind(mod_key | Mod::CTRL, Keysym::Print)
        .on_press(move || {
            Command::with_shell(["bash", "-c"], "wayshot -s \"$(slurp)\" -f $(xdg-user-dir PICTURES)/$(date +%m-%d-%Y_%H-%M-%S).png").spawn();
        })
        .group("Process")
        .description("Take a Screenshot of a region in the current output/screen");


    // MEDIA KEYS
    input::keybind(Mod::empty(), Keysym::XF86_AudioRaiseVolume)
        .on_press(move || {
            Command::new("swayosd-client").args(["--output-volume", "raise"]).spawn();
        })
        .group("Process")
        .description("Raise output Volume");

    input::keybind(Mod::empty(), Keysym::XF86_AudioLowerVolume)
        .on_press(move || {
            Command::new("swayosd-client").args(["--output-volume", "lower"]).spawn();
        })
        .group("Process")
        .description("Lower output Volume");

    input::keybind(Mod::empty(), Keysym::XF86_AudioMute)
        .on_press(move || {
            Command::new("swayosd-client").args(["--output-volume", "mute-toggle"]).spawn();
        })
        .group("Process")
        .description("Mute Audio Output");

    input::keybind(Mod::empty(), Keysym::XF86_AudioMicMute)
        .on_press(move || {
            Command::new("swayosd-client").args(["--input-volume", "mute-toggle"]).spawn();
        })
        .group("Process")
        .description("Mute Mic");

    input::keybind(Mod::empty(), Keysym::XF86_MonBrightnessUp)
        .on_press(move || {
            Command::new("swayosd-client").args(["--brightness", "raise"]).spawn();
        })
        .group("Process")
        .description("Raise output Volume");

    input::keybind(Mod::empty(), Keysym::XF86_MonBrightnessDown)
        .on_press(move || {
            Command::new("swayosd-client").args(["--brightness", "lower"]).spawn();
        })
        .group("Process")
        .description("Lower output Volume");

    input::keybind(Mod::empty(), Keysym::XF86_AudioPlay)
        .on_press(move || {
            Command::new("playerctl").args(["play-pause"]).spawn();
        })
        .group("Process")
        .description("Media Player play-pause");

    input::keybind(Mod::empty(), Keysym::XF86_AudioNext)
        .on_press(move || {
            Command::new("playerctl").args(["next"]).spawn();
        })
        .group("Process")
        .description("Media Player next track/song");

    input::keybind(Mod::empty(), Keysym::XF86_AudioPrev)
        .on_press(move || {
            Command::new("playerctl").args(["previous"]).spawn();
        })
        .group("Process")
        .description("Media Player previous track/song");

    // `mod_key + ctrl + space` toggles floating
    input::keybind(mod_key | Mod::CTRL, Keysym::space)
        .on_press(|| {
            if let Some(window) = window::get_focused() {
                window.toggle_floating();
                window.raise();
            }
        })
        .group("Window")
        .description("Toggle floating on the focused window");

    // `mod_key + f` toggles fullscreen
    input::keybind(mod_key, 'f')
        .on_press(|| {
            if let Some(window) = window::get_focused() {
                window.toggle_fullscreen();
                window.raise();
            }
        })
        .group("Window")
        .description("Toggle fullscreen on the focused window");

    // `mod_key + m` toggles maximized
    input::keybind(mod_key, 'm')
        .on_press(|| {
            if let Some(window) = window::get_focused() {
                window.toggle_maximized();
                window.raise();
            }
        })
        .group("Window")
        .description("Toggle maximized on the focused window");

    //------------------------
    // Layouts               |
    //------------------------

    // Pinnacle supports a tree-based layout system built on layout nodes.
    //
    // To determine the tree used to layout windows, Pinnacle requests your config for a tree data structure
    // with nodes containing gaps, directions, etc. There are a few provided utilities for creating
    // a layout, known as layout generators.
    //
    // ### Layout generators ###
    // A layout generator is a table that holds some state as well as
    // the `layout` function, which takes in a window count and computes
    // a tree of layout nodes that determines how windows are laid out.
    //
    // There are currently six built-in layout generators, one of which delegates to other
    // generators as shown below.

    fn into_box<'a, T: LayoutGenerator + Send + 'a>(
        generator: T,
    ) -> Box<dyn LayoutGenerator + Send + 'a> {
        Box::new(generator) as _
    }

    // Create a cycling layout generator that can cycle between layouts on different tags.
    let cycler = Arc::new(Mutex::new(Cycle::new([
        into_box(MasterStack::default()),
        into_box(MasterStack {
            master_side: MasterSide::Right,
            ..Default::default()
        }),
        into_box(MasterStack {
            master_side: MasterSide::Top,
            ..Default::default()
        }),
        into_box(MasterStack {
            master_side: MasterSide::Bottom,
            ..Default::default()
        }),
        into_box(Dwindle::default()),
        into_box(Spiral::default()),
        into_box(Corner::default()),
        into_box(Corner {
            corner_loc: CornerLocation::TopRight,
            ..Default::default()
        }),
        into_box(Corner {
            corner_loc: CornerLocation::BottomLeft,
            ..Default::default()
        }),
        into_box(Corner {
            corner_loc: CornerLocation::BottomRight,
            ..Default::default()
        }),
        into_box(Fair::default()),
        into_box(Fair {
            axis: Axis::Horizontal,
            ..Default::default()
        }),
    ])));

    // Use the cycling layout generator to manage layout requests.
    // This returns a layout requester that allows you to request layouts manually.
    let layout_requester = layout::manage({
        let cycler = cycler.clone();
        move |args| {
            let Some(tag) = args.tags.first() else {
                return LayoutNode::new();
            };
            let mut generator = cycler.lock().unwrap();
            generator.set_current_tag(tag.clone());
            generator.layout(args.window_count)
        }
    });

    // `mod_key + space` cycles to the next layout
    input::keybind(mod_key, Keysym::space)
        .on_press({
            let cycler = cycler.clone();
            let requester = layout_requester.clone();
            move || {
                let Some(focused_op) = output::get_focused() else {
                    return;
                };
                let Some(first_active_tag) = focused_op
                    .tags()
                    .batch_find(|tag| Box::pin(tag.active_async()), |active| *active)
                else {
                    return;
                };

                cycler
                    .lock()
                    .unwrap()
                    .cycle_layout_forward(&first_active_tag);
                requester.request_layout_on_output(&focused_op);
            }
        })
        .group("Layout")
        .description("Cycle the layout forward");

    // `mod_key + shift + space` cycles to the previous layout
    input::keybind(mod_key | Mod::SHIFT, Keysym::space)
        .on_press(move || {
            let Some(focused_op) = output::get_focused() else {
                return;
            };
            let Some(first_active_tag) = focused_op
                .tags()
                .batch_find(|tag| Box::pin(tag.active_async()), |active| *active)
            else {
                return;
            };

            cycler
                .lock()
                .unwrap()
                .cycle_layout_backward(&first_active_tag);
            layout_requester.request_layout_on_output(&focused_op);
        })
        .group("Layout")
        .description("Cycle the layout backward");

    //------------------------
    // Tags                  |
    //------------------------

    let tag_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"];
    let names = HashMap::from([
        ( "1", Keysym::F1),
        ( "2", Keysym::F2),
        ( "3", Keysym::F3),
        ( "4", Keysym::F4),
        ( "5", Keysym::F5),
        ( "6", Keysym::F6),
        ( "7", Keysym::F7),
        ( "8", Keysym::F8),
        ( "9", Keysym::F9),
        ("10", Keysym::F10),
    ]);

    // Setup all monitors with tags "1" through "9"
    output::for_each_output(move |output| {
        let mut tags = tag::add(output, tag_names);
        tags.next().unwrap().set_active(true);
    });

    // for tag_name in tag_names {
    for (tag_name, tag_key) in names {
        // `mod_key + 1-9` switches to tag "1" to "9"
        input::keybind(mod_key | Mod::SHIFT, tag_key)
            .on_press(move || {
                if let Some(tag) = tag::get(tag_name) {
                    tag.switch_to();
                }
            })
            .group("Tag")
            .description(format!("Switch to tag {tag_name}"));

        // `mod_key + ctrl + 1-9` toggles tag "1" to "9"
        input::keybind(mod_key | Mod::CTRL, tag_key)
            .on_press(move || {
                if let Some(tag) = tag::get(tag_name) {
                    tag.toggle_active();
                }
            })
            .group("Tag")
            .description(format!("Toggle tag {tag_name}"));

        // `mod_key + shift + 1-9` moves the focused window to tag "1" to "9"
        input::keybind(mod_key | Mod::ALT, tag_key)
            .on_press(move || {
                if let Some(tag) = tag::get(tag_name) {
                    if let Some(win) = window::get_focused() {
                        win.move_to_tag(&tag);
                    }
                }
            })
            .group("Tag")
            .description(format!("Move the focused window to tag {tag_name}"));

        // `mod_key + ctrl + shift + 1-9` toggles tag "1" to "9" on the focused window
        input::keybind(mod_key | Mod::CTRL | Mod::SHIFT, tag_key)
            .on_press(move || {
                if let Some(tg) = tag::get(tag_name) {
                    if let Some(win) = window::get_focused() {
                        win.toggle_tag(&tg);
                    }
                }
            })
            .group("Tag")
            .description(format!("Toggle tag {tag_name} on the focused window"));
    }

    input::libinput::for_each_device(|device| {
        // Enable natural scroll for touchpads
        if device.device_type().is_touchpad() {
            device.set_natural_scroll(false);
            device.set_tap(true);
        }
    });

    input::set_xkb_config(
        XkbConfig::new()
            .with_layout("fr,ara")
            .with_variant("azerty")
            .with_options("grp:alt_space_toggle"),
    );

    // There are no server-side decorations yet, so request all clients use client-side decorations.
    window::add_window_rule(|window| {
        window.set_decoration_mode(window::DecorationMode::ClientSide);
    });

    // Enable sloppy focus
    window::connect_signal(WindowSignal::PointerEnter(Box::new(|win| {
        win.set_focused(true);
    })));

    #[cfg(feature = "snowcap")]
    if let Some(error) = pinnacle_api::pinnacle::take_last_error() {
        // Show previous crash messages
        pinnacle_api::snowcap::ConfigCrashedMessage::new().show(error);
    } else {
        // Or show the bind overlay on startup
        pinnacle_api::snowcap::BindOverlay::new().show();
    }

    // Command::new(terminal).once().spawn();
    Command::new("at-start.sh").once().spawn();
    Command::new("waybar").once().spawn();
}

pinnacle_api::main!(config);
