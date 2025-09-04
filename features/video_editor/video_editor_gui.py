#!/usr/bin/env python3
"""
Main GUI class for the Video Editor application.
Provides the core structure and coordinates all GUI components.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import os
import sys
import queue
import subprocess
from pathlib import Path
from typing import List, Optional

# Import your existing modules

from core.utils.video_utils import get_video_info, is_video_file
from core.detection.scene_detection import detect_scenes_advanced
from core.processing.video_processor import create_video_folder, split_video_by_scenes

# Import GUI components
from .widgets.sidebar import SidebarWidget
from .widgets.status_bar import StatusBarWidget
from .tabs.processing_tab import ProcessingTab
from .tabs.logs_tab import LogsTab
from .tabs.results_tab import ResultsTab
from .tabs.help_tab import HelpTab
from .utils.gui_utils import GuiUtils


class VideoEditorGUI:
    """
    Main GUI class for the Video Editor application.
    
    This class provides a modern, user-friendly interface for:
    - Selecting input videos (single or multiple)
    - Configuring processing parameters
    - Monitoring processing progress
    - Viewing results and output information
    
    Usage:
        app = VideoEditorGUI()
        app.run()
    """
    
    def __init__(self):
        """Initialize the GUI with all components and styling."""
        self.root = tk.Tk()
        self.setup_main_window()
        self.setup_styles()
        self.setup_variables()
        
        # Create GUI components
        self.create_widgets()
        self.setup_bindings()
        
        # Queue for thread-safe GUI updates
        self.update_queue = queue.Queue()
        self.check_queue()
    
    def setup_main_window(self):
        """Configure the main window properties and appearance."""
        self.root.title("🎬 Video Editor - Smart Scene Detection & Splitting")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Set window icon if available
        try:
            self.root.iconbitmap("assets/icons/video_editor.ico")
        except:
            pass
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
    
    def setup_styles(self):
        """Configure custom styles for the GUI components."""
        style = ttk.Style()
        
        # Configure modern theme
        style.theme_use('clam')
        
        # Custom styles for buttons
        style.configure('Primary.TButton', 
                       background='#007bff', 
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Success.TButton',
                       background='#28a745',
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Warning.TButton',
                       background='#ffc107',
                       foreground='black',
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure frame styles
        style.configure('Card.TFrame', 
                       relief='solid', 
                       borderwidth=1,
                       background='#f8f9fa')
    
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Create sidebar
        self.sidebar = SidebarWidget(self.root, self)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create main content area
        self.create_main_content()
        
        # Create status bar
        self.status_bar = StatusBarWidget(self.root)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=2)
    
    def create_main_content(self):
        """Create the main content area with tabs."""
        # Main content frame
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # Create tabs
        self.processing_tab = ProcessingTab(self.notebook, self)
        self.logs_tab = LogsTab(self.notebook, self)
        self.results_tab = ResultsTab(self.notebook, self)
        self.help_tab = HelpTab(self.notebook, self)
    
    def setup_variables(self):
        """Initialize and setup all variables used by the GUI."""
        self.selected_files = []
        self.processing = False
        self.processing_thread = None
        self.stop_processing_flag = False
        self.start_time = None
        self.completed_files = 0
        self.total_clips = 0
    
    def setup_bindings(self):
        """Setup event bindings and callbacks."""
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def check_queue(self):
        """Check for updates from the processing thread and update GUI."""
        try:
            while True:
                update_type, data = self.update_queue.get_nowait()
                
                if update_type == 'progress':
                    self.processing_tab.update_overall_progress(data)
                elif update_type == 'current_file':
                    self.processing_tab.update_current_file(data)
                elif update_type == 'status':
                    self.processing_tab.update_status(data)
                    self.status_bar.update_status(data)
                elif update_type == 'completed_count':
                    self.processing_tab.update_completed_count(data)
                elif update_type == 'clips_count':
                    self.processing_tab.update_clips_count(data)
                elif update_type == 'processing_complete':
                    self.processing_complete()
                
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_queue)
    
    def processing_complete(self):
        """Handle completion of processing."""
        self.sidebar.enable_process_button()
        self.sidebar.disable_stop_button()
        self.processing_tab.stop_current_file_progress()
        
        # Update time display
        if self.start_time:
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.processing_tab.update_time_display(f"{minutes}:{seconds:02d}")
        
        # Show completion message
        if self.completed_files > 0:
            from tkinter import messagebox
            messagebox.showinfo("Processing Complete", 
                              f"Successfully processed {self.completed_files} video(s)!\n"
                              f"Created {self.total_clips} total clips.\n\n"
                              f"Check the Results tab for details.")
    
    def on_closing(self):
        """Handle window closing event."""
        if self.processing:
            from tkinter import messagebox
            if messagebox.askyesno("Processing Active", 
                                 "Video processing is still active. Do you want to stop and exit?"):
                self.stop_processing_flag = True
                if self.processing_thread:
                    self.processing_thread.join(timeout=2)
            else:
                return
        
        self.root.destroy()
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    """Main entry point for the Video Editor GUI application."""
    try:
        # Check if FFmpeg is available
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode != 0:
            from tkinter import messagebox
            messagebox.showerror("FFmpeg Not Found", 
                               "FFmpeg is required but not found in your system PATH.\n\n"
                               "Please install FFmpeg and ensure it's accessible from the command line.")
            return
        
        # Create and run the GUI
        app = VideoEditorGUI()
        app.run()
        
    except ImportError as e:
        from tkinter import messagebox
        messagebox.showerror("Import Error", f"Failed to import required modules: {str(e)}")
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")


if __name__ == "__main__":
    main()
