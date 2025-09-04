#!/usr/bin/env python3
"""
Logs tab for the Video Editor GUI.
Displays processing logs with controls for managing log content.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import time


class LogsTab(ttk.Frame):
    """
    Logs tab that displays detailed processing logs and provides log management tools.
    
    This tab provides:
    - Scrolled text area for displaying logs
    - Timestamped log entries
    - Controls for clearing, saving, and copying logs
    - Automatic scrolling to latest entries
    
    Usage:
        logs_tab = LogsTab(notebook, main_gui)
        logs_tab.log_message("Processing started...")
        logs_tab.clear_logs()
    """
    
    def __init__(self, notebook, main_gui):
        """Initialize the logs tab with all its components."""
        super().__init__(notebook, padding="20")
        self.main_gui = main_gui
        self.notebook = notebook
        self.create_widgets()
        self.add_to_notebook()
    
    def create_widgets(self):
        """Create and arrange all logs tab widgets."""
        # Logs text area
        logs_label = ttk.Label(self, text="Processing Logs:", font=('Segoe UI', 12, 'bold'))
        logs_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Create scrolled text widget
        self.logs_text = scrolledtext.ScrolledText(self, 
                                                 height=20, 
                                                 width=80,
                                                 font=('Consolas', 10),
                                                 background='#f8f9fa',
                                                 foreground='#212529')
        self.logs_text.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        # Logs control buttons
        logs_buttons_frame = ttk.Frame(self)
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
        
        # Configure grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def add_to_notebook(self):
        """Add this tab to the notebook."""
        self.notebook.add(self, text="📝 Logs")
    
    def log_message(self, message):
        """Add a message to the logs tab with timestamp.
        
        Args:
            message (str): The message to log
        """
        # Check if detailed logs are enabled (from sidebar settings)
        if hasattr(self.main_gui, 'sidebar') and hasattr(self.main_gui.sidebar, 'show_logs_var'):
            if not self.main_gui.sidebar.show_logs_var.get():
                return
        
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Update logs in main thread
        self.main_gui.root.after(0, lambda: self.logs_text.insert(tk.END, log_entry))
        self.main_gui.root.after(0, lambda: self.logs_text.see(tk.END))
    
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
            self.main_gui.root.clipboard_clear()
            self.main_gui.root.clipboard_append(self.logs_text.get(1.0, tk.END))
            messagebox.showinfo("Success", "Logs copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy logs: {str(e)}")
