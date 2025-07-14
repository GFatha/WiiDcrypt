import os
import tkinter as tk
from tkinter import filedialog, messagebox

MAX_ATTEMPTS = 3

def is_valid_cdn_file(filename, parent_folder):
    filepath = os.path.join(parent_folder, filename)
    ext = os.path.splitext(filename)[1].lower()

    # ✅ Allow known CDN file types
    if ext in ['.app', '.tmd', '.tik', '.cert', '.h3', ''] and os.path.isfile(filepath):
        return True

    # ✅ Accept alternate TMDs like tmd.0, tmd.123, etc.
    if filename.startswith("tmd.") and len(filename.split(".")) == 2 and os.path.isfile(filepath):
        return True

    return False

def validate_folder(path):
    entries = os.listdir(path)

    # ❌ Reject empty folder
    if not entries:
        return False

    has_valid_file = False

    for entry in entries:
        entry_path = os.path.join(path, entry)

        if os.path.isdir(entry_path):
            continue  # skip subfolders

        if is_valid_cdn_file(entry, path):
            has_valid_file = True
        else:
            return False  # contains unsupported file

    # ❌ Reject folder if no valid files were found
    return has_valid_file

def run_folder_validation():
    attempt_count = 0

    while attempt_count < MAX_ATTEMPTS:
        root = tk.Tk()
        root.withdraw()

        selected = filedialog.askdirectory(
            title="Select Wii U CDN Folder",
            initialdir=os.getcwd()
        )

        if not selected:
            messagebox.showinfo("Cancelled", "Operation cancelled — no folder was selected.")
            return None

        if validate_folder(selected):
            messagebox.showinfo("Folder Validated ✅", f"Valid Wii U CDN folder selected:\n{selected}")
            return selected
        else:
            attempt_count += 1
            if attempt_count < MAX_ATTEMPTS:
                retry = messagebox.askquestion(
                    "Invalid Folder ❌",
                    "This folder is empty or contains unsupported files.\nWould you like to try again?",
                    icon="warning"
                )
                if retry != 'yes':
                    messagebox.showinfo("Cancelled", "Operation cancelled — no valid folder was selected.")
                    return None
            else:
                messagebox.showinfo(
                    "Too Many Attempts 🚫",
                    "It appears you're having trouble selecting a valid folder.\nPlease try again later."
                )
                return None

# Run standalone for testing
if __name__ == "__main__":
    run_folder_validation()