"""
Logging system for WiiDcrypt application.

This module provides centralized logging functionality for debugging,
error tracking, and user support.
"""
import logging
import os
from datetime import datetime
from .config import APP_VERSION


class WiiDcryptLogger:
    """Centralized logging system for the application."""
    
    def __init__(self):
        self.logger = None
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup the application logger with file and console handlers."""
        self.logger = logging.getLogger('WiiDcrypt')
        self.logger.setLevel(logging.DEBUG)
        
        # Avoid duplicate handlers
        if self.logger.handlers:
            return
            
        # Create logs directory
        log_dir = os.path.join(os.path.expanduser('~'), '.wiidcrypt', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # File handler with rotation
        log_file = os.path.join(log_dir, f'wiidcrypt_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler (only warnings and errors)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Formatters
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s.%(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Log startup
        self.logger.info(f"WiiDcrypt v{APP_VERSION} started")
        self.logger.info(f"Log file: {log_file}")
    
    def debug(self, message, *args, **kwargs):
        """Log debug message."""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message, *args, **kwargs):
        """Log info message."""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        """Log warning message."""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        """Log error message."""
        self.logger.error(message, *args, **kwargs)
    
    def exception(self, message, *args, **kwargs):
        """Log exception with traceback."""
        self.logger.exception(message, *args, **kwargs)
    
    def log_operation(self, operation, path=None, details=None):
        """Log a user operation."""
        msg = f"Operation: {operation}"
        if path:
            msg += f" | Path: {path}"
        if details:
            msg += f" | Details: {details}"
        self.info(msg)
    
    def log_error_with_context(self, error, context=None, user_action=None):
        """Log error with additional context for support."""
        self.error(f"Error occurred: {error}")
        if context:
            self.error(f"Context: {context}")
        if user_action:
            self.error(f"User action: {user_action}")
    
    def get_log_directory(self):
        """Get the log directory path."""
        return os.path.join(os.path.expanduser('~'), '.wiidcrypt', 'logs')


# Global logger instance
_logger_instance = None

def get_logger():
    """Get the global logger instance."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = WiiDcryptLogger()
    return _logger_instance


# Convenience functions
def log_debug(message, *args, **kwargs):
    """Log debug message."""
    get_logger().debug(message, *args, **kwargs)

def log_info(message, *args, **kwargs):
    """Log info message."""
    get_logger().info(message, *args, **kwargs)

def log_warning(message, *args, **kwargs):
    """Log warning message."""
    get_logger().warning(message, *args, **kwargs)

def log_error(message, *args, **kwargs):
    """Log error message."""
    get_logger().error(message, *args, **kwargs)

def log_exception(message, *args, **kwargs):
    """Log exception with traceback."""
    get_logger().exception(message, *args, **kwargs)

def log_operation(operation, path=None, details=None):
    """Log a user operation."""
    get_logger().log_operation(operation, path, details)

def log_error_with_context(error, context=None, user_action=None):
    """Log error with context."""
    get_logger().log_error_with_context(error, context, user_action)
