import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from wiiman.validator import select_and_validate_folder
from wiiman.rename import rename_extensionless_files
from wiiman.ui_utils import show_about, show_info, center_window, get_root_window
from wiiman.config import (
    DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT,
    APP_TITLE, BUTTON_WIDTH, DEFAULT_FONT,
    PADDING_LARGE, PADDING_MEDIUM,
    MESSAGES
)
        
def cancel_and_exit(window):
    """Cancel operation and exit application with confirmation."""
    show_info("Cancelled", MESSAGES['operation_cancelled'], parent=window)
    window.destroy()
    exit()

def dorun(main_window=None):
    """Run the main decryption process.
    
    Args:
        main_window (tk.Tk, optional): Main window to close after completion
    """
    selected_path = select_and_validate_folder()
    if not selected_path:
        return
    
    from wiiman.rename_tmd_files import handle_tmd_logic

    rename_extensionless_files(selected_path)

    src = os.path.join(os.path.dirname(__file__), 'template', 'title.cert')
    dst = os.path.join(selected_path, 'title.cert')
    shutil.copy2(src, dst)
    
    handle_tmd_logic(selected_path)

    print("Operation completed.")
    
    # Show completion message and close main window
    parent = main_window if main_window else get_root_window()
    show_info("Complete", MESSAGES['operation_completed'], parent=parent)
    
    if main_window:
        main_window.quit()
        main_window.destroy()

def main():
    """Main application entry point."""
    window = tk.Tk()
    window.title(APP_TITLE)
    
    # Center the window using the utility function
    center_window(window, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)

    from wiiman.about_menu import add_about_menu
    add_about_menu(window)

    tk.Label(window, text="Choose what to process:", font=DEFAULT_FONT).pack(pady=(PADDING_LARGE, PADDING_LARGE))
    tk.Button(window, text="📁 Select Folder", width=BUTTON_WIDTH, command=lambda: dorun(window)).pack(pady=PADDING_MEDIUM)
 #   tk.Button(window, text="📦 Select Archive File", width=BUTTON_WIDTH, command=handle_file_selection).pack(pady=PADDING_SMALL)

    window.bind("<Escape>", lambda e: cancel_and_exit(window))
    window.bind("<Control-q>", lambda e: cancel_and_exit(window))
    window.mainloop()
    
# 🔧 Testable entry point
if __name__ == "__main__":
    main()
    