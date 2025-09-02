#!/usr/bin/env python3
"""
Manual Video Splitter - Precise Control Over Cutting Points

This script allows you to manually specify exact timestamps for splitting
to avoid scene overlap and get clean cuts between TikTok shorts.
"""

import os
import subprocess
import sys
from typing import List, Tuple


def get_video_info(input_video: str) -> dict:
    """
    Get detailed video information using FFmpeg.
    
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


def preview_video_at_time(input_video: str, timestamp: float, duration: float = 5.0):
    """
    Create a preview clip around a specific timestamp to help identify scene boundaries.
    
    Args:
        input_video: Path to input video file
        timestamp: Time in seconds to preview around
        duration: Duration of preview clip in seconds
    """
    start_time = max(0, timestamp - duration/2)
    end_time = min(timestamp + duration/2, get_video_info(input_video)['duration'])
    
    preview_file = f"preview_{timestamp:.1f}s.mp4"
    
    cmd = [
        'ffmpeg',
        '-i', input_video,
        '-ss', str(start_time),
        '-t', str(end_time - start_time),
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-y',
        preview_file
    ]
    
    try:
        print(f"Creating preview around {timestamp:.1f}s...")
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"✅ Preview saved as: {preview_file}")
        print(f"   Preview shows: {start_time:.1f}s to {end_time:.1f}s")
        return preview_file
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating preview: {e}")
        return None


def split_video_by_timestamps(input_video: str, timestamps: List[Tuple[float, float]], 
                             output_dir: str = "manual_split", 
                             overlap_buffer: float = 0.0) -> List[str]:
    """
    Split video using precise timestamps with optional overlap buffer.
    
    Args:
        input_video: Path to input video file
        timestamps: List of (start_time, end_time) tuples in seconds
        output_dir: Directory to save output clips
        overlap_buffer: Buffer time to add around each scene (in seconds)
        
    Returns:
        List of paths to created video clips
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    output_paths = []
    
    print(f"Splitting video into {len(timestamps)} clips with precise timestamps...")
    if overlap_buffer > 0:
        print(f"Using overlap buffer: ±{overlap_buffer}s around each scene")
    
    for i, (start_time, end_time) in enumerate(timestamps, 1):
        # Apply overlap buffer if specified
        actual_start = max(0, start_time - overlap_buffer)
        actual_end = min(get_video_info(input_video)['duration'], end_time + overlap_buffer)
        
        # Calculate duration
        duration = actual_end - actual_start
        
        # Generate output filename
        output_filename = f"tiktok_short_{i:02d}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"\nProcessing clip {i}:")
        print(f"  Original: {start_time:.2f}s to {end_time:.2f}s")
        print(f"  With buffer: {actual_start:.2f}s to {actual_end:.2f}s (duration: {duration:.2f}s)")
        
        # Use FFmpeg to extract the clip with precise timing
        cmd = [
            'ffmpeg',
            '-i', input_video,
            '-ss', str(actual_start),
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
            print(f"  ✅ Saved as: {output_filename}")
            output_paths.append(output_path)
            
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Error: {e}")
            continue
    
    return output_paths


def interactive_timestamp_input(video_duration: float) -> List[Tuple[float, float]]:
    """
    Interactive input for timestamps with validation.
    
    Args:
        video_duration: Total duration of the video
        
    Returns:
        List of (start_time, end_time) tuples
    """
    print(f"\n🎬 Interactive Timestamp Input")
    print(f"Video duration: {video_duration:.2f} seconds")
    print("Enter the start and end time for each TikTok short.")
    print("Format: start_time,end_time (e.g., 0,15)")
    print("Press Enter without input to finish.\n")
    
    timestamps = []
    
    while True:
        try:
            user_input = input(f"Short #{len(timestamps) + 1} (start,end): ").strip()
            
            if not user_input:
                if timestamps:
                    break
                else:
                    print("Please enter at least one timestamp pair.")
                    continue
            
            # Parse input
            parts = user_input.split(',')
            if len(parts) != 2:
                print("❌ Invalid format. Use: start_time,end_time")
                continue
            
            start_time = float(parts[0])
            end_time = float(parts[1])
            
            # Validate timestamps
            if start_time < 0 or end_time > video_duration:
                print(f"❌ Timestamps must be between 0 and {video_duration:.2f}")
                continue
            
            if start_time >= end_time:
                print("❌ Start time must be less than end time")
                continue
            
            # Check for overlap with previous clips
            for prev_start, prev_end in timestamps:
                if (start_time < prev_end and end_time > prev_start):
                    print(f"⚠️  Warning: This clip overlaps with previous clip ({prev_start:.1f}s-{prev_end:.1f}s)")
                    response = input("Continue anyway? (y/n): ").lower()
                    if response != 'y':
                        continue
            
            timestamps.append((start_time, end_time))
            print(f"✅ Added: {start_time:.2f}s to {end_time:.2f}s")
            
        except ValueError:
            print("❌ Invalid number format. Please enter valid numbers.")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            return []
    
    return timestamps


def main():
    """Main function with interactive menu."""
    if len(sys.argv) < 2:
        print("Usage: python manual_split.py <input_video>")
        print("Example: python manual_split.py video.mp4")
        sys.exit(1)
    
    input_video = sys.argv[1]
    
    if not os.path.exists(input_video):
        print(f"Error: Input video file not found: {input_video}")
        sys.exit(1)
    
    # Get video information
    print("📹 Getting video information...")
    info = get_video_info(input_video)
    if not info:
        print("❌ Could not get video information")
        sys.exit(1)
    
    print(f"✅ Video loaded successfully:")
    print(f"   Duration: {info['duration']:.2f} seconds")
    print(f"   Resolution: {info['width']}x{info['height']}")
    print(f"   Frame Rate: {info['fps']:.2f} FPS")
    if info['audio_fps']:
        print(f"   Audio: {info['audio_fps']} Hz")
    print(f"   File Size: {info['file_size_mb']:.2f} MB")
    
    # Interactive menu
    while True:
        print("\n" + "="*50)
        print("🎬 MANUAL VIDEO SPLITTER")
        print("="*50)
        print("1. Preview video at specific time")
        print("2. Enter timestamps manually")
        print("3. Use preset timestamps (6 equal parts)")
        print("4. Exit")
        
        choice = input("\nChoose an option (1-4): ").strip()
        
        if choice == "1":
            try:
                timestamp = float(input("Enter time to preview (in seconds): "))
                if 0 <= timestamp <= info['duration']:
                    preview_video_at_time(input_video, timestamp)
                else:
                    print(f"❌ Time must be between 0 and {info['duration']:.2f}")
            except ValueError:
                print("❌ Invalid time format")
        
        elif choice == "2":
            timestamps = interactive_timestamp_input(info['duration'])
            if timestamps:
                overlap = input("Add overlap buffer around scenes? (seconds, default 0): ").strip()
                overlap_buffer = float(overlap) if overlap else 0.0
                
                clips = split_video_by_timestamps(input_video, timestamps, "manual_split", overlap_buffer)
                if clips:
                    print(f"\n🎉 Successfully created {len(clips)} clips!")
                    for i, clip_path in enumerate(clips, 1):
                        file_size = os.path.getsize(clip_path) / (1024 * 1024)
                        print(f"  {i:2d}. {os.path.basename(clip_path)} ({file_size:.2f} MB)")
        
        elif choice == "3":
            # Create 6 equal parts (since you mentioned there are 6 scenes)
            num_clips = 6
            clip_duration = info['duration'] / num_clips
            
            timestamps = []
            for i in range(num_clips):
                start_time = i * clip_duration
                end_time = (i + 1) * clip_duration
                timestamps.append((start_time, end_time))
            
            print(f"\n📏 Creating {num_clips} equal parts:")
            for i, (start, end) in enumerate(timestamps, 1):
                print(f"  {i:2d}. {start:.2f}s to {end:.2f}s ({end-start:.2f}s)")
            
            clips = split_video_by_timestamps(input_video, timestamps, "equal_parts")
            if clips:
                print(f"\n🎉 Successfully created {len(clips)} equal parts!")
        
        elif choice == "4":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
