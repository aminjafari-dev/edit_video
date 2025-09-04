#!/usr/bin/env python3
"""
Main video processing logic that orchestrates the workflow.
"""

import os
from typing import List
from core.utils.video_utils import get_video_info, is_video_file
from core.detection.scene_detection import detect_scenes_advanced
from core.processing.video_processor import (
    create_video_folder, 
    split_video_by_scenes,
    display_video_info,
    display_scene_info,
    display_clip_summary
)


def process_single_video(input_video: str, base_output_dir: str = "smart_split", min_scene_duration: float = 2.0) -> bool:
    """
    Process a single video: detect scenes and split into clips in its own folder.
    
    Args:
        input_video: Path to the input video file
        base_output_dir: Base directory for all split videos
        min_scene_duration: Minimum duration for a scene in seconds
        
    Returns:
        True if successful, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"🎬 Processing: {os.path.basename(input_video)}")
    print(f"{'='*60}")
    
    if not os.path.exists(input_video):
        print(f"❌ Error: Input video file not found: {input_video}")
        return False
    
    # Get video information
    print("📹 Getting video information...")
    info = get_video_info(input_video)
    if not info:
        print("❌ Could not get video information")
        return False
    
    display_video_info(info)
    
    # Detect scenes automatically
    print(f"🔍 Using minimum scene duration: {min_scene_duration} seconds")
    scene_timestamps = detect_scenes_advanced(input_video, min_scene_duration)
    
    if len(scene_timestamps) < 2:
        print("❌ Could not detect any scene boundaries")
        return False
    
    display_scene_info(scene_timestamps)
    
    # Create folder for this video
    video_folder = create_video_folder(input_video, base_output_dir)
    
    # Split the video
    clips = split_video_by_scenes(input_video, scene_timestamps, video_folder)
    
    display_clip_summary(clips, video_folder)
    
    return len(clips) > 0


def process_multiple_videos(video_paths: List[str], base_output_dir: str = "smart_split", min_scene_duration: float = 2.0) -> None:
    """
    Process multiple videos, creating individual folders for each.
    
    Args:
        video_paths: List of paths to video files
        base_output_dir: Base directory for all split videos
        min_scene_duration: Minimum duration for a scene in seconds
    """
    print(f"🚀 Processing {len(video_paths)} videos...")
    print(f"Base output directory: {os.path.abspath(base_output_dir)}")
    
    successful = 0
    failed = 0
    
    for video_path in video_paths:
        try:
            if process_single_video(video_path, base_output_dir, min_scene_duration):
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Unexpected error processing {os.path.basename(video_path)}: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"📊 Processing Summary:")
    print(f"   Successful: {successful}")
    print(f"   Failed: {failed}")
    print(f"   Total: {len(video_paths)}")
    print(f"{'='*60}")


def validate_video_files(input_videos: List[str]) -> List[str]:
    """
    Validate and filter input video files.
    
    Args:
        input_videos: List of potential video file paths
        
    Returns:
        List of valid video file paths
    """
    valid_videos = []
    for video in input_videos:
        if os.path.exists(video):
            # Check if it's a video file
            if is_video_file(video):
                valid_videos.append(video)
            else:
                print(f"⚠️  Skipping non-video file: {video}")
        else:
            print(f"⚠️  Skipping non-existent file: {video}")
    
    return valid_videos
