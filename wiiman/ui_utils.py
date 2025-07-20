"""
UI utilities and common dialog functions for WiiDcrypt.

This module provides centralized UI functionality to eliminate code duplication
and ensure consistent behavior across the application.
"""
import tkinter as tk
from tkinter import messagebox


def get_root_window():
    """Get or create a single root window for dialogs.
    
    Returns:
        tk.Tk: The root window instance, hidden from view
    """
    try:
        root = tk._default_root
        if root is None:
            root = tk.Tk()
            root.withdraw()  # Hide the root window
        return root
    except:
        root = tk.Tk()
        root.withdraw()
        return root


def show_about(parent=None):
    """Show about dialog with proper resource management.
    
    Args:
        parent (tk.Widget, optional): Parent window for the dialog.
                                    If None, uses singleton root window.
    """
    if parent is None:
        parent = get_root_window()
    messagebox.showinfo("About", "Lead Dev - GFatha", parent=parent)


def center_window(window, width, height):
    """Center a window on the screen.
    
    Args:
        window (tk.Tk): The window to center
        width (int): Window width in pixels
        height (int): Window height in pixels
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")


def show_info(title, message, parent=None):
    """Show info message with proper parent management.
    
    Args:
        title (str): Dialog title
        message (str): Dialog message
        parent (tk.Widget, optional): Parent window for the dialog
    """
    if parent is None:
        parent = get_root_window()
    messagebox.showinfo(title, message, parent=parent)


def show_warning(title, message, parent=None):
    """Show warning message with proper parent management.
    
    Args:
        title (str): Dialog title
        message (str): Dialog message
        parent (tk.Widget, optional): Parent window for the dialog
    """
    if parent is None:
        parent = get_root_window()
    messagebox.showwarning(title, message, parent=parent)


def ask_yes_no(title, message, parent=None):
    """Ask yes/no question with proper parent management.
    
    Args:
        title (str): Dialog title
        message (str): Dialog message
        parent (tk.Widget, optional): Parent window for the dialog
        
    Returns:
        bool: True if user selected Yes, False otherwise
    """
    if parent is None:
        parent = get_root_window()
    return messagebox.askyesno(title, message, parent=parent)


def ask_question(title, message, parent=None):
    """Ask question with proper parent management.
    
    Args:
        title (str): Dialog title
        message (str): Dialog message
        parent (tk.Widget, optional): Parent window for the dialog
        
    Returns:
        str: 'yes' or 'no' based on user selection
    """
    if parent is None:
        parent = get_root_window()
    return messagebox.askquestion(title, message, icon="warning", parent=parent)
