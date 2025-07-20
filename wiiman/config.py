"""
Configuration management for WiiDcrypt application.

This module centralizes all configuration constants and settings,
making them easy to modify and maintain.
"""

# Window settings
DEFAULT_WINDOW_WIDTH = 400
DEFAULT_WINDOW_HEIGHT = 200

# Dialog settings
TMD_DIALOG_WIDTH = 350
TMD_DIALOG_HEIGHT = 250

# File operation settings
MAX_FOLDER_VALIDATION_ATTEMPTS = 3
BACKUP_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# Archive file extensions
ARCHIVE_EXTENSIONS = ['.zip', '.rar', '.7z']

# CDN file extensions
CDN_FILE_EXTENSIONS = ['.app', '.tmd', '.tik', '.cert', '.h3']

# UI settings
DEFAULT_FONT = ("Segoe UI", 12)
BUTTON_WIDTH = 25
PADDING_SMALL = 5
PADDING_MEDIUM = 12
PADDING_LARGE = 25

# File patterns
HEX_FILENAME_LENGTH = 8
TMD_ALTERNATE_PATTERN = r'tmd\.\d+'

# Application metadata
APP_TITLE = " --  WiiU CDN Decryptor  --"
ABOUT_TEXT = "Lead Dev - GFatha"

# Messages
MESSAGES = {
    'operation_cancelled': "Operation Cancelled.",
    'operation_completed': "Operation completed successfully!",
    'folder_cancelled': "Operation cancelled — no folder was selected.",
    'folder_invalid': "This folder is empty or contains unsupported files.\nWould you like to try again?",
    'folder_too_many_attempts': "It appears you're having trouble selecting a valid folder.\nPlease try again later.",
    'title_tmd_found': "A title.tmd file was found.\nWould you like to use it?",
    'no_selection_warning': "Please select a file before clicking 'Use Selected'."
}

# Error messages for specific exceptions
ERROR_MESSAGES = {
    'file_not_found': "The specified file was not found.",
    'permission_denied': "Permission denied. Please check file permissions.",
    'invalid_hex': "Invalid hexadecimal filename format.",
    'rename_failed': "Failed to rename file.",
    'backup_failed': "Failed to create backup file."
}
