"""
Example Usage of VideoEditor Class

This script demonstrates various ways to use the VideoEditor class for
splitting TikTok videos into multiple clips.
"""

from video_editor import VideoEditor
import os


def example_split_by_timestamps():
    """
    Example: Split video by specific timestamps.
    
    This is useful when you know exactly where each TikTok short starts and ends.
    """
    print("=== Example 1: Split by Timestamps ===")
    
    # Replace with your actual video file path
    input_video = "your_tiktok_video.mp4"
    
    if not os.path.exists(input_video):
        print(f"Video file not found: {input_video}")
        print("Please update the input_video variable with your actual video file path")
        return
    
    # Define timestamps for splitting (start_time, end_time) in seconds
    # Example: Split a 60-second video into 4 clips of 15 seconds each
    timestamps = [
        (0, 15),    # First clip: 0 to 15 seconds
        (15, 30),   # Second clip: 15 to 30 seconds
        (30, 45),   # Third clip: 30 to 45 seconds
        (45, 60),   # Fourth clip: 45 to 60 seconds
    ]
    
    try:
        with VideoEditor(input_video, "clips_by_timestamps") as editor:
            clips = editor.split_by_timestamps(timestamps, "tiktok_clip")
            print(f"Created {len(clips)} clips by timestamps")
            
    except Exception as e:
        print(f"Error: {e}")


def example_split_into_equal_parts():
    """
    Example: Split video into equal duration parts.
    
    This is useful when you know how many TikTok shorts are in the video
    but don't know the exact timestamps.
    """
    print("\n=== Example 2: Split into Equal Parts ===")
    
    input_video = "your_tiktok_video.mp4"
    
    if not os.path.exists(input_video):
        print(f"Video file not found: {input_video}")
        print("Please update the input_video variable with your actual video file path")
        return
    
    # Number of equal parts to split into
    num_clips = 3  # Change this to match the number of TikTok shorts
    
    try:
        with VideoEditor(input_video, "clips_equal_parts") as editor:
            # Get video info first
            info = editor.get_video_info()
            print(f"Video duration: {info['duration']:.2f} seconds")
            print(f"Each clip will be approximately {info['duration'] / num_clips:.2f} seconds")
            
            clips = editor.split_into_equal_parts(num_clips, "equal_clip")
            print(f"Created {len(clips)} equal-duration clips")
            
    except Exception as e:
        print(f"Error: {e}")


def example_auto_detect_scenes():
    """
    Example: Automatically detect scenes and split accordingly.
    
    This is useful when you want the computer to automatically find
    the best places to split the video based on visual changes.
    """
    print("\n=== Example 3: Auto-Detect Scenes ===")
    
    input_video = "your_tiktok_video.mp4"
    
    if not os.path.exists(input_video):
        print(f"Video file not found: {input_video}")
        print("Please update the input_video variable with your actual video file path")
        return
    
    try:
        with VideoEditor(input_video, "clips_auto_detect") as editor:
            # Auto-detect scenes with custom settings
            clips = editor.auto_split_by_scenes(
                threshold=25.0,        # Lower threshold = more sensitive to changes
                min_scene_duration=3.0, # Minimum scene duration in seconds
                output_prefix="auto_scene"
            )
            print(f"Auto-detected and created {len(clips)} scene-based clips")
            
    except Exception as e:
        print(f"Error: {e}")


def example_get_video_info():
    """
    Example: Get detailed information about a video file.
    
    This is useful to understand your video before deciding how to split it.
    """
    print("\n=== Example 4: Get Video Information ===")
    
    input_video = "your_tiktok_video.mp4"
    
    if not os.path.exists(input_video):
        print(f"Video file not found: {input_video}")
        print("Please update the input_video variable with your actual video file path")
        return
    
    try:
        with VideoEditor(input_video) as editor:
            info = editor.get_video_info()
            
            print("Video Information:")
            print(f"  Duration: {info['duration']:.2f} seconds")
            print(f"  Resolution: {info['width']}x{info['height']}")
            print(f"  Frame Rate: {info['fps']:.2f} FPS")
            print(f"  Audio FPS: {info['audio_fps']:.2f}" if info['audio_fps'] else "  Audio FPS: No audio")
            print(f"  File Size: {info['file_size_mb']:.2f} MB")
            
            # Suggest splitting strategy based on duration
            duration = info['duration']
            if duration <= 30:
                print(f"\nSuggestion: This is a short video ({duration:.1f}s). Consider splitting into 2-3 parts.")
            elif duration <= 60:
                print(f"\nSuggestion: This is a medium video ({duration:.1f}s). Consider splitting into 3-4 parts.")
            else:
                print(f"\nSuggestion: This is a long video ({duration:.1f}s). Consider splitting into 4+ parts.")
                
    except Exception as e:
        print(f"Error: {e}")


def main():
    """
    Main function to run all examples.
    
    Before running, make sure to:
    1. Install required packages: pip install -r requirements.txt
    2. Update the input_video variable in each example function
    3. Ensure ffmpeg is installed on your system
    """
    print("TikTok Video Splitter - Example Usage")
    print("=" * 50)
    print("Before running these examples:")
    print("1. Install requirements: pip install -r requirements.txt")
    print("2. Update input_video paths in the example functions")
    print("3. Ensure ffmpeg is installed on your system")
    print("=" * 50)
    
    # Run examples
    example_get_video_info()
    example_split_by_timestamps()
    example_split_into_equal_parts()
    example_auto_detect_scenes()
    
    print("\n" + "=" * 50)
    print("All examples completed!")
    print("Check the output directories for your split video clips.")


if __name__ == "__main__":
    main()



