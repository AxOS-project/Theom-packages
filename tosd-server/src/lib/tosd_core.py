import tkinter as tk
from tkinter import font

_reuse_next_window = False
_osd_windows = []

def reuse_osd_window():
    global _reuse_next_window
    _reuse_next_window = True

def clear_osd_windows():
    for win in _osd_windows[:]:
        try:
            win.destroy()
        except tk.TclError:
            pass
        _osd_windows.remove(win)

def calculate_position(pos_code, width, height, screen_width, screen_height, margin=20):
    pos_code = pos_code.upper()
    center_x = (screen_width - width) // 2
    center_y = (screen_height - height) // 2

    if 'T' in pos_code:
        y = margin
    elif 'B' in pos_code:
        y = screen_height - height - margin
    else:
        y = center_y

    if 'L' in pos_code:
        x = margin
    elif 'R' in pos_code:
        x = screen_width - width - margin
    else:
        x = center_x

    if pos_code == 'C':
        x, y = center_x, center_y

    return x, y

def show_osd(text, mode, value, duration, size, position,
             background="#23262d", text_color="#ffffff",
             slider_fill_color="#61afef", slider_knob_color="#528bff"):

    global _reuse_next_window

    if _reuse_next_window and _osd_windows:
        root = _osd_windows[-1]

        for widget in root.winfo_children():
            widget.destroy()

        if hasattr(root, '_close_after_id'):
            root.after_cancel(root._close_after_id)
        root.deiconify()
    else:
        root = tk.Tk()
        _osd_windows.append(root)
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.config(bg=background)

    _reuse_next_window = False

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

    canvas = tk.Canvas(root, width=width, height=height, bg=background, highlightthickness=0)
    canvas.pack()

    if text:
        canvas.create_text(int(20 * size), height // 2, text=text, anchor="w", font=fnt, fill=text_color)

    if mode == "slider":
        bar_x0 = text_width + gap + int(20 * size) if text else int(20 * size)
        bar_y0 = height // 2 - int(15 * size)
        bar_x1 = bar_x0 + slider_width
        bar_y1 = height // 2 + int(15 * size)

        canvas.create_rectangle(bar_x0, bar_y0, bar_x1, bar_y1, outline="#555555", width=2, fill="#3a3f4b")

        val = max(0, min(100, value))
        fill_width = int((val / 100) * (bar_x1 - bar_x0))
        canvas.create_rectangle(bar_x0, bar_y0, bar_x0 + fill_width, bar_y1, outline="", fill=slider_fill_color)

        knob_width = int(8 * size)
        knob_height = int(35 * size)
        knob_x = bar_x0 + fill_width
        knob_y0 = (bar_y0 + bar_y1) // 2 - knob_height // 2
        knob_y1 = knob_y0 + knob_height

        canvas.create_rectangle(
            knob_x - knob_width // 2, knob_y0,
            knob_x + knob_width // 2, knob_y1,
            fill=slider_knob_color, outline=""
        )

    elif mode == "text":
        canvas.delete("all")
        full_text = f"{text}: {value}" if text and value is not None else str(value or text)
        width = fnt.measure(full_text) + padding
        root.geometry(f"{width}x{height}+{x}+{y}")
        canvas.config(width=width)
        canvas.create_text(width // 2, height // 2, text=full_text, font=fnt, fill=text_color)

    else:
        print(f"Unsupported mode: {mode}")
        root.withdraw()
        return

    def hide_window():
        try:
            root.withdraw()
        except tk.TclError:
            pass

    root._close_after_id = root.after(int(duration * 1000), hide_window)

    root.mainloop()
