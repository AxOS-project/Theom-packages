import subprocess
def parse_image_data_struct(proc):
    data = {}
    while True:
        line = next(proc).strip()
        if line == '}':
            break
        if line.startswith('int32'):
            val = int(line.split()[1])
            # Assign fields in order (width, height, rowstride, bits_per_sample, channels)
            # We will parse in order, so track order with a list
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
                # Each line contains bytes like "00 00 00 ..."
                bytes_list.extend(int(b, 16) for b in line.split())
            data['data'] = bytes_list
    return data


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
            # Distinguish first array (list of strings) and second array (dict entries)
            array_items = []
            while True:
                line = next(proc.stdout).strip()
                if line == ']':
                    break
                if line.startswith('string'):
                    val = line.split('"', 1)[1].rsplit('"', 1)[0]
                    array_items.append(val)

                elif line.startswith('dict entry('):
                    # Parse one dict entry
                    key = None
                    value = None
                    # Parse key
                    line = next(proc.stdout).strip()
                    if line.startswith('string'):
                        key = line.split('"', 1)[1].rsplit('"', 1)[0]

                    # Parse variant value
                    line = next(proc.stdout).strip()

                    if line.startswith('variant'):
                        # Parse variant content
                        variant_content = line[len('variant'):].strip()
                        if variant_content.startswith('int64'):
                            value = int(variant_content.split()[1])
                        elif variant_content.startswith('string'):
                            # variant string "discord"
                            value = variant_content.split('"', 1)[1].rsplit('"', 1)[0]
                        elif variant_content.startswith('byte'):
                            value = int(variant_content.split()[1])
                        elif variant_content.startswith('struct {'):
                            value = parse_image_data_struct(proc.stdout)
                        else:
                            value = variant_content  # fallback
                    else:
                        # fallback for non-variant lines (unlikely)
                        value = line


                    array_items.append({key: value})

                    # Skip closing parenthesis for dict entry if any
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
            with open("./examine", 'w') as f:
                f.write(str(result))
            state = 'idle'
