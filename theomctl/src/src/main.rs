mod args;
mod functions;

use args::{Cli, Commands, AutostartCommand};
use clap::Parser;

fn main() {
    let cli = Cli::parse();

    use functions::{list_autostarts, register_autostarts};

    match cli.command {
        Commands::Autostart(subcmd) => match subcmd {
            AutostartCommand::Add(args) => {
                let res = if args.once {
                    register_autostarts::register_once(&args.cmd)
                } else {
                    register_autostarts::register_always(&args.cmd)
                };
                match res {
                    Ok(_) => println!("Successfully registered command '{}'", args.cmd),
                    Err(e) => eprintln!("Error registering command: {}", e),
                }
            }
            AutostartCommand::List => {
                if let Err(e) = list_autostarts::list_autostarts() {
                    eprintln!("Error listing autostarts: {}", e);
                }
            }
        },
    }
}
