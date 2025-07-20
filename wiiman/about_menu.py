import tkinter as tk
from tkinter import messagebox

def _get_root_window():
    """Get or create a single root window for dialogs."""
    try:
        root = tk._default_root
        if root is None:
            root = tk.Tk()
            root.withdraw()
        return root
    except:
        root = tk.Tk()
        root.withdraw()
        return root

def show_about(window=None):
    """Show about dialog with proper resource management."""
    parent = window if window is not None else _get_root_window()
    messagebox.showinfo("About", "Lead Dev - GFatha", parent=parent)

def add_about_menu(window):
    menubar = tk.Menu(window)
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=lambda: show_about(window))
    menubar.add_cascade(label="Help", menu=helpmenu)
    window.config(menu=menubar)
