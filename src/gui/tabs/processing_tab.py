#!/usr/bin/env python3
"""
Processing tab for the Video Editor GUI.
Displays progress bars, statistics, and current processing status.
"""

import tkinter as tk
from tkinter import ttk


class ProcessingTab(ttk.Frame):
    """
    Processing tab that displays progress and statistics during video processing.
    
    This tab provides:
    - Overall progress bar for all videos
    - Current file progress indicator
    - Status messages and current file information
    - Statistics including file counts and processing time
    
    Usage:
        processing_tab = ProcessingTab(notebook, main_gui)
        processing_tab.update_progress(50)  # Update to 50%
        processing_tab.update_status("Processing video...")
    """
    
    def __init__(self, notebook, main_gui):
        """Initialize the processing tab with all its components."""
        super().__init__(notebook, padding="20")
        self.main_gui = main_gui
        self.notebook = notebook
        self.create_widgets()
        self.add_to_notebook()
    
    def create_widgets(self):
        """Create and arrange all processing tab widgets."""
        # Progress section
        progress_frame = ttk.LabelFrame(self, text="📊 Progress", padding="15")
        progress_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Overall progress
        ttk.Label(progress_frame, text="Overall Progress:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.overall_progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.overall_progress.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Current file progress
        ttk.Label(progress_frame, text="Current File:").grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.current_file_progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.current_file_progress.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        
        # Status labels
        self.status_label = ttk.Label(progress_frame, text="Ready to process", font=('Segoe UI', 10))
        self.status_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        self.current_file_label = ttk.Label(progress_frame, text="", foreground='#6c757d')
        self.current_file_label.grid(row=5, column=0, sticky="w")
        
        # Statistics section
        stats_frame = ttk.LabelFrame(self, text="📈 Statistics", padding="15")
        stats_frame.grid(row=1, column=0, sticky="ew")
        
        # Stats grid
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(3, weight=1)
        
        # Left column
        ttk.Label(stats_frame, text="Files to Process:").grid(row=0, column=0, sticky="w", pady=2)
        self.files_count_label = ttk.Label(stats_frame, text="0", font=('Segoe UI', 12, 'bold'))
        self.files_count_label.grid(row=0, column=1, sticky="w", padx=(10, 20), pady=2)
        
        ttk.Label(stats_frame, text="Files Completed:").grid(row=1, column=0, sticky="w", pady=2)
        self.completed_count_label = ttk.Label(stats_frame, text="0", font=('Segoe UI', 12, 'bold'))
        self.completed_count_label.grid(row=1, column=1, sticky="w", padx=(10, 20), pady=2)
        
        # Right column
        ttk.Label(stats_frame, text="Total Clips Created:").grid(row=0, column=2, sticky="w", pady=2)
        self.clips_count_label = ttk.Label(stats_frame, text="0", font=('Segoe UI', 12, 'bold'))
        self.clips_count_label.grid(row=0, column=2, sticky="w", padx=(10, 0), pady=2)
        
        ttk.Label(stats_frame, text="Processing Time:").grid(row=1, column=2, sticky="w", pady=2)
        self.time_label = ttk.Label(stats_frame, text="0:00", font=('Segoe UI', 12, 'bold'))
        self.time_label.grid(row=1, column=2, sticky="w", padx=(10, 0), pady=2)
    
    def add_to_notebook(self):
        """Add this tab to the notebook."""
        self.notebook.add(self, text="🎬 Processing")
    
    def update_overall_progress(self, value):
        """Update the overall progress bar.
        
        Args:
            value (float): Progress value from 0 to 100
        """
        self.overall_progress.config(value=value)
    
    def update_current_file(self, filename):
        """Update the current file label.
        
        Args:
            filename (str): Name of the current file being processed
        """
        self.current_file_label.config(text=f"Current: {filename}")
    
    def update_status(self, message):
        """Update the status label.
        
        Args:
            message (str): New status message
        """
        self.status_label.config(text=message)
    
    def update_completed_count(self, count):
        """Update the completed files count.
        
        Args:
            count (int): Number of completed files
        """
        self.completed_count_label.config(text=str(count))
    
    def update_clips_count(self, count):
        """Update the total clips count.
        
        Args:
            count (int): Total number of clips created
        """
        self.clips_count_label.config(text=str(count))
    
    def update_files_count(self, count):
        """Update the files to process count.
        
        Args:
            count (int): Number of files to process
        """
        self.files_count_label.config(text=str(count))
    
    def update_time_display(self, time_str):
        """Update the processing time display.
        
        Args:
            time_str (str): Time string to display (e.g., "1:30")
        """
        self.time_label.config(text=time_str)
    
    def reset_progress(self):
        """Reset the overall progress bar to 0."""
        self.overall_progress.config(value=0)
    
    def start_current_file_progress(self):
        """Start the current file progress bar animation."""
        self.current_file_progress.start()
    
    def stop_current_file_progress(self):
        """Stop the current file progress bar animation."""
        self.current_file_progress.stop()
