import tkinter as tk
from tkinter import filedialog, messagebox
import os
from folder_validator import validate_folder

ARCHIVE_EXTENSIONS = ['.zip', '.rar', '.7z']

def start_input_selector():
    selected_path_holder = [None]
    retry_count = [0]  # 📌 track failed attempts

    def handle_folder_selection():
        folder = filedialog.askdirectory(
            title="Select Wii U CDN Folder",
            initialdir=os.getcwd()
        )
        if folder:
            if validate_folder(folder):
                selected_path_holder[0] = folder
                messagebox.showinfo("Success ✅", f"Valid folder selected:\n{folder}")
                window.destroy()
            else:
                retry_count[0] += 1
                if retry_count[0] >= 3:
                    messagebox.showinfo("Too Many Attempts 🚫", "I'm Sorry A valid WiiU CDN Folder must be selected.")
                    window.destroy()
                else:
                    messagebox.showerror("Invalid Folder ❌", "This folder is either empty or contains unsupported files.\nPlease try again.")

    def handle_file_selection():
        file = filedialog.askopenfilename(
            title="Select Archive File (.zip, .rar, .7z)",
            filetypes=[("Archive Files", "*.zip *.rar *.7z"), ("All Files", "*.*")]
        )
        if file:
            ext = os.path.splitext(file)[1].lower()
            if ext in ARCHIVE_EXTENSIONS:
                selected_path_holder[0] = file
                messagebox.showinfo("Success ✅", f"Selected archive file:\n{file}")
                window.destroy()
            else:
                retry_count[0] += 1
                if retry_count[0] >= 3:
                    messagebox.showinfo("Too Many Attempts 🚫", "You’ve Reached the Maximum Number of Retries.")
                    window.destroy()
                else:
                    messagebox.showerror("Invalid File ❌", "Unsupported Archive File.\nPlease Try Again.")

    def cancel_and_exit():
        messagebox.showinfo("Cancelled", "Operation Cancelled.")
        window.destroy()
        exit()

    window = tk.Tk()
    window.title("Choose Input Type")
    window_width = 400
    window_height = 200
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tk.Label(window, text="Choose what to process:", font=("Segoe UI", 12)).pack(pady=12)
    tk.Button(window, text="📁 Select Folder", width=25, command=handle_folder_selection).pack(pady=5)
    tk.Button(window, text="📦 Select Archive File", width=25, command=handle_file_selection).pack(pady=5)
    tk.Button(window, text="❌ Cancel", width=25, command=cancel_and_exit).pack(pady=10)

    window.bind("<Escape>", lambda e: cancel_and_exit())
    window.bind("<Control-q>", lambda e: cancel_and_exit())
    window.mainloop()

    return selected_path_holder[0]

# 🔧 Testable entry point
if __name__ == "__main__":
    result = start_input_selector()
    if result:
        print("Selected path:", result)
