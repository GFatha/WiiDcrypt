import os
import re
import shutil
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from wiiman.rename import rename_tmd_file
from .ui_utils import get_root_window, ask_yes_no, show_warning, center_window

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
        response = ask_yes_no(
            "Use title.tmd?",
            "A title.tmd file was found.\nWould you like to use it?"
        )

        if response:
            return
        else:
            backup_tmd_file("r", cdn_folder, tmd_path)
            return "skip"
    else:
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
    return [f for f in os.listdir(cdn_folder) if re.fullmatch(r'tmd\.\d+', f)]

def prompt_choose_tmd_file(cdn_folder, options):
    """Display an enhanced dialog to choose from multiple TMD files.
    
    Args:
        cdn_folder (str): Path to the CDN folder
        options (list): List of TMD file options
        
    Returns:
        str: Selected TMD file name or None if cancelled
    """
    selected_value = None

    root = tk.Tk()
    root.title("Select TMD File")
    root.configure(bg='#f8f9fa')
    root.resizable(False, False)
    
    # Use centralized window centering
    center_window(root, 400, 300)

    # Main content frame
    main_frame = tk.Frame(root, bg='#f8f9fa')
    main_frame.pack(fill='both', expand=True, padx=20, pady=15)
    
    # Header
    header_label = tk.Label(
        main_frame,
        text="Multiple TMD Files Found",
        font=("Segoe UI", 14, "bold"),
        bg='#f8f9fa',
        fg='#2c3e50'
    )
    header_label.pack(pady=(0, 10))
    
    # Instructions
    instruction_label = tk.Label(
        main_frame,
        text="Please select which TMD file to use as title.tmd:",
        font=("Segoe UI", 10),
        bg='#f8f9fa',
        fg='#34495e'
    )
    instruction_label.pack(pady=(0, 15))

    # List frame with styling
    list_frame = tk.Frame(main_frame, bg='#f8f9fa')
    list_frame.pack(fill="both", expand=True, pady=(0, 15))

    listbox = tk.Listbox(
        list_frame, 
        selectmode=tk.SINGLE, 
        width=35, 
        height=6,
        font=("Consolas", 10),
        bg='white',
        fg='#2c3e50',
        selectbackground='#3498db',
        selectforeground='white',
        relief='solid',
        bd=1
    )
    scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for opt in options:
        listbox.insert(tk.END, opt)
    
    # Auto-select first item
    if options:
        listbox.selection_set(0)
        listbox.focus_set()

    def on_select():
        nonlocal selected_value
        sel = listbox.curselection()
        if sel:
            selected_value = options[sel[0]]
            root.destroy()
        else:
            show_warning(
                "No Selection", 
                "Please select a TMD file from the list before clicking 'Use Selected'.",
                parent=root
            )
    
    def on_double_click(event):
        """Handle double-click on listbox item"""
        on_select()
    
    def on_cancel():
        nonlocal selected_value
        selected_value = None
        root.destroy()
    
    # Handle window close (X button)
    root.protocol("WM_DELETE_WINDOW", on_cancel)
    
    # Bind double-click
    listbox.bind('<Double-Button-1>', on_double_click)
    
    # Keyboard shortcuts
    root.bind('<Return>', lambda e: on_select())
    root.bind('<Escape>', lambda e: on_cancel())

    # Button frame with improved styling
    button_frame = tk.Frame(main_frame, bg='#f8f9fa')
    button_frame.pack(pady=(0, 5))
    
    use_button = tk.Button(
        button_frame, 
        text="Use Selected", 
        command=on_select,
        font=("Segoe UI", 10, "bold"),
        bg='#27ae60',
        fg='white',
        activebackground='#229954',
        activeforeground='white',
        width=12,
        cursor='hand2'
    )
    use_button.pack(side="left", padx=(0, 10))
    
    cancel_button = tk.Button(
        button_frame, 
        text="Cancel", 
        command=on_cancel,
        font=("Segoe UI", 10),
        bg='#95a5a6',
        fg='white',
        activebackground='#7f8c8d',
        activeforeground='white',
        width=12,
        cursor='hand2'
    )
    cancel_button.pack(side="left")
    
    # Help text
    help_label = tk.Label(
        main_frame,
        text="Double-click an item or press Enter to select",
        font=("Segoe UI", 8),
        bg='#f8f9fa',
        fg='#7f8c8d'
    )
    help_label.pack(pady=(10, 0))

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
