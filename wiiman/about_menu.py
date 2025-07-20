import tkinter as tk
from tkinter import messagebox

def show_about(window=None):
    # If a window is provided, use it as the parent; else, create a temp root
    if window is None:
        temp_root = tk.Tk()
        temp_root.withdraw()
        messagebox.showinfo("About", "Lead Dev - GFatha", parent=temp_root)
        temp_root.destroy()
    else:
        messagebox.showinfo("About", "Lead Dev - GFatha", parent=window)

def add_about_menu(window):
    menubar = tk.Menu(window)
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=lambda: show_about(window))
    menubar.add_cascade(label="Help", menu=helpmenu)
    window.config(menu=menubar)
