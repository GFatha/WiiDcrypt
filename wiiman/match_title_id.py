import csv
import os
import logging

def match_title_id_exact(title_id_hex, csv_path):
    """
    Searches for a row in the given CSV where Title ID matches exactly.
    Handles BOMs and fuzzy header matching.

    Args:
        title_id_hex (str): Title ID to match.
        csv_path (str): Path to CSV file.

    Returns:
        dict or None: Matching row with normalized keys, or None.
    """
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # 🔍 Resolve Title ID column with BOM-safe logic
            title_id_key = next(
                (key for key in reader.fieldnames if "TITLE ID" in key.upper()),
                None
            )

            if not title_id_key:
                logging.warning("Title ID column not found in CSV headers.")
                return None

            logging.debug(f"Using Title ID column: {title_id_key}")

            for row in reader:
                csv_id = row.get(title_id_key, "").strip().upper()
                if csv_id == title_id_hex.strip().upper():
                    logging.info(f"✅ Match found for Title ID: {csv_id}")

                    # 🧠 Dynamically resolve name key and add normalized data
                    name_key = next((k for k in row.keys() if "NAME" in k.upper()), None)
                    title_key_key = next((k for k in row.keys() if "TITLE KEY" in k.upper()), None)

                    return {
                        "Title ID": csv_id,
                        "Title Key": row.get(title_key_key, "Unknown"),
                        "Name": row.get(name_key, "Unknown")
                    }

    except Exception as e:
        logging.error(f"[ERROR] Failed to read CSV: {e}")

    return None