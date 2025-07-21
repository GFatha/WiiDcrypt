import logging
import os
import shutil
import tkinter as tk

from wiiman.about_menu import add_about_menu
from wiiman.config import MESSAGES
from wiiman.decrypt_utils import generate_fake_tik
from wiiman.match_title_id import match_title_id_exact
from wiiman.rename import rename_extensionless_files
from wiiman.tmd_handler import handle_tmd_logic
from wiiman.tmd_parser import read_tmd_title_id
from wiiman.ui_utils import show_error, show_info, show_warning
from wiiman.validator import select_and_validate_folder

# 📋 Logging setup
logging.basicConfig(level=logging.DEBUG)


def dorun(window=None):
    selected_path = select_and_validate_folder()
    if not selected_path:
        return

    logging.info(MESSAGES["selected_folder"].format(selected_path=selected_path))

    # Step 1: Rename extensionless files
    rename_extensionless_files(selected_path)

    # Step 2: Handle title.tmd and fallback logic
    handle_tmd_logic(selected_path)

    # Step 3: Parse Title ID from title.tmd
    tmd_path = os.path.join(selected_path, "title.tmd")

    try:
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
                parent=window,
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
                parent=window,
            )
            return

    except Exception as e:
        show_error("TMD Parsing Error", str(e), parent=window)
        return

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
    src = os.path.join(os.path.dirname(__file__), "template", "title.cert")
    dst = os.path.join(selected_path, "title.cert")
    shutil.copy2(src, dst)

    # Final message
    show_info("Complete", MESSAGES["operation_completed"], parent=window)
    if window:
        window.quit()
        window.destroy()


def main():
    window = tk.Tk()
    window.title("🧩 WiiU CDN Processor")
    window.geometry("400x180")

    add_about_menu(window)  # ✅ Adds Help > About to menu bar

    tk.Label(window, text="Select folder to process:", font=("Segoe UI", 12)).pack(
        pady=20
    )
    tk.Button(
        window, text="📁 Select Folder", width=25, command=lambda: dorun(window)
    ).pack(pady=10)
    window.mainloop()


if __name__ == "__main__":
    main()
