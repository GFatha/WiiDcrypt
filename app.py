import logging
import os
import shutil
import tkinter as tk

from wiiman.about_menu import add_about_menu
from wiiman.config import (
    APP_TITLE, BUTTON_WIDTH, DEFAULT_FONT,
    DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, 
    MESSAGES, PADDING_LARGE, PADDING_MEDIUM,
    COLORS, APP_VERSION, PROGRESS_DIALOG_WIDTH, PROGRESS_DIALOG_HEIGHT
)

from wiiman.decrypt_utils import generate_fake_tik
from wiiman.match_title_id import match_title_id_exact
from wiiman.rename import rename_extensionless_files
from wiiman.tmd_handler import handle_tmd_logic
from wiiman.tmd_parser import read_tmd_title_id
from wiiman.ui_utils import show_error, show_info, show_warning, center_window, get_root_window, show_about
from wiiman.validator import select_and_validate_folder

# 📋 Logging setup
logging.basicConfig(level=logging.DEBUG)


def dorun(main_window=None):
    from wiiman.progress_dialog import ProgressDialog

    selected_path = select_and_validate_folder()
    if not selected_path:
        return

    logging.info(MESSAGES["selected_folder"].format(selected_path=selected_path))

    # Create progress dialog
    progress = ProgressDialog(
        parent=main_window,
        title="Processing CDN Files",
        width=PROGRESS_DIALOG_WIDTH,
        height=PROGRESS_DIALOG_HEIGHT
    )

    try:
        # Step 1: Rename extensionless files
        progress.set_status("Renaming extensionless files...")
        progress.set_details(f"Processing folder: {os.path.basename(selected_path)}")
        progress.set_progress(20)

        rename_extensionless_files(selected_path)

        # Step 2: Handle title.tmd and fallback logic
        progress.set_status("Processing TMD files...")
        progress.set_details("Checking and processing title.tmd files")
        progress.set_progress(40)

        handle_tmd_logic(selected_path)

        # Step 3: Parse Title ID from title.tmd
        progress.set_status("Copying certificate template...")
        progress.set_details("Adding title.cert file")
        progress.set_progress(60) 

        try:
            tmd_path = os.path.join(selected_path, "title.tmd")

            title_id = read_tmd_title_id(tmd_path)
            logging.info(MESSAGES["extracted_title_id"].format(title_id=title_id))

            wiiman_dir = os.path.abspath(os.path.dirname(__file__))  # safer root
            csv_path = os.path.join(wiiman_dir, "wiiman", "wiiu_titlekeys.csv")

            matched = match_title_id_exact(title_id, csv_path)
            if matched:
                show_info(
                    "🎯 Match Found",
                    MESSAGES["game_info"].format(
                        matched_name=matched["Name"],
                        matched_title_id=matched["Title ID"],
                        matched_title_key=matched["Title Key"],
                    ),
                    parent=main_window,
                )
                logging.info(f"🎮 Game Name: {matched['Name']}")
                logging.info(f"🆔 Title ID: {matched['Title ID']}")
                logging.info(f"🔐 Title Key: {matched['Title Key']}")

                class SimpleUI:
                    def update(self, msg):
                        logging.info(msg)

                generate_fake_tik(
                    title_id=matched["Title ID"],
                    title_key=matched["Title Key"],
                    output_path=selected_path,
                    ui=SimpleUI(),
                )
            else:
                show_warning(
                    "Match Failed",
                    MESSAGES["match_failed"].format(title_id=title_id),
                    parent=main_window,
                )
                return

        except Exception as e:
            show_error("TMD Parsing Error", str(e), parent=main_window)
            return
        
        # Step 4: Parse Title ID from title.tmd
        progress.set_status("Decrypting...")
        progress.set_details("Decrypting file")
        progress.set_progress(80) 

        from wiiman.decrypt_utils import run_cdecrypt

        # 🔓 Decrypt into a sibling folder named after the game
        game_name = matched["Name"].replace(":", "").replace("/", "-").strip()  # Sanitized
        parent_dir = os.path.dirname(selected_path)
        output_dir = os.path.join(parent_dir, game_name)

        os.makedirs(output_dir, exist_ok=True)

        class SimpleUI:
            def update(self, msg):
                logging.info(msg)

        decryptor_path = os.path.join(os.path.dirname(__file__), "wiiman", "cdecrypt.exe")

        run_cdecrypt(decryptor_path, selected_path, output_dir, SimpleUI())

        # Step 5: Copy title.cert template
        progress.set_status("Copying certificate template...")
        progress.set_details("Adding title.cert file")
        progress.set_progress(95)

        src = os.path.join(os.path.dirname(__file__), "template", "title.cert")
        dst = os.path.join(selected_path, "title.cert")
        if os.path.exists(src):
            shutil.copy2(src, dst)
        else:
            # Template file missing - show warning but continue
            progress.set_details("Warning: title.cert template not found")

        # Brief delay to show completion
        import time
        time.sleep(0.5)

    except Exception as e:
        progress.set_status("Error occurred")
        progress.set_details(str(e))
        show_info("Error", f"An error occurred during processing:\n{str(e)}", parent=main_window)
    finally:
        progress.close()

    # Final message
    show_info("Complete", MESSAGES["operation_completed"], parent=main_window)

    # Show completion message
    parent = main_window if main_window else get_root_window()
    
    show_info("Complete", MESSAGES['operation_completed'], parent=parent)
    if main_window:
        # Ask if user wants to process another folder
        from wiiman.ui_utils import ask_yes_no
        if not ask_yes_no(
            "Process Another?", 
            "Would you like to process another folder?", 
            parent=main_window
        ):
            main_window.quit()
            main_window.destroy()

