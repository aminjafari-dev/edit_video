#!/usr/bin/env python3
"""
Video processing functions for splitting videos and managing output folders.
"""

import os
import subprocess
from typing import List
from core.utils.video_utils import get_video_name


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
    from core.utils.video_utils import get_ffmpeg_path
    
    # Get FFmpeg path
    ffmpeg_path = get_ffmpeg_path()
    if not ffmpeg_path:
        print("❌ Error: FFmpeg not found")
        return []
    
    # Convert to absolute paths
    input_video = os.path.abspath(input_video)
    output_dir = os.path.abspath(output_dir)
    
    output_paths = []
    total_clips = len(scene_timestamps) - 1
    
    print(f"\n✂️  Splitting video into {total_clips} clips...")
    
    for i in range(total_clips):
        # Calculate timestamps with adjustments to avoid overlap
        start_time = scene_timestamps[i]
        end_time = scene_timestamps[i + 1]
        
        # Add small padding to avoid overlap
        padding = 0.04  # About 1 frame at 25fps
        adjusted_start = start_time + padding
        adjusted_end = end_time - padding
        duration = adjusted_end - adjusted_start
        
        # Skip if duration becomes too short
        if duration < 0.1:
            print(f"⚠️ Skipping clip {i+1} - too short after adjustment")
            continue
        
        # Generate output filename
        output_filename = f"clip_{i+1:02d}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"\nProcessing clip {i+1}/{total_clips}:")
        print(f"  Time: {adjusted_start:.2f}s to {adjusted_end:.2f}s")
        print(f"  Duration: {duration:.2f}s")
        
        # Two-pass encoding for better quality
        cmd = [
            ffmpeg_path,
            '-ss', str(adjusted_start),  # Seek before input for accuracy
            '-i', input_video,
            '-t', str(duration),
            '-map', '0:v:0',            # First video stream
            '-map', '0:a:0?',           # First audio stream (if exists)
            '-c:v', 'libx264',          # Video codec
            '-preset', 'medium',         # Balance between speed and quality
            '-crf', '18',               # High quality
            '-c:a', 'aac',              # Audio codec
            '-b:a', '192k',             # Audio bitrate
            '-af', 'apad',              # Audio padding
            '-shortest',                 # Cut to shortest stream
            '-copyts',                  # Copy timestamps
            '-avoid_negative_ts', '1',  # Avoid negative timestamps
            '-y',                       # Overwrite output
            output_path
        ]
        
        try:
            # Start FFmpeg process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Monitor the process
            print("  ⏳ Processing clip...", end='\r')
            _, stderr = process.communicate()
            
            # Check if the file was created successfully
            if process.returncode == 0 and os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # Size in MB
                print(f"  ✅ Saved as: {output_filename} ({file_size:.2f} MB)")
                output_paths.append(output_path)
            else:
                print(f"  ❌ Error processing clip: {stderr}")
                # Clean up failed output
                if os.path.exists(output_path):
                    try:
                        os.remove(output_path)
                    except:
                        pass
                        
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            # Clean up failed output
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass
    
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
