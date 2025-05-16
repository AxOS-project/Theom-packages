#!/usr/bin/env python3

import gi
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class SettingsHub(Gtk.Window):
    def __init__(self):
        super().__init__(title="Theom Settings")
        self.connect("button-press-event", self.on_window_click)
        self.set_default_size(600, 400)
        self.set_resizable(False)
        self.connect("destroy", Gtk.main_quit)
        self.get_style_context().add_class("main-window")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_homogeneous(False)
        vbox.set_hexpand(False)
        self.add(vbox)


        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header.set_halign(Gtk.Align.END)
        header.set_margin_top(10)
        header.set_margin_right(10)
        header.set_margin_bottom(10)
        vbox.pack_start(header, False, False, 0)

        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Search settings...")
        self.search_entry.set_width_chars(25)
        self.search_entry.connect("changed", self.on_search_changed)
        self.search_entry.get_style_context().add_class("search-entry")
        header.pack_end(self.search_entry, False, False, 0)

        self.hidden_entry = Gtk.Entry()
        self.hidden_entry.set_visible(False)
        self.hidden_entry.set_no_show_all(True)
        vbox.pack_start(self.hidden_entry, False, False, 0)

        self.icon_grid = Gtk.FlowBox()
        self.icon_grid.set_max_children_per_line(4)
        self.icon_grid.set_selection_mode(Gtk.SelectionMode.NONE)
        self.icon_grid.set_column_spacing(20)
        self.icon_grid.set_row_spacing(20)
        self.icon_grid.set_margin_top(20)
        self.icon_grid.set_margin_left(20)
        self.icon_grid.set_margin_right(20)
        self.icon_grid.set_halign(Gtk.Align.START)
        vbox.pack_start(self.icon_grid, False, False, 0)

        self.settings_buttons = []
        self.add_icon_button("Appearance", "preferences-desktop-theme", self.launch_lxappearance)

        self.apply_theme()

    def on_window_click(self, widget, event):
        allocation = self.search_entry.get_allocation()

        if not (allocation.x <= event.x <= allocation.x + allocation.width and
                allocation.y <= event.y <= allocation.y + allocation.height):
            self.hidden_entry.grab_focus()

    def add_icon_button(self, label_text, icon_name, callback):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.CENTER)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)

        icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
        label = Gtk.Label(label=label_text)
        label.set_justify(Gtk.Justification.CENTER)

        event_box = Gtk.EventBox()
        event_box.add(box)
        event_box.connect("button-press-event", lambda w, e: callback())
        event_box.get_style_context().add_class("icon-button")

        box.pack_start(icon, False, False, 0)
        box.pack_start(label, False, False, 0)

        self.icon_grid.add(event_box)
        self.settings_buttons.append((label_text.lower(), event_box))

    def on_search_changed(self, entry):
        text = entry.get_text().lower()
        for label, widget in self.settings_buttons:
            widget.set_visible(text in label)

    def launch_lxappearance(self):
        subprocess.Popen(["lxappearance"])

    def apply_theme(self):
        provider = Gtk.CssProvider()
        css = """
        .main-window {
            background-color: #1e1e1e;
        }

        .search-entry {
            padding: 6px;
            border-radius: 8px;
            background-color: #2c2c2c;
            color: #ffffff;
            margin-top: 10px;
            margin-right: 10px;
            margin-bottom: 10px;
            margin-left: 10px;
        }

        .icon-button {
            border-radius: 10px;
            background-color: #2e2e2e;
            padding: 6px;
            margin-top: 20px;
            margin-left: 20px;
            margin-right: 20px;
            margin-bottom: 20px;
        }

        .icon-button:hover {
            background-color: #3d3d3d;
        }

        .icon-button GtkLabel {
            color: #ffffff;
            font-size: 14px;
        }
        """

        try:
            provider.load_from_data(css.encode("utf-8"))
        except GLib.Error as e:
            print(f"CSS load error: {e.message}")

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

if __name__ == "__main__":
    app = SettingsHub()
    app.show_all()
    Gtk.main()
