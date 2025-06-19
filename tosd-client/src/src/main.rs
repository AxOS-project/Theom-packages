use clap::{Arg, Command};
use zbus::Connection;
use std::error::Error;
// use clap::ArgAction;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let matches = Command::new(env!("CARGO_PKG_NAME"))
    .version(env!("CARGO_PKG_VERSION"))
        .about("tosd CLI client to call D-Bus server")
        .arg(Arg::new("text")
            .required(true)
            .help("Text label or 'clear'"))
        .arg(Arg::new("mode")
            .required(false)
            .value_parser(["slider", "text"])
            .help("Display mode"))
        .arg(Arg::new("value")
            .required(false)
            .help("Value for slider or text")
            .value_parser(clap::value_parser!(i32)))
        .arg(Arg::new("duration")
            .short('d')
            .long("duration")
            .default_value("2.0")
            .help("Duration"))
        .arg(Arg::new("size")
            .short('s')
            .long("size")
            .default_value("1.0")
            .help("Size"))
        .arg(Arg::new("position")
            .short('p')
            .long("position")
            .default_value("T")
            .help("Position (TL, T, TR, L, C, R, BL, B, BR)"))
        .arg(Arg::new("margin_x")
            .required(false)
            .long("margin-x")
            .default_value("20")
            .help("X margin of the window")
            .value_parser(clap::value_parser!(i32)))
        .arg(Arg::new("margin_y")
            .required(false)
            .long("margin-y")
            .default_value("20")
            .help("Y margin of the window")
            .value_parser(clap::value_parser!(i32)))
        .arg(Arg::new("dont_reuse_window")
            .short('x')
            .long("dont-reuse-window")
            .action(clap::ArgAction::SetTrue)
            .help("Dont reuse the existing window."))
        .arg(Arg::new("background_color")
            .long("background-color")
            .default_value("#23262d"))
        .arg(Arg::new("text_color")
            .long("text-color")
            .default_value("#ffffff"))
        .arg(Arg::new("slider_fill_color")
            .long("slider-fill-color")
            .default_value("#61afef"))
        .arg(Arg::new("slider_knob_color")
            .long("slider-knob-color")
            .default_value("#528bff"))
        .get_matches();

    let text = matches.get_one::<String>("text").unwrap();
    let mode = matches.get_one::<String>("mode").map(|s| s.as_str());
    let value = matches.get_one::<i32>("value").copied();
    let duration = matches.get_one::<String>("duration").unwrap().parse::<f64>()?;
    let size = matches.get_one::<String>("size").unwrap().parse::<f64>()?;
    let position = matches.get_one::<String>("position").unwrap();
    let margin_x = matches.get_one::<i32>("margin_x").copied().unwrap();
    let margin_y = matches.get_one::<i32>("margin_y").copied().unwrap();
    let dont_reuse_window = matches.get_flag("dont_reuse_window");
    let background_color = matches.get_one::<String>("background_color").unwrap();
    let text_color = matches.get_one::<String>("text_color").unwrap();
    let slider_fill_color = matches.get_one::<String>("slider_fill_color").unwrap();
    let slider_knob_color = matches.get_one::<String>("slider_knob_color").unwrap();

    let connection = Connection::session().await?;

    let proxy = zbus::Proxy::new(
        &connection,
        "org.theom.tosd",
        "/org/theom/tosd",
        "org.theom.tosd",
    ).await?;
    

    if text == "clear" {
        proxy.call_method("ClearAll", &()).await?;
        println!("Cleared OSD.");
        return Ok(());
    }

    let args = (
        text.as_str(),
        mode.unwrap_or("text"),
        value.unwrap_or(0),
        duration,
        size,
        position.as_str(),
        margin_x,
        margin_y,
        dont_reuse_window,
        background_color.as_str(),
        text_color.as_str(),
        slider_fill_color.as_str(),
        slider_knob_color.as_str(),
    );

    proxy.call_method("ShowOSD", &args).await?;

    Ok(())
}
