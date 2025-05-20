import subprocess


def current_theme():
    try:
        theme_output = subprocess.check_output(["theom-config", "theme"], text=True).strip().lower()
        return (theme_output)
    except Exception as e:
        print(f"Error detecting theme: {e}")
        return ("dark")