import os
import re
import shutil
import tkinter as tk
from datetime import datetime

from wiiman.config import DEFAULT_WINDOW_HEIGHT, DEFAULT_WINDOW_WIDTH, MESSAGES
from wiiman.rename import rename_tmd_file
from wiiman.ui_utils import ask_yes_no, show_warning


def handle_tmd_logic(selected_path):
    tmd_result = check_for_title_tmd(selected_path)
    print("check_for_title_tmd result:", tmd_result)
    if tmd_result in ("skip", "not_found"):
        fb_result = fallback_tmd_logic(selected_path)
        print("fallback_tmd_logic result:", fb_result)
    return


def check_for_title_tmd(cdn_folder):
    """Check for existing title.tmd with proper resource management."""
    tmd_path = os.path.join(cdn_folder, "title.tmd")

    if os.path.exists(tmd_path):
        response = ask_yes_no("Use title.tmd?", MESSAGES["use_title_tmd"], parent=root)

        if response:
            return "valid"

        backup_tmd_file("r", cdn_folder, tmd_path)
        return "skip"

    return "not_found"


def backup_tmd_file(type, cdn_folder, tmd_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(tmd_path)
    backup_name = f"{filename}.bak_{timestamp}"
    backup_path = os.path.join(cdn_folder, backup_name)

    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    if type == "c":
        shutil.copy2(tmd_path, backup_path)
    elif type == "r":
        os.rename(tmd_path, backup_path)

    return backup_path


def get_tmd_alternates(cdn_folder):
    return [f for f in os.listdir(cdn_folder) if re.fullmatch(r"tmd\.\d+", f)]


def prompt_choose_tmd_file(cdn_folder, options):
    selected_value = None

    root = tk.Tk()
    root.title("Select tmd.X file")
    center_window(root, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)

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
        else:
            show_warning("No Selection", MESSAGES["no_selection_warning"], parent=root)

    def on_cancel():
        nonlocal selected_value
        selected_value = None
        root.destroy()

    # Handle window close (X button)
    root.protocol("WM_DELETE_WINDOW", on_cancel)

    # Button frame
    button_frame = tk.Frame(root)
    button_frame.pack(pady=(0, 10))

    tk.Button(button_frame, text="Use Selected", command=on_select).pack(
        side="left", padx=(0, 5)
    )
    tk.Button(button_frame, text="Cancel", command=on_cancel).pack(
        side="left", padx=(5, 0)
    )

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

        # Now handle the backup and rename operations after dialog returns
        src = os.path.join(cdn_folder, selected)
        print(f"[DEBUG] Selected file path: {src}")
        print(f"[DEBUG] Exists before rename? {os.path.exists(src)}")

        # Backup the selected tmd file before renaming
        backup_tmd_file("c", cdn_folder, src)

        # Use the rename_tmd_file function if available, otherwise do it manually
        try:
            rename_tmd_file(cdn_folder, selected)
            print(f"[DEBUG] Renamed {selected} to title.tmd using rename_tmd_file")
            return "replaced"
        except Exception as e:
            print(f"[ERROR] Failed to rename using rename_tmd_file: {e}")
            # Fallback to manual rename
            try:
                if os.path.exists(title_tmd_path):
                    os.remove(title_tmd_path)
                os.rename(src, title_tmd_path)
                print(f"[DEBUG] Manually renamed {src} to {title_tmd_path}")
                return "replaced"
            except Exception as e2:
                print(f"[ERROR] Manual rename also failed: {e2}")
                return "error"
    else:
        print("[DEBUG] No alternative tmd files found")
        return "no_alternates"
