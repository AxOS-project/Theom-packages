import subprocess

proc = subprocess.Popen(
    ['dbus-monitor', "interface='org.freedesktop.Notifications',member='Notify'"],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,
    text=True
)

print("Listening for notifications...\n")

state = 'idle'
fields = []
arrays = []

for line in proc.stdout:
    line = line.strip()

    if "member=Notify" in line:
        state = 'collect'
        fields = []
        arrays = []
        continue

    if state == 'collect':
        if line.startswith('string'):
            value = line.split('"', 1)[1].rsplit('"', 1)[0]
            fields.append(value)
            # Only print after processing arrays
            continue

        elif line.startswith('array ['):
            array_items = []
            while True:
                line = next(proc.stdout).strip()
                if line == ']':
                    break
                if line.startswith('string'):
                    value = line.split('"', 1)[1].rsplit('"', 1)[0]
                    array_items.append(value)
            arrays.append(array_items)
            continue

        # Optional: stop collection if you want here after arrays processed
        # For demonstration, let's print when we have 4 strings and any arrays
        if len(fields) >= 4:
            result = {
                "process_name": fields[0],
                "icon_path": fields[1],
                "heading": fields[2],
                "subheading": fields[3],
                "arrays": arrays
            }
            print(result)
            state = 'idle'
