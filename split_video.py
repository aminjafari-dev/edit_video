#!/usr/bin/env python3
"""
TikTok Video Splitter - Command Line Interface

This script provides a simple command-line interface for splitting TikTok videos
into multiple clips using the VideoEditor class.

Usage Examples:
    # Split by specific timestamps
    python split_video.py --input video.mp4 --timestamps "0,15" "15,30" "30,45"
    
    # Split into equal parts
    python split_video.py --input video.mp4 --equal-parts 3
    
    # Auto-detect scenes
    python split_video.py --input video.mp4 --auto-detect
    
    # Get video information only
    python split_video.py --input video.mp4 --info
"""

import argparse
import sys
import os
from video_editor import VideoEditor


def parse_timestamps(timestamp_strings):
    """
    Parse timestamp strings into list of tuples.
    
    Args:
        timestamp_strings (list): List of timestamp strings like "0,15"
        
    Returns:
        list: List of (start_time, end_time) tuples
    """
    timestamps = []
    for ts_str in timestamp_strings:
        try:
            start, end = map(float, ts_str.split(','))
            timestamps.append((start, end))
        except ValueError:
            print(f"Error: Invalid timestamp format '{ts_str}'. Use format 'start,end'")
            sys.exit(1)
    return timestamps


def main():
    """Main function to handle command line arguments and execute video splitting."""
    parser = argparse.ArgumentParser(
        description="Split TikTok videos into multiple clips",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Split by specific timestamps
  python split_video.py --input video.mp4 --timestamps "0,15" "15,30" "30,45"
  
  # Split into 3 equal parts
  python split_video.py --input video.mp4 --equal-parts 3
  
  # Auto-detect scenes
  python split_video.py --input video.mp4 --auto-detect
  
  # Get video information
  python split_video.py --input video.mp4 --info
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input video file path'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        default='split_videos',
        help='Output directory for split clips (default: split_videos)'
    )
    
    parser.add_argument(
        '--timestamps', '-t',
        nargs='+',
        help='Timestamps for splitting in format "start,end" (e.g., "0,15" "15,30")'
    )
    
    parser.add_argument(
        '--equal-parts', '-e',
        type=int,
        help='Split video into N equal parts'
    )
    
    parser.add_argument(
        '--auto-detect', '-a',
        action='store_true',
        help='Automatically detect scenes and split accordingly'
    )
    
    parser.add_argument(
        '--threshold',
        type=float,
        default=30.0,
        help='Scene detection threshold (default: 30.0, higher = more sensitive)'
    )
    
    parser.add_argument(
        '--min-scene-duration',
        type=float,
        default=5.0,
        help='Minimum scene duration in seconds (default: 5.0)'
    )
    
    parser.add_argument(
        '--info',
        action='store_true',
        help='Show video information only (no splitting)'
    )
    
    parser.add_argument(
        '--output-prefix',
        default='clip',
        help='Prefix for output filenames (default: clip)'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    # Check that only one splitting method is specified
    splitting_methods = sum([
        args.timestamps is not None,
        args.equal_parts is not None,
        args.auto_detect
    ])
    
    if args.info:
        # Just show video information
        try:
            with VideoEditor(args.input, args.output_dir) as editor:
                info = editor.get_video_info()
                print("\n" + "="*50)
                print("VIDEO INFORMATION")
                print("="*50)
                print(f"File: {args.input}")
                print(f"Duration: {info['duration']:.2f} seconds")
                print(f"Resolution: {info['width']}x{info['height']}")
                print(f"Frame Rate: {info['fps']:.2f} FPS")
                print(f"Audio FPS: {info['audio_fps']:.2f}" if info['audio_fps'] else "Audio FPS: No audio")
                print(f"File Size: {info['file_size_mb']:.2f} MB")
                print("="*50)
        except Exception as e:
            print(f"Error getting video information: {e}")
            sys.exit(1)
        return
    
    if splitting_methods == 0:
        print("Error: Please specify a splitting method (--timestamps, --equal-parts, or --auto-detect)")
        parser.print_help()
        sys.exit(1)
    
    if splitting_methods > 1:
        print("Error: Please specify only one splitting method")
        parser.print_help()
        sys.exit(1)
    
    # Execute video splitting
    try:
        with VideoEditor(args.input, args.output_dir) as editor:
            print(f"\nProcessing video: {args.input}")
            print(f"Output directory: {args.output_dir}")
            
            if args.timestamps:
                print(f"\nSplitting by timestamps: {args.timestamps}")
                timestamps = parse_timestamps(args.timestamps)
                clips = editor.split_by_timestamps(timestamps, args.output_prefix)
                
            elif args.equal_parts:
                print(f"\nSplitting into {args.equal_parts} equal parts")
                clips = editor.split_into_equal_parts(args.equal_parts, args.output_prefix)
                
            elif args.auto_detect:
                print(f"\nAuto-detecting scenes (threshold: {args.threshold}, min duration: {args.min_scene_duration}s)")
                clips = editor.auto_split_by_scenes(
                    threshold=args.threshold,
                    min_scene_duration=args.min_scene_duration,
                    output_prefix=args.output_prefix
                )
            
            # Show results
            print(f"\n✅ Successfully created {len(clips)} video clips:")
            for i, clip_path in enumerate(clips, 1):
                file_size = os.path.getsize(clip_path) / (1024 * 1024)
                print(f"  {i:2d}. {os.path.basename(clip_path)} ({file_size:.2f} MB)")
            
            print(f"\nAll clips saved to: {os.path.abspath(args.output_dir)}")
            
    except Exception as e:
        print(f"\n❌ Error during video processing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()



