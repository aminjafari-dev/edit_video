#!/usr/bin/env python3
"""
Video processing functions for splitting videos and managing output folders.
"""

import os
import subprocess
from typing import List
from video_utils import get_video_name


def create_video_folder(video_path: str, base_output_dir: str = "smart_split") -> str:
    """
    Create a folder for the specific video being processed.
    
    Args:
        video_path: Path to the input video file
        base_output_dir: Base directory for all split videos
        
    Returns:
        Path to the created folder for this video
    """
    # Get the video filename without extension
    video_name = get_video_name(video_path)
    
    # Create the base output directory if it doesn't exist
    os.makedirs(base_output_dir, exist_ok=True)
    
    # Create a folder specifically for this video
    video_folder = os.path.join(base_output_dir, video_name)
    os.makedirs(video_folder, exist_ok=True)
    
    print(f"📁 Created folder: {video_folder}")
    return video_folder


def split_video_by_scenes(input_video: str, scene_timestamps: List[float], 
                          output_dir: str) -> List[str]:
    """
    Split video based on detected scene boundaries.
    
    Args:
        input_video: Path to input video file
        scene_timestamps: List of timestamps where scenes change
        output_dir: Directory to save output clips (specific to this video)
        
    Returns:
        List of paths to created video clips
    """
    output_paths = []
    
    print(f"\n✂️  Splitting video into {len(scene_timestamps) - 1} clips...")
    
    for i in range(len(scene_timestamps) - 1):
        start_time = scene_timestamps[i]
        end_time = scene_timestamps[i + 1]
        duration = end_time - start_time
        
        # Generate output filename
        output_filename = f"clip_{i+1:02d}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"\nProcessing clip {i+1}:")
        print(f"  Time: {start_time:.2f}s to {end_time:.2f}s")
        print(f"  Duration: {duration:.2f}s")
        
        # Use FFmpeg to extract the clip
        cmd = [
            'ffmpeg',
            '-i', input_video,
            '-ss', str(start_time),
            '-t', str(duration),
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-avoid_negative_ts', 'make_zero',
            '-y',
            output_path
        ]
        
        try:
            # Run FFmpeg command
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"  ✅ Saved as: {output_filename}")
            output_paths.append(output_path)
            
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Error: {e}")
            continue
    
    return output_paths


def display_video_info(info: dict) -> None:
    """Display video information in a formatted way."""
    print(f"✅ Video loaded successfully:")
    print(f"   Duration: {info['duration']:.2f} seconds")
    print(f"   Resolution: {info['width']}x{info['height']}")
    print(f"   Frame Rate: {info['fps']:.2f} FPS")
    if info['audio_fps']:
        print(f"   Audio: {info['audio_fps']} Hz")
    print(f"   File Size: {info['file_size_mb']:.2f} MB")


def display_scene_info(scene_timestamps: List[float]) -> None:
    """Display detected scene information."""
    print(f"\n🎯 Detected {len(scene_timestamps) - 1} scenes:")
    for i in range(len(scene_timestamps) - 1):
        start = scene_timestamps[i]
        end = scene_timestamps[i + 1]
        duration = end - start
        print(f"  Scene {i+1}: {start:.2f}s to {end:.2f}s ({duration:.2f}s)")


def display_clip_summary(clips: List[str], video_folder: str) -> None:
    """Display summary of created clips."""
    if clips:
        print(f"\n🎉 Successfully created {len(clips)} clips!")
        for i, clip_path in enumerate(clips, 1):
            file_size = os.path.getsize(clip_path) / (1024 * 1024)
            print(f"  {i:2d}. {os.path.basename(clip_path)} ({file_size:.2f} MB)")
        
        print(f"\nAll clips saved to: {os.path.abspath(video_folder)}")
    else:
        print("❌ No clips were created successfully")
