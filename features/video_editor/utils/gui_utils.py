#!/usr/bin/env python3
"""
Utility functions and helper classes for the Video Editor GUI.
Provides common operations and helper methods used across the GUI components.
"""

import os
import sys
import subprocess
from tkinter import messagebox


class GuiUtils:
    """
    Utility class providing common GUI operations and helper functions.
    
    This class provides:
    - File and directory operations
    - System-specific file opening
    - Error handling and user notifications
    - Common validation functions
    
    Usage:
        utils = GuiUtils()
        utils.open_folder("/path/to/folder")
        utils.show_error("Error message")
    """
    
    @staticmethod
    def open_folder(folder_path):
        """Open a folder in the system's default file manager.
        
        Args:
            folder_path (str): Path to the folder to open
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(folder_path):
            return False
        
        try:
            if sys.platform == "win32":
                os.startfile(folder_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", folder_path])
            else:
                subprocess.run(["xdg-open", folder_path])
            return True
        except Exception:
            return False
    
    @staticmethod
    def show_error(message, title="Error"):
        """Show an error message dialog.
        
        Args:
            message (str): Error message to display
            title (str): Dialog window title
        """
        messagebox.showerror(title, message)
    
    @staticmethod
    def show_warning(message, title="Warning"):
        """Show a warning message dialog.
        
        Args:
            message (str): Warning message to display
            title (str): Dialog window title
        """
        messagebox.showwarning(title, message)
    
    @staticmethod
    def show_info(message, title="Information"):
        """Show an information message dialog.
        
        Args:
            message (str): Information message to display
            title (str): Dialog window title
        """
        messagebox.showinfo(title, message)
    
    @staticmethod
    def ask_yes_no(message, title="Question"):
        """Show a yes/no question dialog.
        
        Args:
            message (str): Question message to display
            title (str): Dialog window title
            
        Returns:
            bool: True if user clicked Yes, False otherwise
        """
        return messagebox.askyesno(title, message)
    
    @staticmethod
    def format_file_size(size_bytes):
        """Format file size in bytes to human-readable format.
        
        Args:
            size_bytes (int): Size in bytes
            
        Returns:
            str: Formatted size string (e.g., "1.5 MB")
        """
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    @staticmethod
    def format_duration(seconds):
        """Format duration in seconds to human-readable format.
        
        Args:
            seconds (float): Duration in seconds
            
        Returns:
            str: Formatted duration string (e.g., "1:30")
        """
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes}:{remaining_seconds:02d}"
    
    @staticmethod
    def validate_file_path(file_path):
        """Validate if a file path exists and is accessible.
        
        Args:
            file_path (str): Path to the file to validate
            
        Returns:
            bool: True if file is valid and accessible, False otherwise
        """
        return os.path.isfile(file_path) and os.access(file_path, os.R_OK)
    
    @staticmethod
    def validate_directory_path(dir_path):
        """Validate if a directory path exists and is accessible.
        
        Args:
            dir_path (str): Path to the directory to validate
            
        Returns:
            bool: True if directory is valid and accessible, False otherwise
        """
        return os.path.isdir(dir_path) and os.access(dir_path, os.R_OK | os.W_OK)
    
    @staticmethod
    def get_file_extension(file_path):
        """Get the file extension from a file path.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: File extension (e.g., ".mp4") or empty string if no extension
        """
        return os.path.splitext(file_path)[1].lower()
    
    @staticmethod
    def is_video_file(file_path):
        """Check if a file is a video file based on its extension.
        
        Args:
            file_path (str): Path to the file to check
            
        Returns:
            bool: True if file is a video file, False otherwise
        """
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}
        return GuiUtils.get_file_extension(file_path) in video_extensions
