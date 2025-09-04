#!/usr/bin/env python3
"""
Modern GUI for the Video Editor application.
Provides an intuitive interface for video processing, scene detection, and splitting.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import time
from pathlib import Path
from typing import List, Optional
import queue
import subprocess

# Import your existing modules
from main_processor import process_single_video, process_multiple_videos, validate_video_files
from video_utils import get_video_info, is_video_file
from scene_detection import detect_scenes_advanced
from video_processor import create_video_folder, split_video_by_scenes


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
        self.create_widgets()
        self.setup_variables()
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
        self.create_sidebar()
        self.create_main_content()
        self.create_status_bar()
    
    def create_sidebar(self):
        """Create the left sidebar with navigation and controls."""
        # Sidebar frame
        sidebar = ttk.Frame(self.root, style='Card.TFrame', padding="10")
        sidebar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        sidebar.grid_rowconfigure(8, weight=1)  # Push settings to bottom
        
        # App title
        title_label = ttk.Label(sidebar, 
                               text="🎬 Video Editor", 
                               font=('Segoe UI', 16, 'bold'),
                               foreground='#007bff')
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        # File selection section
        self.create_file_selection_widgets(sidebar)
        
        # Processing options section
        self.create_processing_options_widgets(sidebar)
        
        # Control buttons section
        self.create_control_buttons(sidebar)
        
        # Settings section
        self.create_settings_widgets(sidebar)
    
    def create_file_selection_widgets(self, parent):
        """Create widgets for file selection functionality."""
        # File selection frame
        file_frame = ttk.LabelFrame(parent, text="📁 File Selection", padding="10")
        file_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Single file selection
        ttk.Button(file_frame, 
                  text="Select Single Video", 
                  style='Primary.TButton',
                  command=self.select_single_video).grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        ttk.Button(file_frame, 
                  text="Select Multiple Videos", 
                  style='Primary.TButton',
                  command=self.select_multiple_videos).grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Selected files display
        self.files_label = ttk.Label(file_frame, text="No files selected", foreground='#6c757d')
        self.files_label.grid(row=2, column=0, sticky="ew")
        
        # Clear selection button
        ttk.Button(file_frame, 
                  text="Clear Selection", 
                  command=self.clear_file_selection).grid(row=3, column=0, sticky="ew", pady=(5, 0))
    
    def create_processing_options_widgets(self, parent):
        """Create widgets for processing configuration."""
        # Processing options frame
        options_frame = ttk.LabelFrame(parent, text="⚙️ Processing Options", padding="10")
        options_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        # Minimum scene duration
        ttk.Label(options_frame, text="Min Scene Duration (seconds):").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.min_duration_var = tk.DoubleVar(value=8.0)
        duration_spinbox = ttk.Spinbox(options_frame, 
                                      from_=1.0, 
                                      to=60.0, 
                                      increment=0.5,
                                      textvariable=self.min_duration_var,
                                      width=10)
        duration_spinbox.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Output directory
        ttk.Label(options_frame, text="Output Directory:").grid(row=2, column=0, sticky="w", pady=(0, 5))
        output_frame = ttk.Frame(options_frame)
        output_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        
        self.output_dir_var = tk.StringVar(value="smart_split")
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var)
        output_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        ttk.Button(output_frame, 
                  text="Browse", 
                  command=self.browse_output_directory).grid(row=0, column=1)
        
        output_frame.grid_columnconfigure(0, weight=1)
    
    def create_control_buttons(self, parent):
        """Create the main control buttons for processing."""
        # Control buttons frame
        control_frame = ttk.LabelFrame(parent, text="🎯 Processing Controls", padding="10")
        control_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        
        # Process button
        self.process_button = ttk.Button(control_frame, 
                                       text="🚀 Start Processing", 
                                       style='Success.TButton',
                                       command=self.start_processing)
        self.process_button.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Stop button
        self.stop_button = ttk.Button(control_frame, 
                                    text="⏹️ Stop Processing", 
                                    style='Warning.TButton',
                                    command=self.stop_processing,
                                    state='disabled')
        self.stop_button.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Preview button
        ttk.Button(control_frame, 
                  text="👁️ Preview Scenes", 
                  style='Primary.TButton',
                  command=self.preview_scenes).grid(row=2, column=0, sticky="ew")
    
    def create_settings_widgets(self, parent):
        """Create settings and configuration widgets."""
        # Settings frame
        settings_frame = ttk.LabelFrame(parent, text="🔧 Settings", padding="10")
        settings_frame.grid(row=4, column=0, sticky="ew", pady=(0, 15))
        
        # Auto-open output folder
        self.auto_open_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, 
                       text="Auto-open output folder", 
                       variable=self.auto_open_var).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Show detailed logs
        self.show_logs_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, 
                       text="Show detailed logs", 
                       variable=self.show_logs_var).grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        # Keep original files
        self.keep_original_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, 
                       text="Keep original files", 
                       variable=self.keep_original_var).grid(row=2, column=0, sticky="w")
    
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
        self.create_processing_tab()
        self.create_logs_tab()
        self.create_results_tab()
        self.create_help_tab()
    
    def create_processing_tab(self):
        """Create the main processing tab."""
        processing_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(processing_frame, text="🎬 Processing")
        
        # Progress section
        progress_frame = ttk.LabelFrame(processing_frame, text="📊 Progress", padding="15")
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
        stats_frame = ttk.LabelFrame(processing_frame, text="📈 Statistics", padding="15")
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
    
    def create_logs_tab(self):
        """Create the logs tab for detailed output."""
        logs_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(logs_frame, text="📝 Logs")
        
        # Logs text area
        logs_label = ttk.Label(logs_frame, text="Processing Logs:", font=('Segoe UI', 12, 'bold'))
        logs_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Create scrolled text widget
        self.logs_text = scrolledtext.ScrolledText(logs_frame, 
                                                 height=20, 
                                                 width=80,
                                                 font=('Consolas', 10),
                                                 background='#f8f9fa',
                                                 foreground='#212529')
        self.logs_text.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        # Logs control buttons
        logs_buttons_frame = ttk.Frame(logs_frame)
        logs_buttons_frame.grid(row=2, column=0, sticky="ew")
        
        ttk.Button(logs_buttons_frame, 
                  text="Clear Logs", 
                  command=self.clear_logs).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(logs_buttons_frame, 
                  text="Save Logs", 
                  command=self.save_logs).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(logs_buttons_frame, 
                  text="Copy to Clipboard", 
                  command=self.copy_logs_to_clipboard).grid(row=0, column=2)
        
        logs_frame.grid_rowconfigure(1, weight=1)
        logs_frame.grid_columnconfigure(0, weight=1)
    
    def create_results_tab(self):
        """Create the results tab to display processing results."""
        results_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(results_frame, text="📁 Results")
        
        # Results tree view
        results_label = ttk.Label(results_frame, text="Processing Results:", font=('Segoe UI', 12, 'bold'))
        results_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Create tree view for results
        columns = ('File', 'Status', 'Clips', 'Output Folder', 'Size')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)
        
        # Add scrollbar
        results_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scrollbar.set)
        
        # Grid layout
        self.results_tree.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        results_scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Results control buttons
        results_buttons_frame = ttk.Frame(results_frame)
        results_buttons_frame.grid(row=2, column=0, sticky="ew")
        
        ttk.Button(results_buttons_frame, 
                  text="Open Output Folder", 
                  command=self.open_output_folder).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(results_buttons_frame, 
                  text="Refresh Results", 
                  command=self.refresh_results).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(results_buttons_frame, 
                  text="Clear Results", 
                  command=self.clear_results).grid(row=0, column=2)
        
        results_frame.grid_rowconfigure(1, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
    
    def create_help_tab(self):
        """Create the help tab with usage instructions."""
        help_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(help_frame, text="❓ Help")
        
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
        help_text_widget = scrolledtext.ScrolledText(help_frame, 
                                                   wrap=tk.WORD,
                                                   font=('Segoe UI', 10),
                                                   background='#ffffff',
                                                   foreground='#212529')
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)  # Make read-only
        
        help_text_widget.grid(row=0, column=0, sticky="nsew")
        help_frame.grid_rowconfigure(0, weight=1)
        help_frame.grid_columnconfigure(0, weight=1)
    
    def create_status_bar(self):
        """Create the status bar at the bottom of the window."""
        status_frame = ttk.Frame(self.root)
        status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=2)
        
        # Status message
        self.status_message = ttk.Label(status_frame, text="Ready", foreground='#6c757d')
        self.status_message.grid(row=0, column=0, sticky="w")
        
        # Version info
        version_label = ttk.Label(status_frame, text="v1.0.0", foreground='#6c757d')
        version_label.grid(row=0, column=1, sticky="e")
        
        status_frame.grid_columnconfigure(0, weight=1)
    
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
    
    def select_single_video(self):
        """Open file dialog to select a single video file."""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.selected_files = [file_path]
            self.update_file_display()
            self.log_message(f"Selected single video: {os.path.basename(file_path)}")
    
    def select_multiple_videos(self):
        """Open file dialog to select multiple video files."""
        file_paths = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
                ("All files", "*.*")
            ]
        )
        
        if file_paths:
            self.selected_files = list(file_paths)
            self.update_file_display()
            self.log_message(f"Selected {len(file_paths)} video files")
    
    def clear_file_selection(self):
        """Clear the current file selection."""
        self.selected_files = []
        self.update_file_display()
        self.log_message("File selection cleared")
    
    def browse_output_directory(self):
        """Open directory dialog to select output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
            self.log_message(f"Output directory set to: {directory}")
    
    def update_file_display(self):
        """Update the file selection display."""
        if not self.selected_files:
            self.files_label.config(text="No files selected")
            self.files_count_label.config(text="0")
        else:
            file_names = [os.path.basename(f) for f in self.selected_files]
            self.files_label.config(text=f"{len(file_names)} file(s) selected")
            self.files_count_label.config(text=str(len(file_names)))
            
            # Show first few file names
            if len(file_names) <= 3:
                display_text = ", ".join(file_names)
            else:
                display_text = ", ".join(file_names[:3]) + f" and {len(file_names) - 3} more"
            
            self.files_label.config(text=display_text)
    
    def start_processing(self):
        """Start the video processing in a separate thread."""
        if not self.selected_files:
            messagebox.showwarning("No Files Selected", "Please select at least one video file to process.")
            return
        
        if self.processing:
            messagebox.showinfo("Already Processing", "Video processing is already in progress.")
            return
        
        # Validate files
        valid_files = validate_video_files(self.selected_files)
        if not valid_files:
            messagebox.showerror("Invalid Files", "No valid video files found in selection.")
            return
        
        # Reset processing state
        self.processing = True
        self.stop_processing_flag = False
        self.completed_files = 0
        self.total_clips = 0
        self.start_time = None
        
        # Update UI
        self.process_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.overall_progress.config(value=0)
        self.current_file_progress.start()
        self.status_label.config(text="Starting processing...")
        
        # Start processing thread
        self.processing_thread = threading.Thread(
            target=self.process_videos_thread,
            args=(valid_files,),
            daemon=True
        )
        self.processing_thread.start()
        
        self.log_message("🚀 Started video processing")
    
    def stop_processing(self):
        """Stop the current processing operation."""
        if self.processing:
            self.stop_processing_flag = True
            self.status_label.config(text="Stopping processing...")
            self.log_message("⏹️ Stopping processing...")
    
    def process_videos_thread(self, video_files):
        """Process videos in a separate thread to avoid blocking the GUI."""
        try:
            total_files = len(video_files)
            self.start_time = time.time()
            
            for i, video_path in enumerate(video_files):
                if self.stop_processing_flag:
                    break
                
                # Update progress
                progress = (i / total_files) * 100
                self.update_queue.put(('progress', progress))
                self.update_queue.put(('current_file', os.path.basename(video_path)))
                self.update_queue.put(('status', f"Processing {os.path.basename(video_path)}..."))
                
                # Process single video
                try:
                    success = process_single_video(video_path, self.output_dir_var.get())
                    if success:
                        self.completed_files += 1
                        # Count clips created
                        video_folder = create_video_folder(video_path, self.output_dir_var.get())
                        if os.path.exists(video_folder):
                            clips = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
                            self.total_clips += len(clips)
                        
                        self.log_message(f"✅ Completed: {os.path.basename(video_path)}")
                    else:
                        self.log_message(f"❌ Failed: {os.path.basename(video_path)}")
                    
                except Exception as e:
                    self.log_message(f"❌ Error processing {os.path.basename(video_path)}: {str(e)}")
                
                # Update completed count
                self.update_queue.put(('completed_count', self.completed_files))
                self.update_queue.put(('clips_count', self.total_clips))
            
            # Processing complete
            if not self.stop_processing_flag:
                self.update_queue.put(('status', "Processing completed successfully!"))
                self.update_queue.put(('progress', 100))
                self.log_message("🎉 All videos processed successfully!")
                
                # Auto-open output folder if enabled
                if self.auto_open_var.get():
                    self.open_output_folder()
            else:
                self.update_queue.put(('status', "Processing stopped by user"))
                self.log_message("⏹️ Processing stopped by user")
                
        except Exception as e:
            self.update_queue.put(('status', f"Error during processing: {str(e)}"))
            self.log_message(f"❌ Processing error: {str(e)}")
        
        finally:
            # Reset processing state
            self.processing = False
            self.update_queue.put(('processing_complete', None))
    
    def check_queue(self):
        """Check for updates from the processing thread and update GUI."""
        try:
            while True:
                update_type, data = self.update_queue.get_nowait()
                
                if update_type == 'progress':
                    self.overall_progress.config(value=data)
                elif update_type == 'current_file':
                    self.current_file_label.config(text=f"Current: {data}")
                elif update_type == 'status':
                    self.status_label.config(text=data)
                    self.status_message.config(text=data)
                elif update_type == 'completed_count':
                    self.completed_count_label.config(text=str(data))
                elif update_type == 'clips_count':
                    self.clips_count_label.config(text=str(data))
                elif update_type == 'processing_complete':
                    self.processing_complete()
                
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_queue)
    
    def processing_complete(self):
        """Handle completion of processing."""
        self.process_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.current_file_progress.stop()
        
        # Update time display
        if self.start_time:
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.time_label.config(text=f"{minutes}:{seconds:02d}")
        
        # Show completion message
        if self.completed_files > 0:
            messagebox.showinfo("Processing Complete", 
                              f"Successfully processed {self.completed_files} video(s)!\n"
                              f"Created {self.total_clips} total clips.\n\n"
                              f"Check the Results tab for details.")
    
    def preview_scenes(self):
        """Preview detected scenes for the first selected video."""
        if not self.selected_files:
            messagebox.showwarning("No Files Selected", "Please select a video file first.")
            return
        
        video_path = self.selected_files[0]
        
        try:
            # Get video info
            info = get_video_info(video_path)
            if not info:
                messagebox.showerror("Error", "Could not get video information.")
                return
            
            # Detect scenes
            scene_timestamps = detect_scenes_advanced(video_path, self.min_duration_var.get())
            
            if len(scene_timestamps) < 2:
                messagebox.showinfo("Scene Detection", "Could not detect any scene boundaries.")
                return
            
            # Create preview window
            self.show_scene_preview(video_path, info, scene_timestamps)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error previewing scenes: {str(e)}")
    
    def show_scene_preview(self, video_path, info, scene_timestamps):
        """Show a preview window with detected scenes."""
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"Scene Preview - {os.path.basename(video_path)}")
        preview_window.geometry("600x500")
        preview_window.transient(self.root)
        preview_window.grab_set()
        
        # Video info
        info_frame = ttk.LabelFrame(preview_window, text="Video Information", padding="10")
        info_frame.pack(fill="x", padx=10, pady=10)
        
        info_text = f"Duration: {info['duration']:.2f}s | Resolution: {info['width']}x{info['height']} | FPS: {info['fps']:.2f}"
        ttk.Label(info_frame, text=info_text).pack()
        
        # Scenes list
        scenes_frame = ttk.LabelFrame(preview_window, text=f"Detected Scenes ({len(scene_timestamps) - 1})", padding="10")
        scenes_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Create tree view for scenes
        columns = ('Scene', 'Start Time', 'End Time', 'Duration')
        scenes_tree = ttk.Treeview(scenes_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            scenes_tree.heading(col, text=col)
            scenes_tree.column(col, width=120)
        
        # Add scenes to tree
        for i in range(len(scene_timestamps) - 1):
            start = scene_timestamps[i]
            end = scene_timestamps[i + 1]
            duration = end - start
            
            scenes_tree.insert('', 'end', values=(
                f"Scene {i+1}",
                f"{start:.2f}s",
                f"{end:.2f}s",
                f"{duration:.2f}s"
            ))
        
        # Add scrollbar
        scenes_scrollbar = ttk.Scrollbar(scenes_frame, orient="vertical", command=scenes_tree.yview)
        scenes_tree.configure(yscrollcommand=scenes_scrollbar.set)
        
        scenes_tree.pack(side="left", fill="both", expand=True)
        scenes_scrollbar.pack(side="right", fill="y")
        
        # Close button
        ttk.Button(preview_window, text="Close", command=preview_window.destroy).pack(pady=10)
    
    def log_message(self, message):
        """Add a message to the logs tab."""
        if self.show_logs_var.get():
            timestamp = time.strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            
            # Update logs in main thread
            self.root.after(0, lambda: self.logs_text.insert(tk.END, log_entry))
            self.root.after(0, lambda: self.logs_text.see(tk.END))
    
    def clear_logs(self):
        """Clear the logs text area."""
        self.logs_text.delete(1.0, tk.END)
    
    def save_logs(self):
        """Save the current logs to a file."""
        file_path = filedialog.asksaveasfilename(
            title="Save Logs",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.logs_text.get(1.0, tk.END))
                messagebox.showinfo("Success", "Logs saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save logs: {str(e)}")
    
    def copy_logs_to_clipboard(self):
        """Copy the current logs to the clipboard."""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.logs_text.get(1.0, tk.END))
            messagebox.showinfo("Success", "Logs copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy logs: {str(e)}")
    
    def open_output_folder(self):
        """Open the output folder in the system file manager."""
        output_dir = self.output_dir_var.get()
        if os.path.exists(output_dir):
            try:
                if sys.platform == "win32":
                    os.startfile(output_dir)
                elif sys.platform == "darwin":
                    subprocess.run(["open", output_dir])
                else:
                    subprocess.run(["xdg-open", output_dir])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open output folder: {str(e)}")
        else:
            messagebox.showwarning("Folder Not Found", "Output folder does not exist yet.")
    
    def refresh_results(self):
        """Refresh the results display."""
        # Clear current results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Scan output directory for results
        output_dir = self.output_dir_var.get()
        if os.path.exists(output_dir):
            for item in os.listdir(output_dir):
                item_path = os.path.join(output_dir, item)
                if os.path.isdir(item_path):
                    # Count clips
                    clips = [f for f in os.listdir(item_path) if f.endswith('.mp4')]
                    clip_count = len(clips)
                    
                    # Get folder size
                    try:
                        size = sum(os.path.getsize(os.path.join(item_path, f)) for f in clips)
                        size_mb = size / (1024 * 1024)
                    except:
                        size_mb = 0
                    
                    # Add to results
                    self.results_tree.insert('', 'end', values=(
                        item,
                        "Completed" if clip_count > 0 else "Failed",
                        clip_count,
                        item_path,
                        f"{size_mb:.1f} MB"
                    ))
    
    def clear_results(self):
        """Clear the results display."""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
    
    def on_closing(self):
        """Handle window closing event."""
        if self.processing:
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
            messagebox.showerror("FFmpeg Not Found", 
                               "FFmpeg is required but not found in your system PATH.\n\n"
                               "Please install FFmpeg and ensure it's accessible from the command line.")
            return
        
        # Create and run the GUI
        app = VideoEditorGUI()
        app.run()
        
    except ImportError as e:
        messagebox.showerror("Import Error", f"Failed to import required modules: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")


if __name__ == "__main__":
    main()
