#!/usr/bin/env python3
"""
Smart Video Splitter - GUI Launcher

This script provides an easy way to launch the Smart Video Splitter GUI
from the main project directory.

Usage:
    python run.py
    python3 run.py
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Main entry point for the GUI launcher."""
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Path to the main GUI file
    gui_path = script_dir / "features" / "video_editor" / "main_gui.py"
    
    # Check if the GUI file exists
    if not gui_path.exists():
        print(f"❌ Error: GUI file not found at {gui_path}")
        print("Please ensure you're running this script from the project root directory.")
        sys.exit(1)
    
    try:
        print("🚀 Launching Smart Video Splitter GUI...")
        print(f"📁 Project root: {script_dir}")
        print("⏳ Please wait...")
        
        # Run the GUI file as a subprocess
        # This ensures proper module resolution and error handling
        result = subprocess.run([
            sys.executable, 
            str(gui_path)
        ], cwd=str(script_dir))
        
        if result.returncode != 0:
            print(f"❌ GUI exited with code: {result.returncode}")
            sys.exit(result.returncode)
            
    except FileNotFoundError:
        print("❌ Error: Python executable not found")
        print("Please ensure Python is installed and available in your PATH")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print("Please check the error details above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
