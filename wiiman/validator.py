import os
import tkinter as tk
from tkinter import filedialog
from .ui_utils import get_root_window, show_info, ask_question
from .config import (
    MAX_FOLDER_VALIDATION_ATTEMPTS,
    CDN_FILE_EXTENSIONS,
    HEX_FILENAME_LENGTH,
    MESSAGES
)
from .exceptions import InvalidCDNFolderError, InvalidHexFilenameError, UserCancelledError

def is_valid_cdn_file(filename, parent_folder):
    """Check if a file is a valid CDN file.
    
    Args:
        filename (str): Name of the file to check
        parent_folder (str): Path to the parent folder
        
    Returns:
        bool: True if file is a valid CDN file, False otherwise
    """
    filepath = os.path.join(parent_folder, filename)
    ext = os.path.splitext(filename)[1].lower()

    # ✅ Allow known CDN file types
    if ext in CDN_FILE_EXTENSIONS and os.path.isfile(filepath):
        return True

    # ✅ Accept alternate TMDs like tmd.0, tmd.123, etc.
    if filename.startswith("tmd.") and len(filename.split(".")) == 2 and os.path.isfile(filepath):
        return True

    # Valid no-extension files: 8-char hex like 00000001
    if ext == '' and os.path.isfile(filepath):
        if len(filename) == HEX_FILENAME_LENGTH:
            try:
                int(filename, 16)
                return True
            except ValueError:
                raise InvalidHexFilenameError(f"Invalid hexadecimal filename: {filename}")
        return False

    return False

# Folder validation helpers
def is_valid_cdn_folder(folder_path):
    """Check if a folder contains valid CDN files.
    
    Args:
        folder_path (str): Path to the folder to validate
        
    Returns:
        bool: True if folder contains at least one valid CDN file
        
    Raises:
        InvalidCDNFolderError: If folder is not a directory
    """
    if not os.path.isdir(folder_path):
        raise InvalidCDNFolderError(f"Path is not a directory: {folder_path}")
        
    try:
        for fname in os.listdir(folder_path):
            if is_valid_cdn_file(fname, folder_path):
                return True
    except InvalidHexFilenameError:
        # Continue checking other files if one has invalid hex format
        pass
    except OSError as e:
        raise InvalidCDNFolderError(f"Cannot access folder: {e}")
        
    return False

def select_and_validate_folder():
    """Select and validate a CDN folder with proper resource management.
    
    Returns:
        str: Path to selected valid folder, or None if cancelled
        
    Raises:
        UserCancelledError: If user cancels the operation
    """
    root = get_root_window()
    attempt_count = 0
    
    while attempt_count < MAX_FOLDER_VALIDATION_ATTEMPTS:
        selected = filedialog.askdirectory(
            title="Select Wii U CDN Folder",
            initialdir=os.getcwd(),
            parent=root
        )
        print(f"Selected folder: {selected}")
        
        if not selected:
            show_info(
                "Cancelled", 
                MESSAGES['folder_cancelled'],
                parent=root
            )
            return None
            
        try:
            if is_valid_cdn_folder(selected):
                return selected
        except InvalidCDNFolderError:
            pass  # Continue to retry logic
            
        attempt_count += 1
        if attempt_count < MAX_FOLDER_VALIDATION_ATTEMPTS:
            retry = ask_question(
                "Invalid Folder ❌",
                MESSAGES['folder_invalid'],
                parent=root
            )
            if retry != 'yes':
                show_info(
                    "Cancelled", 
                    MESSAGES['folder_cancelled'],
                    parent=root
                )
                return None
        else:
            show_info(
                "Too Many Attempts 🚫",
                MESSAGES['folder_too_many_attempts'],
                parent=root
            )
            return None
