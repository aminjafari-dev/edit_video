#!/usr/bin/env python3
"""
Sidebar widget for the Video Editor GUI.
Contains file selection, processing options, and control buttons.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import time
import subprocess
import sys
from main_processor import process_single_video, validate_video_files
from video_utils import get_video_info
from scene_detection import detect_scenes_advanced
from video_processor import create_video_folder


class SidebarWidget(ttk.Frame):
    """
    Sidebar widget containing all the main controls and options.
    
    This widget provides:
    - File selection (single or multiple videos)
    - Processing configuration options
    - Control buttons for starting/stopping processing
    - Settings and preferences
    
    Usage:
        sidebar = SidebarWidget(parent, main_gui)
        sidebar.grid(row=0, column=0, sticky="nsew")
    """
    
    def __init__(self, parent, main_gui):
        """Initialize the sidebar with all its components."""
        super().__init__(parent, style='Card.TFrame', padding="10")
        self.main_gui = main_gui
        self.setup_grid()
        self.create_widgets()
    
    def setup_grid(self):
        """Configure the grid layout for the sidebar."""
        self.grid_rowconfigure(8, weight=1)  # Push settings to bottom
    
    def create_widgets(self):
        """Create and arrange all sidebar widgets."""
        # App title
        title_label = ttk.Label(self, 
                               text="🎬 Video Editor", 
                               font=('Segoe UI', 16, 'bold'),
                               foreground='#007bff')
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        
        # File selection section
        self.create_file_selection_widgets()
        
        # Processing options section
        self.create_processing_options_widgets()
        
        # Control buttons section
        self.create_control_buttons()
        
        # Settings section
        self.create_settings_widgets()
    
    def create_file_selection_widgets(self):
        """Create widgets for file selection functionality."""
        # File selection frame
        file_frame = ttk.LabelFrame(self, text="📁 File Selection", padding="10")
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
    
    def create_processing_options_widgets(self):
        """Create widgets for processing configuration."""
        # Processing options frame
        options_frame = ttk.LabelFrame(self, text="⚙️ Processing Options", padding="10")
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
    
    def create_control_buttons(self):
        """Create the main control buttons for processing."""
        # Control buttons frame
        control_frame = ttk.LabelFrame(self, text="🎯 Processing Controls", padding="10")
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
    
    def create_settings_widgets(self):
        """Create settings and configuration widgets."""
        # Settings frame
        settings_frame = ttk.LabelFrame(self, text="🔧 Settings", padding="10")
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
            self.main_gui.selected_files = [file_path]
            self.update_file_display()
            self.main_gui.logs_tab.log_message(f"Selected single video: {os.path.basename(file_path)}")
    
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
            self.main_gui.selected_files = list(file_paths)
            self.update_file_display()
            self.main_gui.logs_tab.log_message(f"Selected {len(file_paths)} video files")
    
    def clear_file_selection(self):
        """Clear the current file selection."""
        self.main_gui.selected_files = []
        self.update_file_display()
        self.main_gui.logs_tab.log_message("File selection cleared")
    
    def browse_output_directory(self):
        """Open directory dialog to select output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
            self.main_gui.logs_tab.log_message(f"Output directory set to: {directory}")
    
    def update_file_display(self):
        """Update the file selection display."""
        if not self.main_gui.selected_files:
            self.files_label.config(text="No files selected")
            self.main_gui.processing_tab.update_files_count(0)
        else:
            file_names = [os.path.basename(f) for f in self.main_gui.selected_files]
            self.main_gui.processing_tab.update_files_count(len(file_names))
            
            # Show first few file names
            if len(file_names) <= 3:
                display_text = ", ".join(file_names)
            else:
                display_text = ", ".join(file_names[:3]) + f" and {len(file_names) - 3} more"
            
            self.files_label.config(text=display_text)
    
    def start_processing(self):
        """Start the video processing in a separate thread."""
        if not self.main_gui.selected_files:
            messagebox.showwarning("No Files Selected", "Please select at least one video file to process.")
            return
        
        if self.main_gui.processing:
            messagebox.showinfo("Already Processing", "Video processing is already in progress.")
            return
        
        # Validate files
        valid_files = validate_video_files(self.main_gui.selected_files)
        if not valid_files:
            messagebox.showerror("Invalid Files", "No valid video files found in selection.")
            return
        
        # Reset processing state
        self.main_gui.processing = True
        self.main_gui.stop_processing_flag = False
        self.main_gui.completed_files = 0
        self.main_gui.total_clips = 0
        self.main_gui.start_time = None
        
        # Update UI
        self.process_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.main_gui.processing_tab.reset_progress()
        self.main_gui.processing_tab.start_current_file_progress()
        self.main_gui.processing_tab.update_status("Starting processing...")
        
        # Start processing thread
        self.main_gui.processing_thread = threading.Thread(
            target=self.process_videos_thread,
            args=(valid_files,),
            daemon=True
        )
        self.main_gui.processing_thread.start()
        
        self.main_gui.logs_tab.log_message("🚀 Started video processing")
    
    def stop_processing(self):
        """Stop the current processing operation."""
        if self.main_gui.processing:
            self.main_gui.stop_processing_flag = True
            self.main_gui.processing_tab.update_status("Stopping processing...")
            self.main_gui.logs_tab.log_message("⏹️ Stopping processing...")
    
    def process_videos_thread(self, video_files):
        """Process videos in a separate thread to avoid blocking the GUI."""
        try:
            total_files = len(video_files)
            self.main_gui.start_time = time.time()
            
            for i, video_path in enumerate(video_files):
                if self.main_gui.stop_processing_flag:
                    break
                
                # Update progress
                progress = (i / total_files) * 100
                self.main_gui.update_queue.put(('progress', progress))
                self.main_gui.update_queue.put(('current_file', os.path.basename(video_path)))
                self.main_gui.update_queue.put(('status', f"Processing {os.path.basename(video_path)}..."))
                
                # Process single video
                try:
                    success = process_single_video(video_path, self.output_dir_var.get())
                    if success:
                        self.main_gui.completed_files += 1
                        # Count clips created
                        video_folder = create_video_folder(video_path, self.output_dir_var.get())
                        if os.path.exists(video_folder):
                            clips = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
                            self.main_gui.total_clips += len(clips)
                        
                        self.main_gui.logs_tab.log_message(f"✅ Completed: {os.path.basename(video_path)}")
                    else:
                        self.main_gui.logs_tab.log_message(f"❌ Failed: {os.path.basename(video_path)}")
                    
                except Exception as e:
                    self.main_gui.logs_tab.log_message(f"❌ Error processing {os.path.basename(video_path)}: {str(e)}")
                
                # Update completed count
                self.main_gui.update_queue.put(('completed_count', self.main_gui.completed_files))
                self.main_gui.update_queue.put(('clips_count', self.main_gui.total_clips))
            
            # Processing complete
            if not self.main_gui.stop_processing_flag:
                self.main_gui.update_queue.put(('status', "Processing completed successfully!"))
                self.main_gui.update_queue.put(('progress', 100))
                self.main_gui.logs_tab.log_message("🎉 All videos processed successfully!")
                
                # Auto-open output folder if enabled
                if self.auto_open_var.get():
                    self.open_output_folder()
            else:
                self.main_gui.update_queue.put(('status', "Processing stopped by user"))
                self.main_gui.logs_tab.log_message("⏹️ Processing stopped by user")
                
        except Exception as e:
            self.main_gui.update_queue.put(('status', f"Error during processing: {str(e)}"))
            self.main_gui.logs_tab.log_message(f"❌ Processing error: {str(e)}")
        
        finally:
            # Reset processing state
            self.main_gui.processing = False
            self.main_gui.update_queue.put(('processing_complete', None))
    
    def preview_scenes(self):
        """Preview detected scenes for the first selected video."""
        if not self.main_gui.selected_files:
            messagebox.showwarning("No Files Selected", "Please select a video file first.")
            return
        
        video_path = self.main_gui.selected_files[0]
        
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
        preview_window = tk.Toplevel(self.main_gui.root)
        preview_window.title(f"Scene Preview - {os.path.basename(video_path)}")
        preview_window.geometry("600x500")
        preview_window.transient(self.main_gui.root)
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
    
    def enable_process_button(self):
        """Enable the process button."""
        self.process_button.config(state='normal')
    
    def disable_stop_button(self):
        """Disable the stop button."""
        self.stop_button.config(state='disabled')
