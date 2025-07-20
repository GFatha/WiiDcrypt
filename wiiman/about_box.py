"""About dialog module - DEPRECATED.

This module is deprecated and maintained only for backward compatibility.
Use wiiman.ui_utils.show_about() instead.
"""
from .ui_utils import show_about  # Re-export for backward compatibility

# Keep this import for any legacy code that might import directly
__all__ = ['show_about']
