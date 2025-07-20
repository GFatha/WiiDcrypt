import tkinter as tk
from tkinter import messagebox

def show_about(window=None):
    # If a window is provided, use it as the parent; else, create a temp root
    if window is None:
        temp_root = tk.Tk()
        temp_root.withdraw()
        messagebox.showinfo("About", "GFatha - Lead Dev", parent=temp_root)
        temp_root.destroy()
    else:
        messagebox.showinfo("About", "GFatha - Lead Dev", parent=window)
