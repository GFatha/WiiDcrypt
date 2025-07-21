import os
import tkinter as tk
from tkinter import filedialog, messagebox

MAX_ATTEMPTS = 3

def _get_root_window():
    """Get or create a single root window for dialogs."""
    # Check if there's already a root window
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

def is_valid_cdn_file(filename, parent_folder):
    filepath = os.path.join(parent_folder, filename)
    ext = os.path.splitext(filename)[1].lower()

    # ✅ Allow known CDN file types
    if ext in ['.app', '.tmd', '.tik', '.cert', '.h3'] and os.path.isfile(filepath):
        return True

    # ✅ Accept alternate TMDs like tmd.0, tmd.123, etc.
    if filename.startswith("tmd.") and len(filename.split(".")) == 2 and os.path.isfile(filepath):
        return True

    # Valid no-extension files: 8-char hex like 00000001
    if ext == '' and os.path.isfile(filepath):
        if len(filename) == 8:
            try:
                int(filename, 16)
                return True
            except ValueError:
                return False
        return False

    return False

# Folder validation helpers
def is_valid_cdn_folder(folder_path):
    # A folder is valid if it contains at least one valid CDN file
    if not os.path.isdir(folder_path):
        return False
    for fname in os.listdir(folder_path):
        if is_valid_cdn_file(fname, folder_path):
            return True
    return False

def select_and_validate_folder():
    """Select and validate a CDN folder with proper resource management."""
    root = _get_root_window()
    attempt_count = 0
    
    while attempt_count < MAX_ATTEMPTS:
        selected = filedialog.askdirectory(
            title="Select Wii U CDN Folder",
            initialdir=os.getcwd(),
            parent=root
        )
        print(f"Selected folder: {selected}")
        
        if not selected:
            messagebox.showinfo(
                "Cancelled", 
                "Operation cancelled — no folder was selected.",
                parent=root
            )
            return None
            
        if is_valid_cdn_folder(selected):
            return selected
        else:
            attempt_count += 1
            if attempt_count < MAX_ATTEMPTS:
                retry = messagebox.askquestion(
                    "Invalid Folder ❌",
                    "This folder is empty or contains unsupported files.\nWould you like to try again?",
                    icon="warning",
                    parent=root
                )
                if retry != 'yes':
                    messagebox.showinfo(
                        "Cancelled", 
                        "Operation cancelled — no valid folder was selected.",
                        parent=root
                    )
                    return None
            else:
                messagebox.showinfo(
                    "Too Many Attempts 🚫",
                    "It appears you're having trouble selecting a valid folder.\nPlease try again later.",
                    parent=root
                )
                return None
