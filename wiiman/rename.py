import os
from wiiman.validator import is_valid_cdn_file

def rename_extensionless_files(folder_path, new_extension='.app'):
    """
    Renames all extensionless files in the folder to have the given extension (default: .app).
    Only renames files that are 8-char hex and currently have no extension.
    Returns a list of (old_path, new_path) tuples for renamed files.
    """
    renamed = []
    for fname in os.listdir(folder_path):
        full_path = os.path.join(folder_path, fname)
        if os.path.isfile(full_path):
            name, ext = os.path.splitext(fname)
            if ext == '' and len(fname) == 8:
                try:
                    int(fname, 16)
                    new_name = fname + new_extension
                    new_path = os.path.join(folder_path, new_name)
                    os.rename(full_path, new_path)
                    renamed.append((full_path, new_path))
                except ValueError:
                    continue
    return