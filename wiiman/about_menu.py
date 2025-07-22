import tkinter as tk

from .ui_utils import show_about


def add_about_menu(window):
    menubar = tk.Menu(window)
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=lambda: show_about(window))
    menubar.add_cascade(label="Help", menu=helpmenu)
    window.config(menu=menubar)
