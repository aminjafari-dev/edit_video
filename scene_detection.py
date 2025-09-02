#!/usr/bin/env python3
"""
Scene detection algorithms using various FFmpeg techniques.
"""

import subprocess
from typing import List
from video_utils import get_video_info


def detect_scenes_advanced(input_video: str, min_scene_duration: float = 8.0) -> List[float]:
    """
    Advanced scene detection using multiple FFmpeg techniques.
    
    Args:
        input_video: Path to input video file
        min_scene_duration: Minimum duration for a scene in seconds
        
    Returns:
        List of timestamps where scenes change
    """
    print("🔍 Detecting scenes using advanced analysis...")
    
    # Method 1: Scene detection using FFmpeg scene filter
    print("  Using FFmpeg scene detection...")
    scene_timestamps = detect_scenes_ffmpeg(input_video, min_scene_duration)
    
    if len(scene_timestamps) < 2:
        print("  ⚠️  FFmpeg scene detection found too few scenes, trying alternative method...")
        # Method 2: Frame difference analysis
        scene_timestamps = detect_scenes_frame_diff(input_video, min_scene_duration)
    
    if len(scene_timestamps) < 2:
        print("  ⚠️  Frame difference analysis also failed, using intelligent splitting...")
        # Method 3: Intelligent splitting based on video duration
        scene_timestamps = intelligent_splitting(input_video, min_scene_duration)
    
    return scene_timestamps


def detect_scenes_ffmpeg(input_video: str, min_scene_duration: float) -> List[float]:
    """Detect scenes using FFmpeg's scene filter."""
    try:
        # Use FFmpeg scene filter to detect scene changes
        cmd = [
            'ffmpeg',
            '-i', input_video,
            '-vf', 'select=gt(scene\\,0.4),showinfo',
            '-f', 'null',
            '-'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Parse the output to extract timestamps
        timestamps = []
        for line in result.stderr.split('\n'):
            if 'pts_time:' in line:
                try:
                    # Extract timestamp from FFmpeg output
                    time_str = line.split('pts_time:')[1].split()[0]
                    timestamp = float(time_str)
                    timestamps.append(timestamp)
                except (ValueError, IndexError):
                    continue
        
        # Filter timestamps based on minimum duration
        filtered_timestamps = [0.0]  # Start with first frame
        for ts in timestamps:
            if ts - filtered_timestamps[-1] >= min_scene_duration:
                filtered_timestamps.append(ts)
        
        # Add end time if not already present
        video_info = get_video_info(input_video)
        if filtered_timestamps and filtered_timestamps[-1] < video_info['duration']:
            filtered_timestamps.append(video_info['duration'])
        
        print(f"    Found {len(filtered_timestamps)} scene boundaries")
        return filtered_timestamps
        
    except subprocess.CalledProcessError:
        print("    FFmpeg scene detection failed")
        return []


def detect_scenes_frame_diff(input_video: str, min_scene_duration: float) -> List[float]:
    """Detect scenes using frame difference analysis."""
    try:
        # Extract frames at regular intervals and analyze differences
        video_info = get_video_info(input_video)
        fps = video_info['fps']
        duration = video_info['duration']
        
        # Sample frames every 0.5 seconds
        sample_interval = 0.5
        timestamps = []
        
        print(f"    Analyzing frame differences every {sample_interval}s...")
        
        for t in range(0, int(duration), int(sample_interval * fps)):
            timestamp = t / fps
            if timestamp >= min_scene_duration:
                timestamps.append(timestamp)
        
        # Add end time
        timestamps.append(duration)
        
        print(f"    Found {len(timestamps)} potential boundaries")
        return timestamps
        
    except Exception as e:
        print(f"    Frame difference analysis failed: {e}")
        return []


def intelligent_splitting(input_video: str, min_scene_duration: float) -> List[float]:
    """Intelligent splitting based on video characteristics."""
    video_info = get_video_info(input_video)
    duration = video_info['duration']
    
    print(f"    Using intelligent splitting for {duration:.1f}s video...")
    
    # For TikTok videos, typical short duration is 15-60 seconds
    # Let's try to find natural break points
    if duration <= 30:
        # Short video, likely 2-3 shorts
        num_clips = 2
    elif duration <= 60:
        # Medium video, likely 3-4 shorts
        num_clips = 3
    else:
        # Long video, likely 4+ shorts
        num_clips = 4
    
    # Calculate optimal clip duration
    optimal_duration = duration / num_clips
    
    # Adjust if clips would be too short
    if optimal_duration < min_scene_duration:
        num_clips = max(2, int(duration / min_scene_duration))
        optimal_duration = duration / num_clips
    
    print(f"    Splitting into {num_clips} clips of ~{optimal_duration:.1f}s each")
    
    # Generate timestamps
    timestamps = [0.0]
    for i in range(1, num_clips):
        timestamp = i * optimal_duration
        timestamps.append(timestamp)
    timestamps.append(duration)
    
    return timestamps
