use clap::{Args, Parser, Subcommand, ArgGroup};

#[derive(Parser, Debug)]
#[command(name = "theomctl", version = "1.0", about = "Theom desktop control tool")]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}

#[derive(Subcommand, Debug)]
pub enum Commands {
    /// Manage autostart commands
    #[command(subcommand)]
    Autostart(AutostartCommand),
}

#[derive(Subcommand, Debug)]
pub enum AutostartCommand {
    Add(AutostartAddArgs),
    List,
}

#[derive(Args, Debug)]
#[command(group(
    ArgGroup::new("mode")
        .required(true)
        .args(["once", "always"]),
))]
pub struct AutostartAddArgs {
    /// Command to autostart
    #[arg()]
    pub cmd: String,

    /// Run this command only once on load
    #[arg(long)]
    pub once: bool,

    /// Run this command on every load and reload
    #[arg(long)]
    pub always: bool,
}
