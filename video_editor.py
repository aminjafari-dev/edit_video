"""
Video Editor Class for TikTok Video Processing

This class provides comprehensive video editing capabilities including:
- Splitting videos by timestamps
- Automatic scene detection
- Equal duration splitting
- Video format conversion
- Quality optimization

Usage Examples:
    # Split by specific timestamps
    editor = VideoEditor("input_video.mp4")
    editor.split_by_timestamps([(0, 15), (15, 30), (30, 45)])
    
    # Split into equal parts
    editor.split_into_equal_parts(3)
    
    # Auto-detect scenes and split
    editor.auto_split_by_scenes()
"""

import os
import cv2
import numpy as np
from moviepy import VideoFileClip, concatenate_videoclips
from typing import List, Tuple, Optional
import logging

# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VideoEditor:
    """
    A comprehensive video editing class for processing TikTok and other short-form videos.
    
    This class handles video splitting, scene detection, and format conversion
    with support for various input formats and output configurations.
    """
    
    def __init__(self, input_video_path: str, output_dir: str = "split_videos"):
        """
        Initialize the VideoEditor with input video and output directory.
        
        Args:
            input_video_path (str): Path to the input video file
            output_dir (str): Directory to save split video clips
        """
        self.input_video_path = input_video_path
        self.output_dir = output_dir
        self.video = None
        self.video_duration = 0
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Validate input video
        if not os.path.exists(input_video_path):
            raise FileNotFoundError(f"Input video not found: {input_video_path}")
        
        logger.info(f"VideoEditor initialized with: {input_video_path}")
        logger.info(f"Output directory: {output_dir}")
    
    def load_video(self) -> None:
        """
        Load the video file and get its properties.
        
        This method loads the video using MoviePy and extracts basic information
        like duration, resolution, and frame rate for processing.
        """
        try:
            logger.info("Loading video file...")
            self.video = VideoFileClip(self.input_video_path)
            self.video_duration = self.video.duration
            
            logger.info(f"Video loaded successfully:")
            logger.info(f"  Duration: {self.video_duration:.2f} seconds")
            logger.info(f"  Resolution: {self.video.size}")
            logger.info(f"  FPS: {self.video.fps}")
            
        except Exception as e:
            logger.error(f"Error loading video: {str(e)}")
            raise
    
    def split_by_timestamps(self, timestamps: List[Tuple[float, float]], 
                           output_prefix: str = "clip") -> List[str]:
        """
        Split video into clips based on specific timestamps.
        
        Args:
            timestamps (List[Tuple[float, float]]): List of (start_time, end_time) tuples in seconds
            output_prefix (str): Prefix for output filenames
            
        Returns:
            List[str]: List of paths to created video clips
            
        Example:
            timestamps = [(0, 15), (15, 30), (30, 45)]
            clips = editor.split_by_timestamps(timestamps)
        """
        if not self.video:
            self.load_video()
        
        output_paths = []
        
        try:
            logger.info(f"Splitting video into {len(timestamps)} clips...")
            
            for i, (start_time, end_time) in enumerate(timestamps):
                # Validate timestamps
                if start_time < 0 or end_time > self.video_duration:
                    logger.warning(f"Invalid timestamp for clip {i+1}: {start_time}-{end_time}")
                    continue
                
                if start_time >= end_time:
                    logger.warning(f"Invalid timestamp range for clip {i+1}: {start_time}-{end_time}")
                    continue
                
                # Extract subclip
                logger.info(f"Processing clip {i+1}: {start_time:.2f}s to {end_time:.2f}s")
                clip = self.video.subclipped(start_time, end_time)
                
                # Generate output filename
                output_filename = f"{output_prefix}_{i+1:02d}.mp4"
                output_path = os.path.join(self.output_dir, output_filename)
                
                # Save clip with optimized settings
                try:
                    clip.write_videofile(
                        output_path,
                        codec="libx264",
                        audio_codec="aac",
                        temp_audiofile="temp-audio.m4a",
                        remove_temp=True,
                        logger=None
                    )
                except Exception as e:
                    # Handle FFmpeg process detection issues
                    if "'NoneType' object has no attribute 'stdout'" in str(e):
                        logger.warning(f"FFmpeg process detection issue, retrying with simpler settings...")
                        clip.write_videofile(
                            output_path,
                            codec="libx264",
                            audio_codec="aac"
                        )
                    else:
                        raise e
                
                output_paths.append(output_path)
                logger.info(f"Saved clip {i+1} to: {output_path}")
                
                # Clean up clip to free memory
                clip.close()
            
            logger.info(f"Successfully created {len(output_paths)} video clips")
            return output_paths
            
        except Exception as e:
            logger.error(f"Error during video splitting: {str(e)}")
            raise
    
    def split_into_equal_parts(self, num_clips: int, 
                              output_prefix: str = "clip") -> List[str]:
        """
        Split video into equal duration parts.
        
        Args:
            num_clips (int): Number of equal parts to split the video into
            output_prefix (str): Prefix for output filenames
            
        Returns:
            List[str]: List of paths to created video clips
            
        Example:
            # Split a 60-second video into 3 equal parts (20 seconds each)
            clips = editor.split_into_equal_parts(3)
        """
        if not self.video:
            self.load_video()
        
        if num_clips <= 0:
            raise ValueError("Number of clips must be positive")
        
        if num_clips > self.video_duration:
            raise ValueError(f"Cannot split {self.video_duration}s video into {num_clips} clips")
        
        # Calculate duration per clip
        clip_duration = self.video_duration / num_clips
        
        # Generate timestamps for equal splitting
        timestamps = []
        for i in range(num_clips):
            start_time = i * clip_duration
            end_time = (i + 1) * clip_duration
            timestamps.append((start_time, end_time))
        
        logger.info(f"Splitting {self.video_duration:.2f}s video into {num_clips} equal parts")
        logger.info(f"Each clip will be approximately {clip_duration:.2f} seconds")
        
        return self.split_by_timestamps(timestamps, output_prefix)
    
    def auto_split_by_scenes(self, threshold: float = 30.0, 
                            min_scene_duration: float = 5.0,
                            output_prefix: str = "scene") -> List[str]:
        """
        Automatically detect scenes and split video accordingly.
        
        This method uses OpenCV to analyze frame differences and detect scene changes.
        It's useful when you don't know the exact timestamps but want to split
        at natural transition points.
        
        Args:
            threshold (float): Threshold for scene detection (higher = more sensitive)
            min_scene_duration (float): Minimum duration for a scene in seconds
            output_prefix (str): Prefix for output filenames
            
        Returns:
            List[str]: List of paths to created video clips
            
        Example:
            # Auto-detect scenes with default settings
            clips = editor.auto_split_by_scenes()
            
            # More sensitive detection with longer minimum scene duration
            clips = editor.auto_split_by_scenes(threshold=20.0, min_scene_duration=10.0)
        """
        if not self.video:
            self.load_video()
        
        try:
            logger.info("Detecting scenes automatically...")
            
            # Get scene change timestamps
            scene_timestamps = self._detect_scene_changes(threshold, min_scene_duration)
            
            if not scene_timestamps:
                logger.warning("No scenes detected, splitting into equal parts instead")
                return self.split_into_equal_parts(2)
            
            # Convert scene changes to clip timestamps
            timestamps = []
            for i in range(len(scene_timestamps) - 1):
                start_time = scene_timestamps[i]
                end_time = scene_timestamps[i + 1]
                if end_time - start_time >= min_scene_duration:
                    timestamps.append((start_time, end_time))
            
            # Add the last scene if it meets duration requirements
            if scene_timestamps and self.video_duration - scene_timestamps[-1] >= min_scene_duration:
                timestamps.append((scene_timestamps[-1], self.video_duration))
            
            logger.info(f"Detected {len(timestamps)} scenes")
            
            return self.split_by_timestamps(timestamps, output_prefix)
            
        except Exception as e:
            logger.error(f"Error during auto scene detection: {str(e)}")
            logger.info("Falling back to equal parts splitting...")
            return self.split_into_equal_parts(2)
    
    def _detect_scene_changes(self, threshold: float, min_scene_duration: float) -> List[float]:
        """
        Detect scene changes using OpenCV frame analysis.
        
        This is an internal method that analyzes consecutive frames to detect
        significant changes that indicate scene transitions.
        
        Args:
            threshold (float): Sensitivity threshold for scene detection
            min_scene_duration (float): Minimum duration between scenes
            
        Returns:
            List[float]: List of timestamps where scenes change
        """
        cap = cv2.VideoCapture(self.input_video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        scene_changes = [0.0]  # Start with first frame
        prev_frame = None
        frame_number = 0
        
        logger.info(f"Analyzing {frame_count} frames for scene changes...")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            current_time = frame_number / fps
            
            if prev_frame is not None:
                # Convert frames to grayscale for comparison
                gray_prev = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
                gray_current = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Calculate frame difference
                frame_diff = cv2.absdiff(gray_prev, gray_current)
                mean_diff = np.mean(frame_diff)
                
                # Check if this is a scene change
                if (mean_diff > threshold and 
                    current_time - scene_changes[-1] >= min_scene_duration):
                    scene_changes.append(current_time)
                    logger.debug(f"Scene change detected at {current_time:.2f}s (diff: {mean_diff:.2f})")
            
            prev_frame = frame.copy()
            frame_number += 1
            
            # Progress indicator
            if frame_number % 100 == 0:
                progress = (frame_number / frame_count) * 100
                logger.info(f"Scene detection progress: {progress:.1f}%")
        
        cap.release()
        
        # Add end time if not already present
        if scene_changes[-1] < self.video_duration:
            scene_changes.append(self.video_duration)
        
        logger.info(f"Scene detection complete. Found {len(scene_changes)} transition points")
        return scene_changes
    
    def get_video_info(self) -> dict:
        """
        Get comprehensive information about the loaded video.
        
        Returns:
            dict: Dictionary containing video properties
            
        Example:
            info = editor.get_video_info()
            print(f"Duration: {info['duration']} seconds")
            print(f"Resolution: {info['width']}x{info['height']}")
        """
        if not self.video:
            self.load_video()
        
        return {
            'duration': self.video_duration,
            'width': self.video.size[0],
            'height': self.video.size[1],
            'fps': self.video.fps,
            'audio_fps': self.video.audio.fps if self.video.audio else None,
            'file_size_mb': os.path.getsize(self.input_video_path) / (1024 * 1024)
        }
    
    def cleanup(self) -> None:
        """
        Clean up resources and close video files.
        
        This method should be called when you're done processing to free up
        memory and close file handles.
        """
        if self.video:
            self.video.close()
            self.video = None
            logger.info("Video resources cleaned up")
    
    def __enter__(self):
        """Context manager entry point."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point with automatic cleanup."""
        self.cleanup()



