# TikTok Video Splitter

A powerful Python tool for splitting TikTok multi-short videos into individual clips. This tool uses advanced video processing techniques to automatically detect scene changes or allow manual timestamp-based splitting.

## Features

- **Multiple Splitting Methods**: Split by timestamps, equal parts, or automatic scene detection
- **Smart Scene Detection**: Uses OpenCV to automatically find the best splitting points
- **High-Quality Output**: Maintains video quality with optimized encoding settings
- **Flexible Output**: Customizable output directories and filename prefixes
- **Comprehensive Logging**: Detailed progress tracking and error reporting
- **Memory Efficient**: Uses context managers for automatic resource cleanup

## Installation

### Prerequisites

1. **Python 3.7+** - Download from [python.org](https://python.org)
2. **FFmpeg** - Required for video processing

#### Installing FFmpeg

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Windows:**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Add to your system PATH

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install moviepy opencv-python numpy Pillow
```

## Quick Start

### 1. Basic Usage

Split a video into equal parts:
```bash
python split_video.py --input your_video.mp4 --equal-parts 3
```

### 2. Split by Specific Timestamps

If you know the exact timestamps:
```bash
python split_video.py --input your_video.mp4 --timestamps "0,15" "15,30" "30,45"
```

### 3. Auto-Detect Scenes

Let the tool automatically find the best splitting points:
```bash
python split_video.py --input your_video.mp4 --auto-detect
```

### 4. Get Video Information

View video details before splitting:
```bash
python split_video.py --input your_video.mp4 --info
```

## Detailed Usage

### Command Line Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--input` | `-i` | Input video file path (required) | `--input video.mp4` |
| `--output-dir` | `-o` | Output directory for clips | `--output-dir my_clips` |
| `--timestamps` | `-t` | Split by specific timestamps | `--timestamps "0,15" "15,30"` |
| `--equal-parts` | `-e` | Split into N equal parts | `--equal-parts 4` |
| `--auto-detect` | `-a` | Automatically detect scenes | `--auto-detect` |
| `--threshold` | | Scene detection sensitivity (default: 30.0) | `--threshold 25.0` |
| `--min-scene-duration` | | Minimum scene duration in seconds (default: 5.0) | `--min-scene-duration 3.0` |
| `--output-prefix` | | Prefix for output filenames (default: clip) | `--output-prefix tiktok` |
| `--info` | | Show video information only | `--info` |

### Advanced Scene Detection

The auto-detect feature uses computer vision to find scene changes:

- **Lower threshold values** = More sensitive to changes (more clips)
- **Higher threshold values** = Less sensitive to changes (fewer clips)
- **Minimum scene duration** = Ensures clips aren't too short

```bash
# More sensitive detection
python split_video.py --input video.mp4 --auto-detect --threshold 20.0 --min-scene-duration 3.0

# Less sensitive detection
python split_video.py --input video.mp4 --auto-detect --threshold 40.0 --min-scene-duration 8.0
```

## Python API Usage

### Basic VideoEditor Usage

```python
from video_editor import VideoEditor

# Split by timestamps
with VideoEditor("input.mp4", "output_dir") as editor:
    timestamps = [(0, 15), (15, 30), (30, 45)]
    clips = editor.split_by_timestamps(timestamps, "clip")
    print(f"Created {len(clips)} clips")

# Split into equal parts
with VideoEditor("input.mp4", "output_dir") as editor:
    clips = editor.split_into_equal_parts(3, "part")
    print(f"Created {len(clips)} equal parts")

# Auto-detect scenes
with VideoEditor("input.mp4", "output_dir") as editor:
    clips = editor.auto_split_by_scenes(
        threshold=25.0,
        min_scene_duration=5.0,
        output_prefix="scene"
    )
    print(f"Auto-detected {len(clips)} scenes")
```

### Getting Video Information

```python
with VideoEditor("input.mp4") as editor:
    info = editor.get_video_info()
    print(f"Duration: {info['duration']:.2f} seconds")
    print(f"Resolution: {info['width']}x{info['height']}")
    print(f"Frame Rate: {info['fps']:.2f} FPS")
    print(f"File Size: {info['file_size_mb']:.2f} MB")
```

## Examples

### Example 1: Split TikTok Video into 3 Parts

```bash
# If you have a 60-second video with 3 TikTok shorts
python split_video.py --input tiktok_video.mp4 --equal-parts 3
```

This will create:
- `clip_01.mp4` (0-20 seconds)
- `clip_02.mp4` (20-40 seconds)  
- `clip_03.mp4` (40-60 seconds)

### Example 2: Split by Known Timestamps

```bash
# If you know the exact timestamps
python split_video.py --input tiktok_video.mp4 --timestamps "0,18" "18,35" "35,52"
```

### Example 3: Auto-Detect with Custom Settings

```bash
# More sensitive scene detection
python split_video.py --input tiktok_video.mp4 --auto-detect --threshold 20.0 --min-scene-duration 3.0
```

## Output

- **Format**: MP4 with H.264 video codec and AAC audio codec
- **Quality**: Maintains original video quality
- **Naming**: Sequential numbering with customizable prefixes
- **Directory**: Organized output in specified directory

## Troubleshooting

### Common Issues

**1. FFmpeg not found**
```
Error: [Errno 2] No such file or directory: 'ffmpeg'
```
**Solution**: Install FFmpeg and ensure it's in your system PATH

**2. Memory errors with large videos**
```
Error: MemoryError or similar
```
**Solution**: The tool automatically handles memory management, but ensure you have sufficient RAM

**3. Audio missing in output**
```
Output clips have no audio
```
**Solution**: Check if input video has audio track, some TikTok downloads may not include audio

**4. Scene detection not working**
```
No scenes detected, falling back to equal parts
```
**Solution**: Adjust threshold and min-scene-duration parameters

### Performance Tips

- **Large videos**: Scene detection may take several minutes for very long videos
- **Memory usage**: The tool automatically manages memory, but close other applications if needed
- **Processing speed**: Depends on video length, resolution, and system performance

## File Structure

```
edit_video/
├── video_editor.py          # Main VideoEditor class
├── split_video.py           # Command-line interface
├── example_usage.py         # Usage examples
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── split_videos/           # Output directory (created automatically)
    ├── clip_01.mp4
    ├── clip_02.mp4
    └── ...
```

## Technical Details

### Dependencies

- **MoviePy**: Video processing and editing
- **OpenCV**: Computer vision for scene detection
- **NumPy**: Numerical computations
- **Pillow**: Image processing support

### Architecture

The tool follows a clean, modular design:

1. **VideoEditor Class**: Core functionality for video processing
2. **Scene Detection**: OpenCV-based frame analysis
3. **Video Splitting**: MoviePy subclip extraction
4. **Output Management**: Organized file saving and cleanup

### Supported Formats

- **Input**: MP4, AVI, MOV, MKV, and other FFmpeg-supported formats
- **Output**: MP4 (H.264 + AAC) for maximum compatibility

## Contributing

Feel free to contribute improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure all dependencies are installed
3. Verify FFmpeg is properly installed
4. Check the video file format and integrity

For additional help, please open an issue with:
- Your operating system
- Python version
- Error message
- Video file details (format, size, duration)



