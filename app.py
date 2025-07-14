import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from wiiman.folder_validator import select_and_validate_folder
from wiiman.rename import rename_extensionless_files

ARCHIVE_EXTENSIONS = ['.zip', '.rar', '.7z']

def cancel_and_exit(window):
    messagebox.showinfo("Cancelled", "Operation Cancelled.")
    window.destroy()
    exit()

def dorun():
    selected_path = select_and_validate_folder()
    if not selected_path:
        return
    
    rename_extensionless_files(selected_path)

    src = os.path.join(os.path.dirname(__file__), 'template', 'title.cert')
    dst = os.path.join(selected_path, 'title.cert')
    shutil.copy2(src, dst)
    
    
    print("Operation completed.")

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

    tk.Label(window, text="Choose what to process:", font=("Segoe UI", 12)).pack(pady=12)
    tk.Button(window, text="📁 Select Folder", width=25, command=dorun).pack(pady=5)
 #   tk.Button(window, text="📦 Select Archive File", width=25, command=handle_file_selection).pack(pady=5)

    window.bind("<Escape>", lambda e: cancel_and_exit())
    window.bind("<Control-q>", lambda e: cancel_and_exit())
    window.mainloop()
    # selected_path = start_input_selector()
    # print(f"Selected path: {selected_path}")
    # if selected_path:
    #     # rename extensionless files in folder
    #     renamed_files = rename_extensionless_files(selected_path)
    #     return selected_path
    # else:
    #     print("No valid folder selected.")
    #     return None

# 🔧 Testable entry point
if __name__ == "__main__":
    main()
    