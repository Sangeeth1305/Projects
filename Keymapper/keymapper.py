import tkinter as tk
import os
import threading
from pynput import keyboard

ADB_PATH = r"D:\\Projects\\Scrcpy\\adb.exe"  # Update this path

# Define keys and their initial positions
key_positions = {
    "W": (250, 600),
    "A": (200, 650),
    "S": (250, 700),
    "D": (300, 650),
    "SPACE": (450, 400)
}

# Store active keys
active_keys = {}

def adb_touch_down(key, x, y):
    cmd = f'"{ADB_PATH}" shell input tap {x} {y} {x} {y} 1 1'
    proc = threading.Thread(target=lambda: os.system(cmd))
    proc.start()
    active_keys[key] = proc

def adb_touch_up(key):
    os.system(f'"{ADB_PATH}" shell input tap 1 1')  # Ends the "hold"
    active_keys.pop(key, None)

def on_press(key):
    try:
        k = key.char.upper()
    except AttributeError:
        k = key.name.upper()

    if k in key_positions and k not in active_keys:
        x, y = key_positions[k]
        adb_touch_down(k, x, y)

def on_release(key):
    try:
        k = key.char.upper()
    except AttributeError:
        k = key.name.upper()

    if k in active_keys:
        adb_touch_up(k)

# GUI app
def create_markers(root):
    windows = {}

    for key, (x, y) in key_positions.items():
        win = tk.Toplevel(root)
        win.overrideredirect(True)
        win.geometry(f"40x40+{x}+{y}")
        win.attributes("-topmost", True)
        win.attributes("-alpha", 0.6)

        label = tk.Label(win, text=key, bg="red", fg="white", font=("Arial", 10))
        label.pack(fill=tk.BOTH, expand=True)

        def start_drag(event, win=win):
            win._drag_start_x = event.x
            win._drag_start_y = event.y

        def do_drag(event, key=key, win=win):
            dx = event.x - win._drag_start_x
            dy = event.y - win._drag_start_y
            x = win.winfo_x() + dx
            y = win.winfo_y() + dy
            win.geometry(f"+{x}+{y}")
            key_positions[key] = (x, y)

        label.bind("<ButtonPress-1>", start_drag)
        label.bind("<B1-Motion>", do_drag)

        windows[key] = win

    return windows

# Main
def main():
    # Start keyboard listener
    listener_thread = threading.Thread(
        target=lambda: keyboard.Listener(on_press=on_press, on_release=on_release).run(), daemon=True)
    listener_thread.start()

    # Start GUI
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    create_markers(root)
    root.mainloop()

main()
