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
    """Show enhanced about dialog with detailed information.
    
    Args:
        parent (tk.Widget, optional): Parent window for the dialog.
                                    If None, uses singleton root window.
    """
    from .config import APP_TITLE
    
    if parent is None:
        parent = get_root_window()
    
    # Create custom about dialog
    about_dialog = tk.Toplevel(parent)
    about_dialog.title("About")
    about_dialog.resizable(False, False)
    about_dialog.configure(bg='#f8f9fa')
    about_dialog.grab_set()  # Make modal
    
    # Center the dialog
    center_window(about_dialog, 400, 300)
    
    # Main frame
    main_frame = tk.Frame(about_dialog, bg='#f8f9fa')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Application title
    title_label = tk.Label(
        main_frame,
        text="WiiU CDN Decryptor",
        font=("Segoe UI", 16, "bold"),
        bg='#f8f9fa',
        fg='#2c3e50'
    )
    title_label.pack(pady=(0, 10))
    
    # Version
    version_label = tk.Label(
        main_frame,
        text="Version 2.0",
        font=("Segoe UI", 12),
        bg='#f8f9fa',
        fg='#7f8c8d'
    )
    version_label.pack(pady=(0, 15))
    
    # Description
    desc_text = (
        "A tool for processing WiiU CDN files to prepare them for decryption.\n\n"
        "Features:\n"
        "• Validates CDN folder structure\n"
        "• Renames extensionless files to .app format\n"
        "• Handles TMD file processing\n"
        "• Copies required certificate templates\n"
        "• Progress tracking and error handling"
    )
    
    desc_label = tk.Label(
        main_frame,
        text=desc_text,
        font=("Segoe UI", 10),
        bg='#f8f9fa',
        fg='#34495e',
        justify='left',
        wraplength=350
    )
    desc_label.pack(pady=(0, 15))
    
    # Developer info
    dev_label = tk.Label(
        main_frame,
        text="Lead Developer: GFatha",
        font=("Segoe UI", 10, "bold"),
        bg='#f8f9fa',
        fg='#2c3e50'
    )
    dev_label.pack(pady=(0, 5))
    
    # Copyright
    copyright_label = tk.Label(
        main_frame,
        text="© 2025 WiiDcrypt Project",
        font=("Segoe UI", 9),
        bg='#f8f9fa',
        fg='#95a5a6'
    )
    copyright_label.pack(pady=(0, 20))
    
    # Close button
    close_button = tk.Button(
        main_frame,
        text="Close",
        command=about_dialog.destroy,
        font=("Segoe UI", 10),
        bg='#3498db',
        fg='white',
        activebackground='#2980b9',
        activeforeground='white',
        width=10,
        cursor='hand2'
    )
    close_button.pack()
    
    # Keyboard shortcut
    about_dialog.bind('<Return>', lambda e: about_dialog.destroy())
    about_dialog.bind('<Escape>', lambda e: about_dialog.destroy())
    
    # Focus the close button
    close_button.focus_set()


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
