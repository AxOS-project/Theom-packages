from pydbus import SessionBus
from gi.repository import GLib
import asyncio
from tosd_core import show_osd, clear_osd_windows, reuse_osd_window

class TOSDService:
    """
    <node>
        <interface name='org.theom.tosd'>
            <method name='ShowOSD'>
                <arg type='s' name='text' direction='in'/>
                <arg type='s' name='mode' direction='in'/>
                <arg type='i' name='value' direction='in'/>
                <arg type='d' name='duration' direction='in'/>
                <arg type='d' name='size' direction='in'/>
                <arg type='s' name='position' direction='in'/>
                <arg type='b' name='reuse_window' direction='in'/>
                <arg type='s' name='background' direction='in'/>
                <arg type='s' name='text_color' direction='in'/>
                <arg type='s' name='slider_fill_color' direction='in'/>
                <arg type='s' name='slider_knob_color' direction='in'/>
            </method>
            <method name='ClearAll'/>
        </interface>
    </node>
    """

    def ShowOSD(self, text, mode, value, duration, size, position, reuse_window, background,
                text_color, slider_fill_color, slider_knob_color):

        if reuse_window:
            reuse_osd_window()

        def gtk_callback():
            show_osd(text, mode, value, duration, size, position,
                     background, text_color, slider_fill_color, slider_knob_color)
            return False  # Remove from GLib idle queue

        GLib.idle_add(gtk_callback)

        return "OK"

    def ClearAll(self):
        def gtk_callback():
            clear_osd_windows()
            return False
        GLib.idle_add(gtk_callback)
        return "Cleared"


async def main():
    bus = SessionBus()
    loop = asyncio.get_running_loop()
    service = TOSDService()

    bus_name = "org.theom.tosd"
    object_path = "/org/theom/tosd"

    bus.publish(bus_name, (object_path, service))

    print(f"TOSD D-Bus server running at {bus_name} {object_path}")

    future = asyncio.Future()

    def run_glib():
        GLib.MainLoop().run()

    import threading
    threading.Thread(target=run_glib, daemon=True).start()

    await future

if __name__ == "__main__":
    asyncio.run(main())
