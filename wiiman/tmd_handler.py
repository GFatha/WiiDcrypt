import os
import re
import shutil
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from wiiman.rename import rename_tmd_file
import logging

logging.basicConfig(level=logging.DEBUG)

def handle_tmd_logic(selected_path, mode="gui"):
    result = check_for_title_tmd(selected_path)
    logging.debug(f"check_for_title_tmd result: {result}")
    
    if result in ("skip", "not_found"):
        fb_result = fallback_tmd_logic(selected_path, mode)
        logging.debug(f"fallback_tmd_logic result: {fb_result}")

def check_for_title_tmd(cdn_folder):
    tmd_path = os.path.join(cdn_folder, "title.tmd")
    if os.path.exists(tmd_path):
        response = ask_user_use_title_tmd_gui()
        if response:
            return
        else:
            backup_tmd_file("r", cdn_folder, tmd_path)
            return "skip"
    return "not_found"

def ask_user_use_title_tmd_gui():
    try:
        root = tk.Tk()
        root.withdraw()
        response = messagebox.askyesno("Use title.tmd?", "A title.tmd file was found.\nWould you like to use it?")
        root.destroy()
        return response
    except tk.TclError as e:
        logging.warning(f"GUI unavailable: {e}")
        return False

def backup_tmd_file(mode, folder, path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{os.path.basename(path)}.bak_{timestamp}"
    backup_path = os.path.join(folder, backup_name)

    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    if mode == "c":
        shutil.copy2(path, backup_path)
    elif mode == "r":
        os.rename(path, backup_path)
    return backup_path

def get_tmd_alternates(folder):
    return [f for f in os.listdir(folder) if re.fullmatch(r'tmd\.\d+', f)]

def user_select_tmd_file(options, mode="gui"):
    if mode == "cli":
        print("Available tmd.X files:")
        for i, opt in enumerate(options):
            print(f"{i + 1}: {opt}")
        try:
            selection = int(input("Select a file number: ")) - 1
            return options[selection]
        except Exception:
            logging.warning("Invalid CLI input.")
            return None
    else:
        return prompt_choose_tmd_file_gui(options)

def prompt_choose_tmd_file_gui(options):
    selected_value = None

    try:
        root = tk.Tk()
        root.title("Select tmd.X file")
        root.geometry("350x250+200+200")  # You can adjust position as needed

        tk.Label(root, text="Select which tmd.X file to use as title.tmd:").pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=40, height=8)
        scrollbar = tk.Scrollbar(frame, command=listbox.yview)
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
                root.quit()  # ✔ close the mainloop, but let logic finish
            else:
                messagebox.showwarning("No Selection", "Please select a file first.")

        def on_cancel():
            nonlocal selected_value
            selected_value = None
            root.quit()

        root.protocol("WM_DELETE_WINDOW", on_cancel)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=(0, 10))
        tk.Button(button_frame, text="Use Selected", command=on_select).pack(side="left", padx=(0, 5))
        tk.Button(button_frame, text="Cancel", command=on_cancel).pack(side="left", padx=(5, 0))

        root.mainloop()
        root.destroy()  # ✅ must destroy after mainloop exits

    except Exception as e:
        logging.error(f"GUI selection failed: {e}")

    return selected_value

def safely_replace_file(src, dest, backup_mode):
    try:
        backup_tmd_file(backup_mode, os.path.dirname(src), src)
        if os.path.exists(dest):
            os.remove(dest)
        os.rename(src, dest)
        return True
    except Exception as e:
        logging.error(f"File replacement error: {e}")
        return False

def fallback_tmd_logic(folder, mode="gui"):
    title_tmd_path = os.path.join(folder, "title.tmd")
    alternates = get_tmd_alternates(folder)
    if not alternates:
        logging.debug("No tmd.X files found.")
        return "no_alternates"

    selected = alternates[0] if len(alternates) == 1 else user_select_tmd_file(alternates, mode)
    if not selected:
        logging.debug("User canceled or invalid input.")
        return "cancelled"

    src = os.path.join(folder, selected)

    # ✅ Always back up the selected tmd.X file
    backup_tmd_file("c", folder, src)

    try:
        # Preferred rename method
        rename_tmd_file(folder, selected)
        logging.debug(f"Renamed {selected} using rename_tmd_file")
        return "replaced"
    except Exception as e:
        logging.warning(f"rename_tmd_file failed: {e}")

    # Manual fallback
    try:
        if os.path.exists(title_tmd_path):
            os.remove(title_tmd_path)
        os.rename(src, title_tmd_path)
        logging.debug(f"Manually renamed {selected} to title.tmd")
        return "replaced"
    except Exception as e2:
        logging.error(f"Manual rename failed: {e2}")
        return "error"