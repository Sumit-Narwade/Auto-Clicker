import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
import pyautogui
from pynput import keyboard, mouse

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False

running = False
click_points = []

# ------------------------------
# PICK POINT ON SCREEN
# ------------------------------
def pick_point():
    def listener_thread():
        root.attributes("-alpha", 0)
        time.sleep(0.2)
        messagebox.showinfo("Pick Point",
                            "Click anywhere on the screen to select a point.\nWindow will reappear automatically.")

        def on_click(x, y, button, pressed):
            if pressed:
                click_points.append((x, y))
                update_point_list()
                root.attributes("-alpha", 0.85)
                return False

        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

    threading.Thread(target=listener_thread, daemon=True).start()


# ------------------------------
# ADD CURRENT MOUSE POSITION
# ------------------------------
def add_current_point():
    x, y = pyautogui.position()
    click_points.append((x, y))
    update_point_list()


# ------------------------------
# DELETE SELECTED POINT
# ------------------------------
def delete_point():
    selection = point_list.curselection()
    if not selection:
        return
    index = selection[0]
    del click_points[index]
    update_point_list()


# ------------------------------
# UPDATE LISTBOX
# ------------------------------
def update_point_list():
    point_list.delete(0, tk.END)
    for idx, (x, y) in enumerate(click_points):
        point_list.insert(tk.END, f"{idx+1}.  ( {x} , {y} )")


# ------------------------------
# START CLICKING
# ------------------------------
def start_clicking():
    global running

    if not click_points:
        messagebox.showerror("Error", "Add at least one click point!")
        return

    try:
        interval = float(interval_entry.get())
        rand_delay = float(random_entry.get())
        repeat = repeat_entry.get()

        if repeat.strip() == "" or repeat == "0":
            repeat = None
        else:
            repeat = int(repeat)

    except:
        messagebox.showerror("Error", "Enter valid numbers!")
        return

    click_type = click_type_var.get()
    running = True

    def worker():
        global running
        count = 0
        while running:
            for (x, y) in click_points:
                if not running:
                    break

                if click_type == "Left":
                    pyautogui.click(x, y, button="left")
                elif click_type == "Right":
                    pyautogui.click(x, y, button="right")
                elif click_type == "Double":
                    pyautogui.doubleClick(x, y)

                # Random delay
                delay = interval + random.uniform(0, rand_delay)
                time.sleep(delay)

                count += 1
                if repeat is not None and count >= repeat:
                    running = False
                    break

    threading.Thread(target=worker, daemon=True).start()


# ------------------------------
# STOP CLICKING
# ------------------------------
def stop_clicking():
    global running
    running = False


# ------------------------------
# HOTKEYS (F5 START, F6 STOP)
# ------------------------------
def on_key_press(key):
    if key == keyboard.Key.f5:
        start_clicking()
    elif key == keyboard.Key.f6:
        stop_clicking()


keyboard.Listener(on_press=on_key_press).start()


# ------------------------------
# GUI
# ------------------------------
root = tk.Tk()
root.title("Modern Auto Clicker")
root.geometry("450x500")
root.resizable(False, False)
root.attributes("-alpha", 0.85)
root.config(bg="#1e1e1e")

# Title
title = tk.Label(root, text="AUTO CLICKER", fg="white", bg="#1e1e1e",
                 font=("Segoe UI", 18, "bold"))
title.pack(pady=10)

# Point Listbox
point_list = tk.Listbox(root, font=("Segoe UI", 11), height=6,
                        bg="#2e2e2e", fg="white", selectbackground="#00aaff")
point_list.pack(pady=10, fill="x", padx=20)

# Buttons frame
frame_btn = tk.Frame(root, bg="#1e1e1e")
frame_btn.pack()

tk.Button(frame_btn, text="Add Current", command=add_current_point,
          width=12, bg="#00cc66", fg="white").grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Pick Point", command=pick_point,
          width=12, bg="#ffaa00", fg="black").grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Delete", command=delete_point,
          width=12, bg="#ff4444", fg="white").grid(row=0, column=2, padx=5)

# Options
options = tk.Frame(root, bg="#1e1e1e")
options.pack(pady=10)

# Click type
tk.Label(options, text="Click Type", bg="#1e1e1e", fg="white").grid(row=0, column=0)
click_type_var = tk.StringVar(value="Left")
tk.OptionMenu(options, click_type_var, "Left", "Right", "Double").grid(row=0, column=1)

# Interval
tk.Label(options, text="Interval (sec):", bg="#1e1e1e", fg="white").grid(row=1, column=0)
interval_entry = tk.Entry(options, width=8)
interval_entry.insert(0, "0.5")
interval_entry.grid(row=1, column=1)

# Random delay
tk.Label(options, text="Random Delay:", bg="#1e1e1e", fg="white").grid(row=2, column=0)
random_entry = tk.Entry(options, width=8)
random_entry.insert(0, "0.2")
random_entry.grid(row=2, column=1)

# Repeat count
tk.Label(options, text="Repeat Count:", bg="#1e1e1e", fg="white").grid(row=3, column=0)
repeat_entry = tk.Entry(options, width=8)
repeat_entry.insert(0, "0")
repeat_entry.grid(row=3, column=1)

# Start/Stop buttons
tk.Button(root, text="START (F5)", command=start_clicking,
          bg="#00ccff", fg="black", width=20).pack(pady=10)
tk.Button(root, text="STOP (F6)", command=stop_clicking,
          bg="#ff4444", fg="white", width=20).pack()

root.mainloop()
