import tkinter as tk
import os
import subprocess
import sys
from .ui_utils import show_about, show_info
from .logger import get_logger

def open_log_folder():
    """Open the log folder in the system file manager."""
    log_dir = get_logger().get_log_directory()
    
    try:
        if sys.platform == "win32":
            os.startfile(log_dir)
        elif sys.platform == "darwin":
            subprocess.run(["open", log_dir])
        else:
            subprocess.run(["xdg-open", log_dir])
    except Exception as e:
        show_info(
            "Error", 
            f"Could not open log folder: {log_dir}\n\nError: {str(e)}"
        )

def show_troubleshooting_info(parent=None):
    """Show troubleshooting information dialog."""
    from .config import APP_VERSION
    
    info_text = (
        f"WiiU CDN Decryptor v{APP_VERSION}\n\n"
        "Troubleshooting Information:\n\n"
        "Common Issues:\n"
        "• Invalid folder errors: Ensure folder contains .app, .tmd, .tik files\n"
        "• Permission errors: Run as administrator if needed\n"
        "• Template missing: Check that template/title.cert exists\n\n"
        "Log Files:\n"
        f"Location: {get_logger().get_log_directory()}\n"
        "Files are created daily with detailed operation logs\n\n"
        "Support:\n"
        "Check log files for detailed error information\n"
        "Report issues with log file content for faster resolution"
    )
    
    # Create custom troubleshooting dialog
    dialog = tk.Toplevel(parent)
    dialog.title("Troubleshooting")
    dialog.resizable(False, False)
    dialog.configure(bg='#f8f9fa')
    dialog.grab_set()
    
    from .ui_utils import center_window
    center_window(dialog, 500, 400)
    
    main_frame = tk.Frame(dialog, bg='#f8f9fa')
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Title
    title_label = tk.Label(
        main_frame,
        text="Troubleshooting Guide",
        font=("Segoe UI", 14, "bold"),
        bg='#f8f9fa',
        fg='#2c3e50'
    )
    title_label.pack(pady=(0, 15))
    
    # Text area with scrollbar
    text_frame = tk.Frame(main_frame)
    text_frame.pack(fill='both', expand=True, pady=(0, 15))
    
    text_widget = tk.Text(
        text_frame,
        width=60,
        height=18,
        font=("Segoe UI", 10),
        bg='white',
        fg='#2c3e50',
        relief='solid',
        bd=1,
        wrap='word',
        padx=10,
        pady=10
    )
    scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    
    text_widget.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    text_widget.insert('1.0', info_text)
    text_widget.config(state='disabled')  # Make read-only
    
    # Button frame
    button_frame = tk.Frame(main_frame, bg='#f8f9fa')
    button_frame.pack(pady=(0, 5))
    
    # Open logs button
    logs_button = tk.Button(
        button_frame,
        text="Open Log Folder",
        command=open_log_folder,
        font=("Segoe UI", 10),
        bg='#3498db',
        fg='white',
        activebackground='#2980b9',
        activeforeground='white',
        width=15,
        cursor='hand2'
    )
    logs_button.pack(side='left', padx=(0, 10))
    
    # Close button
    close_button = tk.Button(
        button_frame,
        text="Close",
        command=dialog.destroy,
        font=("Segoe UI", 10),
        bg='#95a5a6',
        fg='white',
        activebackground='#7f8c8d',
        activeforeground='white',
        width=15,
        cursor='hand2'
    )
    close_button.pack(side='left')
    
    # Keyboard shortcuts
    dialog.bind('<Return>', lambda e: dialog.destroy())
    dialog.bind('<Escape>', lambda e: dialog.destroy())
    
    close_button.focus_set()

def add_about_menu(window):
    """Add enhanced help menu with troubleshooting and log access."""
    menubar = tk.Menu(window)
    
    # Help menu
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=lambda: show_about(window))
    helpmenu.add_separator()
    helpmenu.add_command(label="Troubleshooting", command=lambda: show_troubleshooting_info(window))
    helpmenu.add_command(label="Open Log Folder", command=open_log_folder)
    
    menubar.add_cascade(label="Help", menu=helpmenu)
    window.config(menu=menubar)
