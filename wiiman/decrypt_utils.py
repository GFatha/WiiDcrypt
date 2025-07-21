# decrypt_utils.py
import os
import shutil
import subprocess

def generate_fake_tik(title_id, title_key, output_path, ui):
    """
    Generates a minimal fake .tik using Title ID and Key.

    Args:
        title_id (str): 16-char hex Title ID
        title_key (str): 32-char hex Title Key
        output_path (str): Folder to write 'title.tik'
        ui: UI object for feedback (can be dummy if not using)
    """
    try:
        # 📦 Build binary structure
        title_id_bytes = bytes.fromhex(title_id)
        title_key_bytes = bytes.fromhex(title_key)

        if len(title_id_bytes) != 8 or len(title_key_bytes) != 16:
            raise ValueError("Invalid Title ID or Key length.")

        # ⚙️ Create minimal ticket
        tik = bytearray(0x2A4)  # Base size of .tik
        tik[0x01DC:0x01DC+8] = title_id_bytes      # Title ID
        tik[0x01BF:0x01BF+16] = title_key_bytes    # Title Key

        # 💾 Write to file
        tik_path = os.path.join(output_path, "title.tik")
        with open(tik_path, "wb") as f:
            f.write(tik)

        ui.update("✅ Generated title.tik")

    except Exception as e:
        ui.update(f"[ERROR] Failed to generate title.tik: {e}")


def copy_cert(cert_file, folder_path, ui):
    shutil.copy(cert_file, os.path.join(folder_path, "title.cert"))
    ui.update("Copied title.cert")

def run_cdecrypt(decryptor, folder_path, output_folder, ui):
    import subprocess

    try:
        if not os.path.exists(decryptor):
            raise FileNotFoundError("cddecrypt.exe not found")

        tik = os.path.join(folder_path, "title.tik")
        tmd = os.path.join(folder_path, "title.tmd")

        if not os.path.exists(tik) or not os.path.exists(tmd):
            raise FileNotFoundError("Required .tik or .tmd file missing")

        cmd = [decryptor, folder_path, tmd, tik]
        ui.update("🔓 Running cddecrypt...")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            ui.update("✅ Decryption complete")

            # 📁 Only move decrypted folders
            moved_dirs = 0
            for folder_name in ("code", "content", "meta"):
                src = os.path.join(folder_path, folder_name)
                dst = os.path.join(output_folder, folder_name)
                if os.path.isdir(src):
                    shutil.move(src, dst)
                    moved_dirs += 1

            ui.update(f"📦 Moved {moved_dirs} decrypted folder(s) to: {output_folder}")

        else:
            ui.update("❌ Decryption failed")
            logging.error(result.stderr)

    except Exception as e:
        ui.update(f"[ERROR] cddecrypt execution failed: {e}")
