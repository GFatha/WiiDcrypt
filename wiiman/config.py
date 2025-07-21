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

# Color scheme
COLORS = {
    'primary': '#3498db',
    'primary_dark': '#2980b9',
    'success': '#27ae60',
    'success_dark': '#229954',
    'secondary': '#95a5a6',
    'secondary_dark': '#7f8c8d',
    'background': '#f8f9fa',
    'text_primary': '#2c3e50',
    'text_secondary': '#34495e',
    'text_muted': '#7f8c8d',
    'text_light': '#95a5a6',
    'status_bar': '#ecf0f1',
    'tooltip': '#ffffe0'
}

# Progress dialog settings
PROGRESS_DIALOG_WIDTH = 450
PROGRESS_DIALOG_HEIGHT = 180
PROGRESS_UPDATE_DELAY = 0.1  # seconds

# Tooltip settings
TOOLTIP_DELAY = 800  # milliseconds
TOOLTIP_WRAP_LENGTH = 250

# Application info
APP_VERSION = "2.0"
APP_COPYRIGHT = "© 2025 WiiDcrypt Project"

# Messages
MESSAGES = {
    'operation_cancelled': "Operation Cancelled.",
    'operation_completed': "Operation completed successfully!",
    'folder_cancelled': "Operation cancelled — no folder was selected.",
    'folder_invalid': "This folder is empty or contains unsupported files.\nWould you like to try again?",
    'folder_too_many_attempts': "It appears you're having trouble selecting a valid folder.\nPlease try again later.",
    'title_tmd_found': "A title.tmd file was found.\nWould you like to use it?",
    'no_selection_warning': "Please select a file before clicking 'Use Selected'.",
    'confirm_exit': "Are you sure you want to exit WiiU CDN Decryptor?",
    'process_another': "Would you like to process another folder?",
    'template_missing': "Warning: title.cert template not found",
    'archive_coming_soon': "Archive file support will be added in a future update."
}

# Error messages for specific exceptions
ERROR_MESSAGES = {
    'file_not_found': "The specified file was not found.",
    'permission_denied': "Permission denied. Please check file permissions.",
    'invalid_hex': "Invalid hexadecimal filename format.",
    'rename_failed': "Failed to rename file.",
    'backup_failed': "Failed to create backup file."
}
