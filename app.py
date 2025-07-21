import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from wiiman.validator import select_and_validate_folder
from wiiman.rename import rename_extensionless_files
from wiiman.ui_utils import show_about, show_info, center_window, get_root_window
from wiiman.logger import log_info, log_error, log_exception, log_operation, log_debug
from wiiman.config import (
    DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT,
    APP_TITLE, BUTTON_WIDTH, DEFAULT_FONT,
    PADDING_LARGE, PADDING_MEDIUM, MESSAGES,
    COLORS, APP_VERSION, PROGRESS_DIALOG_WIDTH, PROGRESS_DIALOG_HEIGHT
)
        
def cancel_and_exit(window):
    """Cancel operation and exit application with user confirmation."""
    from wiiman.ui_utils import ask_yes_no
    
    log_debug("User initiated exit sequence")
    
    # Ask for confirmation before exiting
    if ask_yes_no(
        "Confirm Exit", 
        "Are you sure you want to exit WiiU CDN Decryptor?", 
        parent=window
    ):
        log_info("User confirmed application exit")
        window.destroy()
        # Use sys.exit instead of exit() for cleaner shutdown
        import sys
        sys.exit(0)
    else:
        log_debug("User cancelled exit sequence")
    # If user says no, do nothing and return to application

def dorun(main_window=None):
    """Run the main decryption process with progress feedback and comprehensive logging.
    
    Args:
        main_window (tk.Tk, optional): Main window to close after completion
    """
    from wiiman.progress_dialog import ProgressDialog
    from wiiman.rename_tmd_files import handle_tmd_logic
    
    log_operation("Process CDN Files", details="User initiated CDN processing")
    
    selected_path = select_and_validate_folder()
    if not selected_path:
        log_info("User cancelled folder selection")
        return
    
    log_operation("Folder Selected", path=selected_path, details=f"Processing {os.path.basename(selected_path)}")
    
    # Create progress dialog
    progress = ProgressDialog(
        parent=main_window,
        title="Processing CDN Files",
        width=PROGRESS_DIALOG_WIDTH,
        height=PROGRESS_DIALOG_HEIGHT
    )
    
    operation_start_time = __import__('time').time()
    
    try:
        # Step 1: Rename extensionless files
        log_info("Starting step 1: Rename extensionless files")
        progress.set_status("Renaming extensionless files...")
        progress.set_details(f"Processing folder: {os.path.basename(selected_path)}")
        progress.set_progress(25)
        
        step_start = __import__('time').time()
        rename_extensionless_files(selected_path)
        log_info(f"Step 1 completed in {__import__('time').time() - step_start:.2f}s")
        
        # Step 2: Copy template file
        log_info("Starting step 2: Copy certificate template")
        progress.set_status("Copying certificate template...")
        progress.set_details("Adding title.cert file")
        progress.set_progress(50)
        
        src = os.path.join(os.path.dirname(__file__), 'template', 'title.cert')
        dst = os.path.join(selected_path, 'title.cert')
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            log_info(f"Template copied: {src} -> {dst}")
        else:
            log_error(f"Template file not found: {src}")
            progress.set_details("Warning: title.cert template not found")
        
        # Step 3: Handle TMD logic
        log_info("Starting step 3: Process TMD files")
        progress.set_status("Processing TMD files...")
        progress.set_details("Checking and processing title.tmd files")
        progress.set_progress(75)
        
        step_start = __import__('time').time()
        handle_tmd_logic(selected_path)
        log_info(f"Step 3 completed in {__import__('time').time() - step_start:.2f}s")
        
        # Step 4: Complete
        progress.set_status("Operation completed successfully!")
        progress.set_details("All files processed")
        progress.set_progress(100)
        
        total_time = __import__('time').time() - operation_start_time
        log_operation("Processing Complete", path=selected_path, details=f"Total time: {total_time:.2f}s")
        
        # Brief delay to show completion
        import time
        time.sleep(0.5)
        
    except Exception as e:
        log_exception(f"Error during CDN processing: {str(e)}")
        progress.set_status("Error occurred")
        progress.set_details(str(e))
        show_info("Error", f"An error occurred during processing:\n{str(e)}", parent=main_window)
        return  # Exit early on error
    finally:
        progress.close()
    
    log_info("CDN processing completed successfully")
    
    # Show completion message
    parent = main_window if main_window else get_root_window()
    show_info("Complete", MESSAGES['operation_completed'], parent=parent)
    
    if main_window:
        # Ask if user wants to process another folder
        from wiiman.ui_utils import ask_yes_no
        log_debug("Asking user about processing another folder")
        if not ask_yes_no(
            "Process Another?", 
            "Would you like to process another folder?", 
            parent=main_window
        ):
            log_info("User chose to exit application after completion")
            main_window.quit()
            main_window.destroy()
        else:
            log_info("User chose to process another folder")

