use std::fs::{self, OpenOptions};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::env::var;

fn get_config_dir() -> PathBuf {
    if let Ok(xdg) = var("XDG_CONFIG_HOME") {
        PathBuf::from(xdg).join(".theom-autostarts")
    } else {
        dirs::home_dir()
            .expect("Could not find home directory")
            .join(".config/.theom-autostarts")
    }
}

fn append_command_to_file(file_path: &Path, cmd: &str) -> std::io::Result<()> {
    if let Some(parent) = file_path.parent() {
        fs::create_dir_all(parent)?;
    }
    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(file_path)?;

    writeln!(file, "{}", cmd)?;
    Ok(())
}

pub fn register_once(cmd: &str) -> std::io::Result<()> {
    let file_path = get_config_dir().join("exec_once.sh");
    append_command_to_file(&file_path, cmd)
}

pub fn register_always(cmd: &str) -> std::io::Result<()> {
    let file_path = get_config_dir().join("exec_always.sh");
    append_command_to_file(&file_path, cmd)
}
