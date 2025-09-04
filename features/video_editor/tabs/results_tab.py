#!/usr/bin/env python3
"""
Results tab for the Video Editor GUI.
Displays processing results in a tree view with management controls.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import sys


class ResultsTab(ttk.Frame):
    """
    Results tab that displays processing results in an organized tree view.
    
    This tab provides:
    - Tree view showing all processed videos and their results
    - Information about clips created, output folders, and file sizes
    - Controls for opening output folders and refreshing results
    - Clear results functionality
    
    Usage:
        results_tab = ResultsTab(notebook, main_gui)
        results_tab.refresh_results()
        results_tab.clear_results()
    """
    
    def __init__(self, notebook, main_gui):
        """Initialize the results tab with all its components."""
        super().__init__(notebook, padding="20")
        self.main_gui = main_gui
        self.notebook = notebook
        self.create_widgets()
        self.add_to_notebook()
    
    def create_widgets(self):
        """Create and arrange all results tab widgets."""
        # Results tree view
        results_label = ttk.Label(self, text="Processing Results:", font=('Segoe UI', 12, 'bold'))
        results_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Create tree view for results
        columns = ('File', 'Status', 'Clips', 'Output Folder', 'Size')
        self.results_tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)
        
        # Add scrollbar
        results_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scrollbar.set)
        
        # Grid layout
        self.results_tree.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        results_scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Results control buttons
        results_buttons_frame = ttk.Frame(self)
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
        
        # Configure grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def add_to_notebook(self):
        """Add this tab to the notebook."""
        self.notebook.add(self, text="📁 Results")
    
    def open_output_folder(self):
        """Open the output folder in the system file manager."""
        # Get output directory from sidebar
        if hasattr(self.main_gui, 'sidebar') and hasattr(self.main_gui.sidebar, 'output_dir_var'):
            output_dir = self.main_gui.sidebar.output_dir_var.get()
        else:
            output_dir = "smart_split"  # Default fallback
        
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
        """Refresh the results display by scanning the output directory."""
        # Clear current results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Get output directory from sidebar
        if hasattr(self.main_gui, 'sidebar') and hasattr(self.main_gui.sidebar, 'output_dir_var'):
            output_dir = self.main_gui.sidebar.output_dir_var.get()
        else:
            output_dir = "smart_split"  # Default fallback
        
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
