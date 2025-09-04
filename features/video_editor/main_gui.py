#!/usr/bin/env python3
"""
Main entry point for the Video Editor GUI application.
This file imports and runs the separated GUI components.
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Import the main GUI class
from features.video_editor.video_editor_gui import VideoEditorGUI, main

if __name__ == "__main__":
    main()