def create_tooltip(widget, text):
    """Create a tooltip for a widget.
    
    Args:
        widget (tk.Widget): Widget to add tooltip to
        text (str): Tooltip text
    """
    def on_enter(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.configure(bg='#ffffe0', bd=1, relief='solid')

        label = tk.Label(tooltip, text=text, bg='#ffffe0', fg='#000000',
                        font=('Segoe UI', 9), wraplength=250)
        label.pack()

        # Position tooltip near mouse
        x = widget.winfo_rootx() + 25
        y = widget.winfo_rooty() + widget.winfo_height() + 5
        tooltip.geometry(f"+{x}+{y}")

        widget.tooltip = tooltip

    def on_leave(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            delattr(widget, 'tooltip')

    widget.bind('<Enter>', on_enter)
    widget.bind('<Leave>', on_leave)

def main():
    window = tk.Tk()
    window.title(APP_TITLE)
    window.configure(bg='#f8f9fa')
    
    # Set minimum window size and make resizable
    window.minsize(350, 250)
    window.resizable(True, False)

    center_window(window, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT + 50)  # Add some extra height for buttons
    
    add_about_menu(window)  # ✅ Adds Help > About to menu bar

    # Main content frame
    main_frame = tk.Frame(window, bg='#f8f9fa')
    main_frame.pack(fill='both', expand=True, padx=20, pady=10)

    # Header with application description
    header_label = tk.Label(
        main_frame,
        text="WiiU CDN File Processor",
        font=("Segoe UI", 16, "bold"),
        bg='#f8f9fa',
        fg='#2c3e50'
    )
    header_label.pack(pady=(10, 5))

    description_label = tk.Label(
        main_frame,
        text="Process WiiU CDN files for decryption",
        font=("Segoe UI", 10),
        bg='#f8f9fa',
        fg='#7f8c8d'
    )
    description_label.pack(pady=(0, 20))

    # Action selection label
    action_label = tk.Label(
        main_frame, 
        text="Choose what to process:", 
        font=DEFAULT_FONT,
        bg='#f8f9fa',
        fg='#34495e'
    )
    action_label.pack(pady=(0, 15))

    # Button frame for better layout
    button_frame = tk.Frame(main_frame, bg='#f8f9fa')
    button_frame.pack(pady=10)

    # Main action button with improved styling
    select_button = tk.Button(
        button_frame,
        text="📁 Select CDN Folder",
        width=BUTTON_WIDTH,
        height=2,
        command=lambda: dorun(window),
        font=("Segoe UI", 11, "bold"),
        bg='#3498db',
        fg='white',
        activebackground='#2980b9',
        activeforeground='white',
        relief='raised',
        bd=2,
        cursor='hand2'
    )
    select_button.pack(pady=5)

    # Add tooltip
    create_tooltip(
        select_button, 
        "Select a folder containing WiiU CDN files\nto process for decryption.\n\nKeyboard: Enter"
    )

    # Future archive support (disabled for now)
    archive_button = tk.Button(
        button_frame,
        text="📦 Select Archive File",
        width=BUTTON_WIDTH,
        command=lambda: show_info("Coming Soon", "Archive file support will be added in a future update.", parent=window),
        font=("Segoe UI", 10),
        bg='#95a5a6',
        fg='white',
        state='normal',
        cursor='hand2'
    )
    archive_button.pack(pady=5)
    create_tooltip(archive_button, "Archive file support\n(Coming in future update)")

    # Status bar at bottom
    status_frame = tk.Frame(window, bg='#ecf0f1', relief='sunken', bd=1)
    status_frame.pack(side='bottom', fill='x')

    status_label = tk.Label(
        status_frame,
        text="Ready - Press Esc to exit, F1 for help",
        font=("Segoe UI", 9),
        bg='#ecf0f1',
        fg='#7f8c8d',
        anchor='w'
    )
    status_label.pack(side='left', padx=5, pady=2)

    version_label = tk.Label(
        status_frame,
        text="v2.0",
        font=("Segoe UI", 9),
        bg='#ecf0f1',
        fg='#95a5a6',
        anchor='e'
    )
    version_label.pack(side='right', padx=5, pady=2)

    # tk.Label(window, text="Select folder to process:", font=(DEFAULT_FONT)).pack(
    #     pady=(PADDING_LARGE, PADDING_LARGE)
    # )
    # tk.Button(
    #     window, text="📁 Select Folder", width=BUTTON_WIDTH, command=lambda: dorun(window)
    # ).pack(pady=PADDING_MEDIUM)

    # Keyboard shortcuts
    window.bind("<Return>", lambda e: dorun(window))  # Enter key
    window.bind("<F1>", lambda e: show_about(window))  # F1 for help

    window.mainloop()


if __name__ == "__main__":
    main()