def create_tooltip(widget, text):
    """Create a tooltip for a widget.
    
    Args:
        widget (tk.Widget): Widget to add tooltip to
        text (str): Tooltip text
    """
    def on_enter(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.configure(bg='#ffffe0', bd=1, relief='solid')
        
        label = tk.Label(tooltip, text=text, bg='#ffffe0', fg='#000000',
                        font=('Segoe UI', 9), wraplength=250)
        label.pack()
        
        # Position tooltip near mouse
        x = widget.winfo_rootx() + 25
        y = widget.winfo_rooty() + widget.winfo_height() + 5
        tooltip.geometry(f"+{x}+{y}")
        
        widget.tooltip = tooltip
        
    def on_leave(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            delattr(widget, 'tooltip')
    
    widget.bind('<Enter>', on_enter)
    widget.bind('<Leave>', on_leave)

def main():
    """Main application entry point with enhanced UI."""
    window = tk.Tk()
    window.title(APP_TITLE)
    window.configure(bg='#f8f9fa')
    
    # Set minimum window size and make resizable
    window.minsize(350, 250)
    window.resizable(True, False)
    
    # Center the window using the utility function
    center_window(window, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT + 50)

    # Add application icon if available
    try:
        window.iconbitmap(os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico'))
    except:
        pass  # Icon file not found, continue without it
    
    from wiiman.about_menu import add_about_menu
    add_about_menu(window)

    # Main content frame
    main_frame = tk.Frame(window, bg='#f8f9fa')
    main_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    # Header with application description
    header_label = tk.Label(
        main_frame,
        text="WiiU CDN File Processor",
        font=("Segoe UI", 16, "bold"),
        bg='#f8f9fa',
        fg='#2c3e50'
    )
    header_label.pack(pady=(10, 5))
    
    description_label = tk.Label(
        main_frame,
        text="Process WiiU CDN files for decryption",
        font=("Segoe UI", 10),
        bg='#f8f9fa',
        fg='#7f8c8d'
    )
    description_label.pack(pady=(0, 20))
    
    # Action selection label
    action_label = tk.Label(
        main_frame, 
        text="Choose what to process:", 
        font=DEFAULT_FONT,
        bg='#f8f9fa',
        fg='#34495e'
    )
    action_label.pack(pady=(0, 15))
    
    # Button frame for better layout
    button_frame = tk.Frame(main_frame, bg='#f8f9fa')
    button_frame.pack(pady=10)
    
    # Main action button with improved styling
    select_button = tk.Button(
        button_frame,
        text="📁 Select CDN Folder",
        width=BUTTON_WIDTH,
        height=2,
        command=lambda: dorun(window),
        font=("Segoe UI", 11, "bold"),
        bg='#3498db',
        fg='white',
        activebackground='#2980b9',
        activeforeground='white',
        relief='raised',
        bd=2,
        cursor='hand2'
    )
    select_button.pack(pady=5)
    
    # Add tooltip
    create_tooltip(
        select_button, 
        "Select a folder containing WiiU CDN files\nto process for decryption.\n\nKeyboard: Enter"
    )
    
    # Future archive support (disabled for now)
    archive_button = tk.Button(
        button_frame,
        text="📦 Select Archive File",
        width=BUTTON_WIDTH,
        command=lambda: show_info("Coming Soon", "Archive file support will be added in a future update.", parent=window),
        font=("Segoe UI", 10),
        bg='#95a5a6',
        fg='white',
        state='normal',
        cursor='hand2'
    )
    archive_button.pack(pady=5)
    create_tooltip(archive_button, "Archive file support\n(Coming in future update)")
    
    # Status bar at bottom
    status_frame = tk.Frame(window, bg='#ecf0f1', relief='sunken', bd=1)
    status_frame.pack(side='bottom', fill='x')
    
    status_label = tk.Label(
        status_frame,
        text="Ready - Press Esc to exit, F1 for help",
        font=("Segoe UI", 9),
        bg='#ecf0f1',
        fg='#7f8c8d',
        anchor='w'
    )
    status_label.pack(side='left', padx=5, pady=2)
    
    version_label = tk.Label(
        status_frame,
        text="v2.0",
        font=("Segoe UI", 9),
        bg='#ecf0f1',
        fg='#95a5a6',
        anchor='e'
    )
    version_label.pack(side='right', padx=5, pady=2)

    # Keyboard shortcuts
    window.bind("<Return>", lambda e: dorun(window))  # Enter key
    window.bind("<F1>", lambda e: show_about(window))  # F1 for help
    window.bind("<Escape>", lambda e: cancel_and_exit(window))
    window.bind("<Control-q>", lambda e: cancel_and_exit(window))
    window.mainloop()
    
# 🔧 Testable entry point
if __name__ == "__main__":
    main()
    