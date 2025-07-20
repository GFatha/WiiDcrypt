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
    messagebox.showinfo("About", "GFatha - Lead Dev", parent=parent)
