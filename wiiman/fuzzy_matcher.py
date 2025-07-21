import csv

def match_title_id_exact(title_id_hex, csv_path):
    """
    Searches for a row in the given CSV where Title ID matches exactly.
    
    Args:
        title_id_hex (str): The Title ID to look for (case-insensitive).
        csv_path (str): Path to the CSV file containing title info.
    
    Returns:
        dict or None: Matching row as a dictionary, or None if not found.
    """
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("Title ID", "").strip().upper() == title_id_hex.strip().upper():
                    return row
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}")
    return None