import struct
import os

def read_tmd_title_id(tmd_path):
    if not os.path.exists(tmd_path):
        raise FileNotFoundError("title.tmd not found at specified path.")

    with open(tmd_path, "rb") as f:
        f.seek(0x18C)  # Title ID offset in TMD (14th byte of issuer section)
        title_id_raw = f.read(8)  # Title ID is 8 bytes
        title_id_hex = ''.join(f"{b:02X}" for b in title_id_raw)
        return title_id_hex