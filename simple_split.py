#!/usr/bin/env python3
"""
Simple Video Splitter - Bypasses moviepy compatibility issues

This script provides a simpler approach to video splitting that should work
with your current setup.
"""

import os
import subprocess
import sys
from typing import List, Tuple


def split_video_by_timestamps(input_video: str, timestamps: List[Tuple[float, float]], 
                             output_dir: str = "split_videos") -> List[str]:
    """
    Split video using FFmpeg directly to avoid moviepy compatibility issues.
    
    Args:
        input_video: Path to input video file
        timestamps: List of (start_time, end_time) tuples in seconds
        output_dir: Directory to save output clips
        
    Returns:
        List of paths to created video clips
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    output_paths = []
    
    print(f"Splitting video into {len(timestamps)} clips...")
    
    for i, (start_time, end_time) in enumerate(timestamps, 1):
        # Calculate duration
        duration = end_time - start_time
        
        # Generate output filename
        output_filename = f"clip_{i:02d}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"Processing clip {i}: {start_time:.2f}s to {end_time:.2f}s (duration: {duration:.2f}s)")
        
        # Use FFmpeg directly to extract the clip
        cmd = [
            'ffmpeg',
            '-i', input_video,
            '-ss', str(start_time),
            '-t', str(duration),
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-avoid_negative_ts', 'make_zero',
            '-y',  # Overwrite output files
            output_path
        ]
        
        try:
            # Run FFmpeg command
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✅ Saved clip {i} to: {output_path}")
            output_paths.append(output_path)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating clip {i}: {e}")
            print(f"FFmpeg stderr: {e.stderr}")
            continue
    
    return output_paths


def split_video_into_equal_parts(input_video: str, num_clips: int, 
                                output_dir: str = "split_videos") -> List[str]:
    """
    Split video into equal duration parts.
    
    Args:
        input_video: Path to input video file
        num_clips: Number of equal parts to split into
        output_dir: Directory to save output clips
        
    Returns:
        List of paths to created video clips
    """
    # Get video duration using FFmpeg
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        input_video
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        print(f"Video duration: {duration:.2f} seconds")
    except subprocess.CalledProcessError as e:
        print(f"Error getting video duration: {e}")
        return []
    
    # Calculate duration per clip
    clip_duration = duration / num_clips
    
    # Generate timestamps for equal splitting
    timestamps = []
    for i in range(num_clips):
        start_time = i * clip_duration
        end_time = (i + 1) * clip_duration
        timestamps.append((start_time, end_time))
    
    print(f"Splitting {duration:.2f}s video into {num_clips} equal parts")
    print(f"Each clip will be approximately {clip_duration:.2f} seconds")
    
    return split_video_by_timestamps(input_video, timestamps, output_dir)


def get_video_info(input_video: str) -> dict:
    """
    Get video information using FFmpeg.
    
    Args:
        input_video: Path to input video file
        
    Returns:
        Dictionary with video information
    """
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        input_video
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        import json
        data = json.loads(result.stdout)
        
        # Extract relevant information
        format_info = data.get('format', {})
        video_stream = next((s for s in data.get('streams', []) if s.get('codec_type') == 'video'), {})
        audio_stream = next((s for s in data.get('streams', []) if s.get('codec_type') == 'audio'), {})
        
        info = {
            'duration': float(format_info.get('duration', 0)),
            'file_size_mb': float(format_info.get('size', 0)) / (1024 * 1024),
            'width': int(video_stream.get('width', 0)),
            'height': int(video_stream.get('height', 0)),
            'fps': eval(video_stream.get('r_frame_rate', '0/1')),
            'audio_fps': int(audio_stream.get('sample_rate', 0)) if audio_stream else None
        }
        
        return info
        
    except subprocess.CalledProcessError as e:
        print(f"Error getting video information: {e}")
        return {}


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 3:
        print("Usage: python simple_split.py <input_video> <num_clips>")
        print("Example: python simple_split.py video.mp4 7")
        sys.exit(1)
    
    input_video = sys.argv[1]
    num_clips = int(sys.argv[2])
    
    if not os.path.exists(input_video):
        print(f"Error: Input video file not found: {input_video}")
        sys.exit(1)
    
    # Get video information
    print("Getting video information...")
    info = get_video_info(input_video)
    if info:
        print(f"Duration: {info['duration']:.2f} seconds")
        print(f"Resolution: {info['width']}x{info['height']}")
        print(f"Frame Rate: {info['fps']:.2f} FPS")
        if info['audio_fps']:
            print(f"Audio Sample Rate: {info['audio_fps']} Hz")
        print(f"File Size: {info['file_size_mb']:.2f} MB")
    
    print(f"\nSplitting video into {num_clips} equal parts...")
    
    # Split the video
    clips = split_video_into_equal_parts(input_video, num_clips)
    
    if clips:
        print(f"\n✅ Successfully created {len(clips)} video clips:")
        for i, clip_path in enumerate(clips, 1):
            file_size = os.path.getsize(clip_path) / (1024 * 1024)
            print(f"  {i:2d}. {os.path.basename(clip_path)} ({file_size:.2f} MB)")
        
        print(f"\nAll clips saved to: {os.path.abspath('split_videos')}")
    else:
        print("❌ No clips were created successfully")


if __name__ == "__main__":
    main()
