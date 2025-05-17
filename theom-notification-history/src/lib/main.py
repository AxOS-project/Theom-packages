import os
import json
import gzip
import uuid
import subprocess
import argparse
import time

NOTIFICATIONS_DIR = './notifications'

def clean_old_notifications(days=1):
    now = time.time()
    cutoff = now - days * 86400  # 86400 seconds in a day

    for fname in os.listdir(NOTIFICATIONS_DIR):
        if fname.endswith('.json.gz'):
            fpath = os.path.join(NOTIFICATIONS_DIR, fname)
            if os.path.isfile(fpath):
                if os.path.getmtime(fpath) < cutoff:
                    os.remove(fpath)
                    print(f"Removed old notification: {fname}")

def parse_image_data_struct(proc):
    data = {}
    while True:
        line = next(proc).strip()
        if line == '}':
            break
        if line.startswith('int32'):
            val = int(line.split()[1])
            if 'width' not in data:
                data['width'] = val
            elif 'height' not in data:
                data['height'] = val
            elif 'rowstride' not in data:
                data['rowstride'] = val
            elif 'bits_per_sample' not in data:
                data['bits_per_sample'] = val
            elif 'channels' not in data:
                data['channels'] = val
        elif line.startswith('boolean'):
            val = line.split()[1].lower() == 'true'
            data['has_alpha'] = val
        elif line.startswith('array of bytes ['):
            bytes_list = []
            while True:
                line = next(proc).strip()
                if line == ']':
                    break
                bytes_list.extend(int(b, 16) for b in line.split())
            data['data'] = bytes_list
    return data

def list_notifications():
    all_data = {}
    if not os.path.exists(NOTIFICATIONS_DIR):
        print(f"No notifications directory found at {NOTIFICATIONS_DIR}")
        return

    for fname in os.listdir(NOTIFICATIONS_DIR):
        if fname.endswith('.json.gz'):
            fpath = os.path.join(NOTIFICATIONS_DIR, fname)
            try:
                with gzip.open(fpath, 'rt', encoding='utf-8') as f:
                    data = json.load(f)
                all_data[fname] = data
            except Exception as e:
                print(f"Failed to load {fname}: {e}")
    print(json.dumps(all_data, indent=2))

def delete_notification(filename):
    fpath = os.path.join(NOTIFICATIONS_DIR, filename)
    if os.path.exists(fpath):
        os.remove(fpath)
        print(f"Deleted {filename}")
    else:
        print(f"File {filename} does not exist in {NOTIFICATIONS_DIR}")

def monitor_notifications():
    os.makedirs(NOTIFICATIONS_DIR, exist_ok=True)

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
                continue

            elif line.startswith('array ['):
                array_items = []
                while True:
                    line = next(proc.stdout).strip()
                    if line == ']':
                        break
                    if line.startswith('string'):
                        val = line.split('"', 1)[1].rsplit('"', 1)[0]
                        array_items.append(val)
                    elif line.startswith('dict entry('):
                        key = None
                        value = None

                        line = next(proc.stdout).strip()
                        if line.startswith('string'):
                            key = line.split('"', 1)[1].rsplit('"', 1)[0]

                        line = next(proc.stdout).strip()
                        if line.startswith('variant'):
                            variant_content = line[len('variant'):].strip()
                            if variant_content.startswith('int64'):
                                value = int(variant_content.split()[1])
                            elif variant_content.startswith('string'):
                                value = variant_content.split('"', 1)[1].rsplit('"', 1)[0]
                            elif variant_content.startswith('byte'):
                                value = int(variant_content.split()[1])
                            elif variant_content.startswith('struct {'):
                                value = parse_image_data_struct(proc.stdout)
                            else:
                                value = variant_content
                        else:
                            value = line

                        array_items.append({key: value})

                        while True:
                            try:
                                line = next(proc.stdout).strip()
                                if line == ')':
                                    break
                            except StopIteration:
                                break
                arrays.append(array_items)
                continue

            if len(fields) >= 4:
                result = {
                    "process_name": fields[0],
                    "icon_path": fields[1],
                    "heading": fields[2],
                    "subheading": fields[3],
                    "arrays": arrays
                }
                print(result)

                json_data = json.dumps(result, indent=2)
                filename = f"{uuid.uuid4().hex}.json.gz"
                filepath = os.path.join(NOTIFICATIONS_DIR, filename)
                with gzip.open(filepath, 'wt', encoding='utf-8') as f:
                    f.write(json_data)
                print(f"Saved compressed notification to {filepath}")

                state = 'idle'

def main():
    os.makedirs('./notifications', exist_ok=True)
    clean_old_notifications()
    parser = argparse.ArgumentParser(description="Notification manager")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--list', action='store_true', help="List all stored notifications")
    group.add_argument('--delete', metavar='FILENAME', help="Delete a specific notification file")

    args = parser.parse_args()

    if args.list:
        list_notifications()
    elif args.delete:
        delete_notification(args.delete)
    else:
        monitor_notifications()

if __name__ == "__main__":
    main()
