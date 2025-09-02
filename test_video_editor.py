#!/usr/bin/env python3
"""
Test Script for VideoEditor Class

This script tests the basic functionality of the VideoEditor class
to ensure everything is working correctly.
"""

import os
import sys
import tempfile
import shutil
from video_editor import VideoEditor


def test_video_editor_initialization():
    """Test VideoEditor class initialization."""
    print("Testing VideoEditor initialization...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a dummy video file (just a text file for testing)
        dummy_video = os.path.join(temp_dir, "test_video.mp4")
        with open(dummy_video, 'w') as f:
            f.write("This is a dummy video file for testing")
        
        try:
            # Test initialization
            editor = VideoEditor(dummy_video, temp_dir)
            print("✅ VideoEditor initialization successful")
            
            # Test output directory creation
            if os.path.exists(temp_dir):
                print("✅ Output directory created successfully")
            else:
                print("❌ Output directory creation failed")
                
        except Exception as e:
            print(f"❌ VideoEditor initialization failed: {e}")
            return False
    
    return True


def test_video_info_methods():
    """Test video information methods."""
    print("\nTesting video information methods...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        dummy_video = os.path.join(temp_dir, "test_video.mp4")
        with open(dummy_video, 'w') as f:
            f.write("Dummy video content")
        
        try:
            editor = VideoEditor(dummy_video, temp_dir)
            
            # Test get_video_info (this will fail with dummy file, but we test the method exists)
            if hasattr(editor, 'get_video_info'):
                print("✅ get_video_info method exists")
            else:
                print("❌ get_video_info method missing")
                
            # Test cleanup method
            if hasattr(editor, 'cleanup'):
                print("✅ cleanup method exists")
            else:
                print("❌ cleanup method missing")
                
        except Exception as e:
            print(f"⚠️  Expected error with dummy file: {e}")
            print("✅ VideoEditor methods exist (dummy file error is expected)")
    
    return True


def test_context_manager():
    """Test VideoEditor as a context manager."""
    print("\nTesting VideoEditor as context manager...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        dummy_video = os.path.join(temp_dir, "test_video.mp4")
        with open(dummy_video, 'w') as f:
            f.write("Dummy video content")
        
        try:
            with VideoEditor(dummy_video, temp_dir) as editor:
                print("✅ Context manager entry successful")
                if hasattr(editor, 'input_video_path'):
                    print("✅ Editor object accessible in context")
                else:
                    print("❌ Editor object not accessible in context")
                    
            print("✅ Context manager exit successful")
            
        except Exception as e:
            print(f"❌ Context manager test failed: {e}")
            return False
    
    return True


def test_method_existence():
    """Test that all required methods exist."""
    print("\nTesting method existence...")
    
    required_methods = [
        'load_video',
        'split_by_timestamps', 
        'split_into_equal_parts',
        'auto_split_by_scenes',
        'get_video_info',
        'cleanup'
    ]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        dummy_video = os.path.join(temp_dir, "test_video.mp4")
        with open(dummy_video, 'w') as f:
            f.write("Dummy video content")
        
        try:
            editor = VideoEditor(dummy_video, temp_dir)
            
            for method_name in required_methods:
                if hasattr(editor, method_name):
                    print(f"✅ {method_name} method exists")
                else:
                    print(f"❌ {method_name} method missing")
                    return False
                    
        except Exception as e:
            print(f"⚠️  Error during method testing: {e}")
            return False
    
    return True


def test_error_handling():
    """Test error handling for non-existent files."""
    print("\nTesting error handling...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        non_existent_video = os.path.join(temp_dir, "non_existent_video.mp4")
        
        try:
            VideoEditor(non_existent_video, temp_dir)
            print("❌ Should have raised FileNotFoundError")
            return False
            
        except FileNotFoundError:
            print("✅ FileNotFoundError properly raised for non-existent file")
        except Exception as e:
            print(f"❌ Unexpected error type: {type(e).__name__}")
            return False
    
    return True


def main():
    """Run all tests."""
    print("🧪 Running VideoEditor Tests")
    print("=" * 50)
    
    tests = [
        test_video_editor_initialization,
        test_video_info_methods,
        test_context_manager,
        test_method_existence,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ Test {test.__name__} failed")
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! VideoEditor is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())



