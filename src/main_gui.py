#!/usr/bin/env python3
"""
Main entry point for the Video Editor GUI application.
This file imports and runs the separated GUI components.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the main GUI class
from gui.video_editor_gui import VideoEditorGUI, main

if __name__ == "__main__":
    main()
