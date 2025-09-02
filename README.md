# Smart Video Splitter with Individual Folders

A modular Python script that automatically detects scene boundaries in videos and splits them into individual clips, organizing each video's clips in its own folder.

## Features

- **Smart Scene Detection**: Uses multiple FFmpeg techniques to detect scene changes
- **Individual Folders**: Creates a separate folder for each input video
- **Multiple Video Support**: Process multiple videos in one run
- **Fallback Methods**: Multiple scene detection algorithms with intelligent fallbacks
- **Clean Organization**: Modular code structure for easy maintenance

## Project Structure

```
edit_video/
├── smart_split_with_folders.py  # Main entry point (now much smaller!)
├── run.py                       # Alternative launcher
├── video_utils.py              # Video information and utility functions
├── scene_detection.py          # Scene detection algorithms
├── video_processor.py          # Video splitting and folder management
├── main_processor.py           # Main processing workflow
└── README.md                   # This file
```

## Requirements

- Python 3.6+
- FFmpeg (must be installed and available in PATH)

## Installation

1. Ensure FFmpeg is installed on your system
2. Clone or download the project files
3. No additional Python packages required (uses only standard library)

## Usage

### Basic Usage

```bash
# Process a single video
python smart_split_with_folders.py video.mp4

# Process multiple videos
python smart_split_with_folders.py video1.mp4 video2.mp4 video3.mp4

# Process all MP4 files in current directory
python smart_split_with_folders.py *.mp4
```

### Alternative Launcher

```bash
python run.py video.mp4
```

## Output Structure

The script creates a `smart_split/` directory with subdirectories for each video:

```
smart_split/
├── video1/
│   ├── clip_01.mp4
│   ├── clip_02.mp4
│   └── clip_03.mp4
├── video2/
│   ├── clip_01.mp4
│   └── clip_02.mp4
└── ...
```

## How It Works

1. **Video Analysis**: Extracts video metadata (duration, resolution, FPS)
2. **Scene Detection**: Uses multiple algorithms to find scene boundaries:
   - FFmpeg scene filter
   - Frame difference analysis
   - Intelligent splitting based on video duration
3. **Video Splitting**: Cuts video at detected boundaries using FFmpeg
4. **Organization**: Creates individual folders for each video's clips

## Code Organization

- **`video_utils.py`**: Core video operations and information extraction
- **`scene_detection.py`**: All scene detection algorithms and methods
- **`video_processor.py`**: Video splitting, folder creation, and display functions
- **`main_processor.py`**: Main workflow orchestration
- **`smart_split_with_folders.py`**: Clean entry point (now only ~30 lines!)

## Benefits of Modular Structure

- **Maintainability**: Each module has a single responsibility
- **Reusability**: Functions can be imported and used independently
- **Testing**: Easier to test individual components
- **Readability**: Smaller files are easier to understand
- **Collaboration**: Multiple developers can work on different modules

## Troubleshooting

- **FFmpeg not found**: Ensure FFmpeg is installed and in your system PATH
- **Permission errors**: Check write permissions for the output directory
- **Large files**: Processing very large videos may take time and require sufficient disk space

## License

This project is open source and available under the MIT License.
