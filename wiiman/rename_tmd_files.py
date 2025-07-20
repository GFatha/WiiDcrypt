import os
import re
import shutil
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from wiiman.rename import rename_tmd_file

def handle_tmd_logic(selected_path):
    tmd_result = check_for_title_tmd(selected_path)
    print("check_for_title_tmd result:", tmd_result)
    if tmd_result in ("skip", "not_found"):
        fb_result = fallback_tmd_logic(selected_path)
        print("fallback_tmd_logic result:", fb_result)

def check_for_title_tmd(cdn_folder):
    tmd_path = os.path.join(cdn_folder, "title.tmd")

    if os.path.exists(tmd_path):
        root = tk.Tk()
        root.withdraw()
        response = messagebox.askyesno("Use title.tmd?",
            "A title.tmd file was found.\nWould you like to use it?")
        root.destroy()

        if response:
            return
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(cdn_folder, f"title.tmd.bak_{timestamp}")
            os.rename(tmd_path, backup_path)
            return "skip"
    else:
        return "not_found"

def get_tmd_alternates(cdn_folder):
    return [f for f in os.listdir(cdn_folder) if re.fullmatch(r'tmd\.\d+', f)]

def prompt_choose_tmd_file(cdn_folder, options):
    selected_value = None

    root = tk.Tk()
    root.title("Select tmd.X file")
    width, height = 350, 250
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw // 2) - (width // 2)
    y = (sh // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    tk.Label(root, text="Select which tmd.X file to use as title.tmd:").pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=40, height=8)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for opt in options:
        listbox.insert(tk.END, opt)

    def on_select():
        nonlocal selected_value
        sel = listbox.curselection()
        if sel:
            selected_value = options[sel[0]]
            root.destroy()
            rename_tmd_file(cdn_folder, selected_value)

        else:
            messagebox.showwarning("No Selection", "Please select a file before clicking 'Use Selected'.")

    button = tk.Button(root, text="Use Selected", command=on_select)
    button.pack(pady=(0, 10))



    root.mainloop()
    return selected_value

def fallback_tmd_logic(cdn_folder):
    title_tmd_path = os.path.join(cdn_folder, "title.tmd")
    has_title = os.path.exists(title_tmd_path)
    alternates = get_tmd_alternates(cdn_folder)

    if alternates:
        if len(alternates) == 1:
            selected = alternates[0]
        else:
            selected = prompt_choose_tmd_file(cdn_folder, alternates)
            print(f"[DEBUG] User selected: {selected}")
            if not selected:
                print("[DEBUG] User cancelled selection or closed dialog.")
                return "cancelled"

        src = os.path.join(cdn_folder, selected)
        print(f"[DEBUG] Selected file path: {src}")
        print(f"[DEBUG] Exists before rename? {os.path.exists(src)}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(cdn_folder, f"{selected}.bak_{timestamp}")
        shutil.copy2(src, backup_path)

        if os.path.exists(title_tmd_path):
            os.remove(title_tmd_path)

        try:
            os.rename(src, title_tmd_path)
            print(f"[DEBUG] Renamed {src} to {title_tmd_path}")
            return "replaced"
        except Exception as e:
            print(f"[ERROR] Failed to rename {src} to {title_tmd_path}: {e}")
            return "error"

    elif has_title:
        root = tk.Tk()
        root.withdraw()
        response = messagebox.askyesno("Fallback to title.tmd",
            "No alternate tmd.X files were found.\n"
            "If the existing title.tmd is not used, decryption is not possible.\n"
            "Do you want to use the existing title.tmd?")
        root.destroy()

        if response:
            return "fallback"
        else:
            messagebox.showinfo("Cancelled",
                "Operation cancelled — no usable title.tmd available.\n"
                "Decryption cannot proceed.")
            return "cancelled"
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Fatal Error",
            "No valid title.tmd is available.\n"
            "Neither an original title.tmd nor alternate tmd.X file was found.\n"
            "Operation cancelled — decryption cannot continue.")
        root.destroy()
        return "cancelled"