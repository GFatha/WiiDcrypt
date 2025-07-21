"""
Progress dialog utility for WiiDcrypt operations.

This module provides a progress dialog to give users visual feedback
during long-running operations.
"""
import tkinter as tk
from tkinter import ttk
from .ui_utils import center_window
from .config import PADDING_MEDIUM, DEFAULT_FONT


class ProgressDialog:
    """A modal progress dialog with progress bar and status text."""
    
    def __init__(self, parent=None, title="Processing...", width=400, height=150):
        """Initialize the progress dialog.
        
        Args:
            parent (tk.Widget, optional): Parent window
            title (str): Dialog title
            width (int): Dialog width in pixels
            height (int): Dialog height in pixels
        """
        self.root = tk.Toplevel(parent)
        self.root.title(title)
        self.root.resizable(False, False)
        self.root.grab_set()  # Make it modal
        
        # Center the dialog
        center_window(self.root, width, height)
        
        # Configure dialog styling
        self.root.configure(bg='#f0f0f0')
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the dialog UI components."""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Status label
        self.status_label = tk.Label(
            main_frame, 
            text="Initializing...", 
            font=DEFAULT_FONT,
            bg='#f0f0f0',
            fg='#333333'
        )
        self.status_label.pack(pady=(0, PADDING_MEDIUM))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=360,
            mode='determinate'
        )
        self.progress_bar.pack(pady=(0, PADDING_MEDIUM))
        
        # Details label (smaller text)
        self.details_label = tk.Label(
            main_frame,
            text="",
            font=("Segoe UI", 9),
            bg='#f0f0f0',
            fg='#666666'
        )
        self.details_label.pack()
        
        # Cancel button (initially hidden)
        self.cancel_button = tk.Button(
            main_frame,
            text="Cancel",
            command=self._on_cancel,
            state='disabled'
        )
        
        self.cancelled = False
        self.cancel_callback = None
        
    def set_status(self, status_text):
        """Update the main status text.
        
        Args:
            status_text (str): Status message to display
        """
        self.status_label.config(text=status_text)
        self.root.update_idletasks()
        
    def set_details(self, details_text):
        """Update the details text.
        
        Args:
            details_text (str): Details message to display
        """
        self.details_label.config(text=details_text)
        self.root.update_idletasks()
        
    def set_progress(self, percentage):
        """Update the progress bar.
        
        Args:
            percentage (float): Progress percentage (0-100)
        """
        self.progress_var.set(percentage)
        self.root.update_idletasks()
        
    def enable_cancel(self, cancel_callback=None):
        """Enable the cancel button.
        
        Args:
            cancel_callback (callable, optional): Function to call when cancelled
        """
        self.cancel_callback = cancel_callback
        self.cancel_button.config(state='normal')
        self.cancel_button.pack(pady=(PADDING_MEDIUM, 0))
        
    def disable_cancel(self):
        """Disable the cancel button."""
        self.cancel_button.config(state='disabled')
        
    def _on_cancel(self):
        """Handle cancel button click."""
        self.cancelled = True
        self.disable_cancel()
        self.set_status("Cancelling...")
        if self.cancel_callback:
            self.cancel_callback()
            
    def is_cancelled(self):
        """Check if the operation was cancelled.
        
        Returns:
            bool: True if cancelled, False otherwise
        """
        return self.cancelled
        
    def close(self):
        """Close the progress dialog."""
        if self.root and self.root.winfo_exists():
            self.root.grab_release()
            self.root.destroy()


class IndeterminateProgressDialog(ProgressDialog):
    """A progress dialog with indeterminate (animated) progress bar."""
    
    def _setup_ui(self):
        """Setup the dialog UI with indeterminate progress bar."""
        super()._setup_ui()
        
        # Switch to indeterminate mode
        self.progress_bar.config(mode='indeterminate')
        self.progress_bar.start(10)  # Start animation
        
    def set_progress(self, percentage):
        """Override - indeterminate progress doesn't use percentage."""
        pass  # Do nothing for indeterminate progress
        
    def close(self):
        """Close the dialog and stop animation."""
        if hasattr(self, 'progress_bar'):
            self.progress_bar.stop()
        super().close()
