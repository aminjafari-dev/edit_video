#!/usr/bin/env python3
"""
Smart Scene Detection with Individual Folders - Creates a folder for each video

This script automatically detects scene boundaries and creates individual folders
for each input video, placing the split clips in their respective folders.
"""

import sys
from main_processor import process_multiple_videos, validate_video_files


def main():
    """Main function for smart scene detection with individual folders."""
    if len(sys.argv) < 2:
        print("Usage: python smart_split_with_folders.py <input_video1> [input_video2] ...")
        print("Example: python smart_split_with_folders.py video1.mp4 video2.mp4")
        print("Example: python smart_split_with_folders.py *.mp4")
        sys.exit(1)
    
    # Get all input video files
    input_videos = sys.argv[1:]
    
    # Validate and filter video files
    valid_videos = validate_video_files(input_videos)
    
    if not valid_videos:
        print("❌ No valid video files found to process")
        sys.exit(1)
    
    print(f"✅ Found {len(valid_videos)} valid video files to process")
    
    # Process all videos (using default min scene duration of 2.0 seconds)
    process_multiple_videos(valid_videos)


if __name__ == "__main__":
    main()
