#!/usr/bin/env python3
"""
Help tab for the Video Editor GUI.
Displays usage instructions, features, and troubleshooting information.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext


class HelpTab(ttk.Frame):
    """
    Help tab that provides comprehensive usage instructions and help content.
    
    This tab provides:
    - Application overview and purpose
    - Step-by-step usage instructions
    - Feature descriptions and capabilities
    - Processing options explanation
    - Output format information
    - Tips and troubleshooting guidance
    
    Usage:
        help_tab = HelpTab(notebook, main_gui)
    """
    
    def __init__(self, notebook, main_gui):
        """Initialize the help tab with all its components."""
        super().__init__(notebook, padding="20")
        self.main_gui = main_gui
        self.notebook = notebook
        self.create_widgets()
        self.add_to_notebook()
    
    def create_widgets(self):
        """Create and arrange all help tab widgets."""
        # Help content
        help_text = """
🎬 Video Editor - Smart Scene Detection & Splitting

This application automatically detects scene changes in your videos and splits them into individual clips, perfect for creating TikTok-style content or organizing long videos.

📁 How to Use:
1. Select one or more video files using the buttons in the sidebar
2. Configure processing options (minimum scene duration, output directory)
3. Click "Start Processing" to begin automatic scene detection and splitting
4. Monitor progress in the Processing tab
5. View results and logs in their respective tabs

⚙️ Features:
• Automatic scene detection using advanced algorithms
• Configurable minimum scene duration
• Batch processing of multiple videos
• Detailed progress tracking and logging
• Automatic output folder organization
• Support for various video formats (MP4, AVI, MOV, etc.)

🔧 Processing Options:
• Min Scene Duration: Minimum length for each scene (default: 8 seconds)
• Output Directory: Where to save the split video clips
• Auto-open output folder: Automatically open results after processing
• Show detailed logs: Display comprehensive processing information

📊 Output:
• Each video gets its own folder
• Clips are named sequentially (clip_01.mp4, clip_02.mp4, etc.)
• Original video files are preserved
• Processing logs and statistics are available

💡 Tips:
• For best results, use videos with clear scene transitions
• Adjust minimum scene duration based on your content type
• Processing time depends on video length and complexity
• Check the logs tab for detailed information about each step

🔧 Troubleshooting:
• Ensure FFmpeg is installed and accessible in your system PATH
• Check that input video files are valid and not corrupted
• Verify you have sufficient disk space for output files
• If scene detection fails, try adjusting the minimum duration setting
        """
        
        # Create scrolled text widget for help
        help_text_widget = scrolledtext.ScrolledText(self, 
                                                   wrap=tk.WORD,
                                                   font=('Segoe UI', 10),
                                                   background='#ffffff',
                                                   foreground='#212529')
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)  # Make read-only
        
        help_text_widget.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def add_to_notebook(self):
        """Add this tab to the notebook."""
        self.notebook.add(self, text="❓ Help")
