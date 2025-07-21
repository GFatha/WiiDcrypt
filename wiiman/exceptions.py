"""
Custom exceptions for WiiDcrypt application.

This module defines specific exception classes for different error conditions
to enable more precise error handling and better user feedback.
"""


class WiiDcryptError(Exception):
    """Base exception for all WiiDcrypt-related errors."""
    pass


class ValidationError(WiiDcryptError):
    """Raised when file or folder validation fails."""
    pass


class FileOperationError(WiiDcryptError):
    """Raised when file operations (rename, copy, backup) fail."""
    pass


class InvalidCDNFolderError(ValidationError):
    """Raised when a selected folder doesn't contain valid CDN files."""
    pass


class InvalidHexFilenameError(ValidationError):
    """Raised when a filename is not valid hexadecimal format."""
    pass


class TMDFileError(FileOperationError):
    """Raised when TMD file operations fail."""
    pass


class BackupError(FileOperationError):
    """Raised when backup operations fail."""
    pass


class UserCancelledError(WiiDcryptError):
    """Raised when user cancels an operation."""
    pass


class ConfigurationError(WiiDcryptError):
    """Raised when configuration is invalid or missing."""
    pass
