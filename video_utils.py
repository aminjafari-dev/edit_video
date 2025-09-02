#!/usr/bin/env python3
"""
Video utility functions for getting video information and basic operations.
"""

import os
import subprocess
import json
from typing import Dict


def get_video_info(input_video: str) -> Dict:
    """Get detailed video information using FFmpeg."""
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
        data = json.loads(result.stdout)
        
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


def is_video_file(file_path: str) -> bool:
    """Check if a file is a valid video file based on extension."""
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')
    return file_path.lower().endswith(video_extensions)


def get_video_name(file_path: str) -> str:
    """Get the video filename without extension."""
    return os.path.splitext(os.path.basename(file_path))[0]
