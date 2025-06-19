use std::fs;
use std::path::PathBuf;
use std::env::var;

fn get_config_dir() -> PathBuf {
    if let Ok(xdg) = var("XDG_CONFIG_HOME") {
        PathBuf::from(xdg).join("theom-autostarts")
    } else {
        dirs::home_dir()
            .expect("Could not find home directory")
            .join(".config/theom-autostarts")
    }
}

fn read_commands_from_file(path: PathBuf) -> std::io::Result<Vec<String>> {
    if path.exists() {
        let content = fs::read_to_string(path)?;
        // Split lines, trim, filter out empty lines
        let cmds = content
            .lines()
            .map(str::trim)
            .filter(|line| !line.is_empty())
            .map(String::from)
            .collect();
        Ok(cmds)
    } else {
        Ok(Vec::new())
    }
}

pub fn list_autostarts() -> std::io::Result<()> {
    let config = get_config_dir();

    let once_file = config.join("exec_once.sh");
    let always_file = config.join("exec_always.sh");

    println!("Autostart commands (once):");
    let once_cmds = read_commands_from_file(once_file)?;
    if once_cmds.is_empty() {
        println!("  (none)");
    } else {
        for cmd in once_cmds {
            println!("  {}", cmd);
        }
    }

    println!("\nAutostart commands (always):");
    let always_cmds = read_commands_from_file(always_file)?;
    if always_cmds.is_empty() {
        println!("  (none)");
    } else {
        for cmd in always_cmds {
            println!("  {}", cmd);
        }
    }

    Ok(())
}
