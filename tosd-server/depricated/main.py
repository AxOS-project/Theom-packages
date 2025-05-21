import argparse
import tkinter as tk
from tkinter import font

def calculate_position(pos_code, width, height, screen_width, screen_height, margin=20):
    # Default positions in (x, y)
    pos_code = pos_code.upper()
    x = y = 0

    # Center horizontal and vertical helpers
    center_x = (screen_width - width) // 2
    center_y = (screen_height - height) // 2

    if 'T' in pos_code:
        y = margin
    elif 'B' in pos_code:
        y = screen_height - height - margin
    else:
        # vertically center if no T or B
        y = center_y

    if 'L' in pos_code:
        x = margin
    elif 'R' in pos_code:
        x = screen_width - width - margin
    else:
        # horizontally center if no L or R
        x = center_x

    # If only C, center both
    if pos_code == 'C':
        x, y = center_x, center_y

    return x, y

def show_osd(text, mode, value, duration, size, position):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.config(bg="#23262d")

    base_font_size = int(28 * size)
    fnt = font.Font(family="Sans", size=base_font_size)

    text_width = fnt.measure(text) if text else 0
    slider_width = int(250 * size) if mode == "slider" else 0
    padding = int(40 * size)
    gap = int(20 * size) if text and mode == "slider" else 0

    width = text_width + slider_width + padding + gap
    height = int(80 * size)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x, y = calculate_position(position, width, height, screen_width, screen_height)

    root.geometry(f"{width}x{height}+{x}+{y}")

    canvas = tk.Canvas(root, width=width, height=height, bg="#23262d", highlightthickness=0)
    canvas.pack()

    if text:
        canvas.create_text(int(20 * size), height // 2, text=text, anchor="w", font=fnt, fill="#ffffff")

    if mode == "slider":
        bar_x0 = text_width + gap + int(20 * size) if text else int(20 * size)
        bar_y0 = height // 2 - int(15 * size)
        bar_x1 = bar_x0 + slider_width
        bar_y1 = height // 2 + int(15 * size)

        canvas.create_rectangle(bar_x0, bar_y0, bar_x1, bar_y1, outline="#555555", width=2, fill="#3a3f4b")

        val = max(0, min(100, value))
        fill_width = int((val / 100) * (bar_x1 - bar_x0))
        canvas.create_rectangle(bar_x0, bar_y0, bar_x0 + fill_width, bar_y1, outline="", fill="#61afef")

        knob_x = bar_x0 + fill_width
        canvas.create_oval(knob_x - int(10 * size), bar_y0 - int(5 * size), knob_x + int(10 * size), bar_y1 + int(5 * size), fill="#528bff", outline="")

    elif mode == "text":
        if not text and value is not None:
            full_text = f"{value}"
            canvas.delete("all")
            canvas.create_text(width // 2, height // 2, text=full_text, font=fnt, fill="#ffffff")
        elif value is not None and text:
            full_text = f"{text}: {value}"
            canvas.delete("all")
            width = fnt.measure(full_text) + padding
            root.geometry(f"{width}x{height}+{x}+{y}")
            canvas.config(width=width)
            canvas.create_text(width // 2, height // 2, text=full_text, font=fnt, fill="#ffffff")
    else:
        print(f"Unsupported mode: {mode}")
        root.destroy()
        return

    root.after(int(duration * 1000), root.destroy)
    root.mainloop()

def main():
    parser = argparse.ArgumentParser(description="tosd - Theom On Screen Display")
    parser.add_argument("text", type=str, nargs="?", default="", help="Text label (empty disables text)")
    parser.add_argument("mode", choices=["slider", "text"], help="Display mode: slider or text")
    parser.add_argument("value", type=int, nargs="?", default=None, help="Value for slider or text display")
    parser.add_argument("-d", "--duration", type=float, default=2.0, help="Duration to show OSD in seconds")
    parser.add_argument("-s", "--size", type=float, default=1.0, help="Size multiplier for OSD (default 1.0)")
    parser.add_argument("-p", "--position", type=str, default="T", help="Position on screen (T, TR, R, BR, B, BL, L, TL, C)")

    args = parser.parse_args()

    if args.value is None:
        print("Error: You must specify a value for slider or text mode.")
        return

    valid_positions = {"T", "TR", "R", "BR", "B", "BL", "L", "TL", "C"}
    if args.position.upper() not in valid_positions:
        print(f"Error: Invalid position '{args.position}'. Choose from {valid_positions}")
        return

    show_osd(args.text, args.mode, args.value, args.duration, args.size, args.position)

if __name__ == "__main__":
    main()