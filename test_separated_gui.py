#!/usr/bin/env python3
"""
Test script to verify that the separated GUI components work correctly.
This script imports and tests the main GUI class.
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all the separated GUI components can be imported."""
    try:
        print("Testing imports...")
        
        # Test importing the main GUI class
        from src.gui.video_editor_gui import VideoEditorGUI
        print("✅ Main GUI class imported successfully")
        
        # Test importing sidebar widget
        from src.gui.widgets.sidebar import SidebarWidget
        print("✅ Sidebar widget imported successfully")
        
        # Test importing status bar widget
        from src.gui.widgets.status_bar import StatusBarWidget
        print("✅ Status bar widget imported successfully")
        
        # Test importing processing tab
        from src.gui.tabs.processing_tab import ProcessingTab
        print("✅ Processing tab imported successfully")
        
        # Test importing logs tab
        from src.gui.tabs.logs_tab import LogsTab
        print("✅ Logs tab imported successfully")
        
        # Test importing results tab
        from src.gui.tabs.results_tab import ResultsTab
        print("✅ Results tab imported successfully")
        
        # Test importing help tab
        from src.gui.tabs.help_tab import HelpTab
        print("✅ Help tab imported successfully")
        
        # Test importing GUI utils
        from src.gui.utils.gui_utils import GuiUtils
        print("✅ GUI utils imported successfully")
        
        print("\n🎉 All imports successful! The separation worked correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_gui_utils():
    """Test the GUI utility functions."""
    try:
        from src.gui.utils.gui_utils import GuiUtils
        
        print("\nTesting GUI utilities...")
        
        # Test file size formatting
        size_str = GuiUtils.format_file_size(1024 * 1024)  # 1 MB
        print(f"✅ File size formatting: {size_str}")
        
        # Test duration formatting
        duration_str = GuiUtils.format_duration(90.5)  # 1:30
        print(f"✅ Duration formatting: {duration_str}")
        
        # Test video file detection
        is_video = GuiUtils.is_video_file("test.mp4")
        print(f"✅ Video file detection: {is_video}")
        
        print("✅ All GUI utility tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ GUI utility test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Separated GUI Components")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test GUI utilities
    utils_ok = test_gui_utils()
    
    print("\n" + "=" * 50)
    if imports_ok and utils_ok:
        print("🎉 All tests passed! The GUI separation was successful.")
        print("\nYou can now run the separated GUI using:")
        print("python src/main_gui.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
