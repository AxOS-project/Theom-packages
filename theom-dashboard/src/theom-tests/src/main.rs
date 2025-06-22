// Prevent console window in addition to Slint window in Windows release builds when, e.g., starting the app via file manager. Ignored on other platforms.
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::error::Error;
use std::process::Command;
use whoami;

use winit::{
    event_loop::EventLoop,
};

slint::include_modules!();

fn set_username(ui: &AppWindow) {
    let ui_handle = ui.as_weak();
    if let Some(ui) = ui_handle.upgrade() {
        ui.set_user(whoami::username().into());
    }
}

fn set_theme(ui: &AppWindow) {
    let theme_output = Command::new("theom-config")
        .arg("appearance.theme")
        .output()
        .expect("failed to get theom theme");

    let theme_str = String::from_utf8(theme_output.stdout)
        .expect("stdout was not valid UTF-8")
        .trim()
        .to_string();

    let theme = match theme_str.as_str() {
        "dark" => Theme::Dark,
        "light" => Theme::Light,
        _ => {
            eprintln!("Unknown theme: {}. Defaulting to light.", theme_str);
            Theme::Light
        }
    };

    let theme_mgr = ui.global::<ThemeManager>();
    theme_mgr.set_current_theme(theme);
}

pub fn set_screen_width(ui: &AppWindow) {
    let event_loop = EventLoop::new();

    if let Some(primary_monitor) = event_loop.primary_monitor() {
        let size = primary_monitor.size();
        let width = size.width;

        let ui_handle = ui.as_weak();
        if let Some(ui) = ui_handle.upgrade() {
            ui.set_screen_width(width as f32);
        }
    } else {
        eprintln!("No primary monitor found.");
    }
}

fn get_uptime() -> Option<String> {
    let content = std::fs::read_to_string("/proc/uptime").ok()?;
    let seconds: f64 = content.split_whitespace().next()?.parse().ok()?;

    let hours = (seconds / 3600.0).floor();
    let minutes = ((seconds % 3600.0) / 60.0).floor();

    Some(format!("{:02.0}h {:02.0}m", hours, minutes))
}

fn get_time_string() -> String {
    println!("CALLED");
    let now = chrono::Local::now();
    now.format("%H:%M:%S").to_string()
}


fn main() -> Result<(), Box<dyn Error>> {
    let ui = AppWindow::new()?;

    set_username(&ui);
    set_theme(&ui);
    set_screen_width(&ui);

    ui.on_set_uptime({
        let ui_handle = ui.as_weak();
        move || {
            if let Some(ui) = ui_handle.upgrade() {
                if let Some(uptime_str) = get_uptime() {
                    ui.set_uptime(uptime_str.into());
                } else {
                    ui.set_uptime("Unavailable".into());
                }
            }
        }
    });

    ui.on_get_time(move || get_time_string().into());

    ui.run()?;

    Ok(())
}
