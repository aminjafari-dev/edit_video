#!/usr/bin/env python3
"""
Status bar widget for the Video Editor GUI.
Displays current status messages and version information.
"""

import tkinter as tk
from tkinter import ttk


class StatusBarWidget(ttk.Frame):
    """
    Status bar widget that displays status messages and version info.
    
    This widget provides:
    - Current status message display
    - Version information
    - Responsive layout that expands to fill available width
    
    Usage:
        status_bar = StatusBarWidget(parent)
        status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        status_bar.update_status("Processing videos...")
    """
    
    def __init__(self, parent):
        """Initialize the status bar with its components."""
        super().__init__(parent)
        self.setup_grid()
        self.create_widgets()
    
    def setup_grid(self):
        """Configure the grid layout for the status bar."""
        self.grid_columnconfigure(0, weight=1)
    
    def create_widgets(self):
        """Create and arrange status bar widgets."""
        # Status message
        self.status_message = ttk.Label(self, text="Ready", foreground='#6c757d')
        self.status_message.grid(row=0, column=0, sticky="w")
        
        # Version info
        version_label = ttk.Label(self, text="v1.0.0", foreground='#6c757d')
        version_label.grid(row=0, column=1, sticky="e")
    
    def update_status(self, message):
        """Update the status message displayed in the status bar.
        
        Args:
            message (str): The new status message to display
        """
        self.status_message.config(text=message)
