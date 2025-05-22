import gi
gi.require_version("Gtk", "3.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Gtk, Gdk, GLib, Pango, PangoCairo

_reuse_next_window = False
_osd_windows = []

def reuse_osd_window():
    global _reuse_next_window
    _reuse_next_window = True

def clear_osd_windows():
    global _osd_windows
    for win in _osd_windows[:]:
        try:
            win.destroy()
        except:
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

class OSDWindow(Gtk.Window):
    def __init__(self, text, mode, value, duration, size,
                 background="#23262d", text_color="#ffffff",
                 slider_fill_color="#61afef", slider_knob_color="#528bff",
                 position="C"):
        super().__init__(type=Gtk.WindowType.POPUP)
        self.set_app_paintable(True)
        self.set_keep_above(True)
        self.set_accept_focus(False)
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_visual(self.get_screen().get_rgba_visual())
        self.timeout_id = None
        self.start_timeout(duration)

        self.text = text
        self.mode = mode
        self.value = value
        self.duration = duration
        self.size = size
        self.background = background
        self.text_color = text_color
        self.slider_fill_color = slider_fill_color
        self.slider_knob_color = slider_knob_color
        self.position = position.upper()

        self.connect("draw", self.on_draw)
        self.connect("destroy", self.on_destroy)

        # Calculate dimensions
        self.base_font_size = int(28 * size)
        self.padding = int(40 * size)
        self.gap = int(20 * size) if text and mode == "slider" else 0
        self.height = int(80 * size)
        self.slider_width = int(250 * size) if mode == "slider" else 0

        # pago layout
        self.layout = self.create_pango_layout("")
        font_desc = Pango.FontDescription(f"Sans {self.base_font_size}")
        self.layout.set_font_description(font_desc)

        self.text_width = self.measure_text_width(text) if text else 0
        self.width = self.text_width + self.slider_width + self.padding + self.gap
        if mode == "text":
            full_text = f"{text}: {value}" if text and value is not None else str(value or text)
            self.text_width = self.measure_text_width(full_text)
            self.width = self.text_width + self.padding

        screen = self.get_screen()
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        x, y = calculate_position(self.position, self.width, self.height, screen_width, screen_height)
        self.set_size_request(self.width, self.height)
        self.move(x, y)

        #self.timeout_id = GLib.timeout_add(int(duration * 1000), self.hide)

        self.show_all()

    def start_timeout(self, duration):
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self.timeout_id = GLib.timeout_add(int(duration * 1000), self._on_timeout)

    def _on_timeout(self):
        # Timeout callback
        self.timeout_id = None
        self.hide()
        if self in _osd_windows:
            _osd_windows.remove(self)
        self.destroy()
        return False  # Stop timeout

    def measure_text_width(self, text):
        self.layout.set_text(text, -1)
        width, _ = self.layout.get_pixel_size()
        return width

    def on_draw(self, widget, cr):
        # Set background color
        rgba = Gdk.RGBA()
        rgba.parse(self.background)
        cr.set_source_rgba(rgba.red, rgba.green, rgba.blue, rgba.alpha)
        cr.rectangle(0, 0, self.width, self.height)
        cr.fill()

        # Draw text
        if self.mode == "slider" or self.mode == "text":
            cr.set_source_rgba(*self.color_to_rgba(self.text_color))
            _, text_height = self.layout.get_pixel_size()
            text_y = (self.height - text_height) // 2
            cr.move_to(int(20 * self.size), text_y)

            if self.mode == "slider" and self.text:
                self.layout.set_text(self.text, -1)
            elif self.mode == "text":
                full_text = f"{self.text}: {self.value}" if self.text and self.value is not None else str(self.value or self.text)
                self.layout.set_text(full_text, -1)
            PangoCairo.show_layout(cr, self.layout)

        if self.mode == "slider":
            bar_x0 = self.text_width + self.gap + int(20 * self.size) if self.text else int(20 * self.size)
            bar_y0 = self.height // 2 - int(15 * self.size)
            bar_x1 = bar_x0 + self.slider_width
            bar_y1 = self.height // 2 + int(15 * self.size)

            # Draw slider background
            cr.set_source_rgba(*self.color_to_rgba("#3a3f4b"))
            cr.rectangle(bar_x0, bar_y0, bar_x1 - bar_x0, bar_y1 - bar_y0)
            cr.fill()

            # Draw slider border
            cr.set_source_rgba(*self.color_to_rgba("#555555"))
            cr.set_line_width(2)
            cr.rectangle(bar_x0, bar_y0, bar_x1 - bar_x0, bar_y1 - bar_y0)
            cr.stroke()

            # Draw filled portion
            val = max(0, min(100, self.value))
            fill_width = int((val / 100) * (bar_x1 - bar_x0))
            cr.set_source_rgba(*self.color_to_rgba(self.slider_fill_color))
            cr.rectangle(bar_x0, bar_y0, fill_width, bar_y1 - bar_y0)
            cr.fill()

            # Draw knob
            knob_width = int(8 * self.size)
            knob_height = int(35 * self.size)
            knob_x = bar_x0 + fill_width
            knob_y0 = (bar_y0 + bar_y1) // 2 - knob_height // 2

            cr.set_source_rgba(*self.color_to_rgba(self.slider_knob_color))
            cr.rectangle(knob_x - knob_width // 2, knob_y0, knob_width, knob_height)
            cr.fill()

        return False

    def color_to_rgba(self, color_str):
        rgba = Gdk.RGBA()
        rgba.parse(color_str)
        return (rgba.red, rgba.green, rgba.blue, rgba.alpha)

    def close_osd(self):
        # Call the original Gtk.Window.hide() to hide the window
        super().hide()

        if self in _osd_windows:
            _osd_windows.remove(self)

        self.destroy()

        return False

    def on_destroy(self, *args):
        if self in _osd_windows:
            _osd_windows.remove(self)


def show_osd(text, mode, value, duration, size, position,
             background="#23262d", text_color="#ffffff",
             slider_fill_color="#61afef", slider_knob_color="#528bff"):

    global _reuse_next_window

    if _reuse_next_window and _osd_windows:
        win = _osd_windows[-1]
        win.text = text
        win.mode = mode
        win.value = value
        win.duration = duration
        win.size = size
        win.background = background
        win.text_color = text_color
        win.slider_fill_color = slider_fill_color
        win.slider_knob_color = slider_knob_color
        win.position = position.upper()
        win.start_timeout(duration)

        # Recalculate geometry and redraw
        win.queue_draw()
        win.show()
        _reuse_next_window = False
        return

    _reuse_next_window = False

    win = OSDWindow(text, mode, value, duration, size, background, text_color, slider_fill_color, slider_knob_color, position)
    _osd_windows.append(win)

    #Gtk.main()
