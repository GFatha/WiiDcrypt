import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from wiiman.validator import select_and_validate_folder
from wiiman.rename import rename_extensionless_files


# Define the archive extensions globally for easy access
# This allows us to check if a file is an archive without hardcoding it everywhere          
ARCHIVE_EXTENSIONS = ['.zip', '.rar', '.7z']

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
        
def cancel_and_exit(window):
    """Cancel operation and exit application with confirmation."""
    messagebox.showinfo("Cancelled", "Operation Cancelled.", parent=window)
    window.destroy()
    exit()

def dorun(main_window=None):
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
    parent = main_window if main_window else _get_root_window()
    messagebox.showinfo("Complete", "Operation completed successfully!", parent=parent)
    
    if main_window:
        main_window.quit()
        main_window.destroy()

def main():
    window = tk.Tk()
    window.title(" --  WiiU CDN Decryptor  --")
    window_width = 400
    window_height = 200
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    from wiiman.about_menu import add_about_menu
    add_about_menu(window)

    tk.Label(window, text="Choose what to process:", font=("Segoe UI", 12)).pack(pady=(25, 25))
    tk.Button(window, text="📁 Select Folder", width=25, command=lambda: dorun(window)).pack(pady=12)
 #   tk.Button(window, text="📦 Select Archive File", width=25, command=handle_file_selection).pack(pady=5)

    window.bind("<Escape>", lambda e: cancel_and_exit(window))
    window.bind("<Control-q>", lambda e: cancel_and_exit(window))
    window.mainloop()
    
# 🔧 Testable entry point
if __name__ == "__main__":
    main()
    