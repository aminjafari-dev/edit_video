# Smart Video Splitter - Clean Project Structure

A professional, well-organized Python application for automatically detecting scene boundaries in videos and splitting them into individual clips with individual folder organization.

## 🏗️ Project Architecture

This project follows Clean Architecture principles with a clear separation of concerns:

```
clean_project/
├── core/                           # Core business logic and utilities
│   ├── utils/                      # Utility functions
│   │   └── video_utils.py         # Video information and utility functions
│   ├── detection/                  # Scene detection algorithms
│   │   └── scene_detection.py     # Advanced scene detection using FFmpeg
│   └── processing/                 # Video processing logic
│       ├── video_processor.py     # Video splitting and folder management
│       └── main_processor.py      # Main processing workflow orchestration
├── features/                       # Feature-specific modules
│   └── video_editor/              # Video editor GUI feature
│       ├── gui/                   # Main GUI components
│       │   ├── video_editor_gui.py # Main GUI class
│       │   └── README.md          # GUI documentation
│       ├── tabs/                  # GUI tab components
│       │   ├── help_tab.py        # Help and documentation tab
│       │   ├── logs_tab.py        # Processing logs tab
│       │   ├── processing_tab.py  # Progress and statistics tab
│       │   └── results_tab.py     # Results display tab
│       ├── widgets/               # Reusable GUI widgets
│       │   ├── sidebar.py         # Main control sidebar
│       │   └── status_bar.py      # Status display bar
│       ├── utils/                 # GUI utility functions
│       │   └── gui_utils.py       # Common GUI operations
│       └── main_gui.py            # Main GUI entry point
├── scripts/                        # Executable scripts
│   ├── smart_split_with_folders.py # Main CLI script
│   └── run.py                     # Alternative launcher
└── docs/                          # Documentation
    └── README.md                  # Original project documentation
```

## 🚀 Quick Start

### Command Line Interface
```bash
# From the clean_project directory
python scripts/smart_split_with_folders.py video.mp4
python scripts/run.py video.mp4
```

### GUI Interface
```bash
# From the clean_project directory
python features/video_editor/main_gui.py
```

## ✨ Key Features

- **Smart Scene Detection**: Multiple FFmpeg-based algorithms with intelligent fallbacks
- **Individual Folders**: Creates separate folders for each video's clips
- **Multiple Video Support**: Batch process multiple videos in one run
- **Modern GUI**: Professional interface with progress tracking and detailed logs
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **No Dependencies**: Uses only Python standard library and FFmpeg

## 🔧 Requirements

- Python 3.6+
- FFmpeg (must be installed and available in system PATH)

## 📋 Usage Examples

### Process a single video
```bash
python scripts/smart_split_with_folders.py my_video.mp4
```

### Process multiple videos
```bash
python scripts/smart_split_with_folders.py video1.mp4 video2.mp4 video3.mp4
```

### Process all MP4 files in current directory
```bash
python scripts/smart_split_with_folders.py *.mp4
```

### Launch GUI
```bash
python features/video_editor/main_gui.py
```

## 📁 Output Structure

The application creates a `smart_split/` directory with organized output:

```
smart_split/
├── video1_name/
│   ├── clip_01.mp4
│   ├── clip_02.mp4
│   └── clip_03.mp4
├── video2_name/
│   ├── clip_01.mp4
│   └── clip_02.mp4
└── ...
```

## 🏛️ Architecture Benefits

- **Clean Separation**: Core logic, GUI features, and scripts are clearly separated
- **Maintainability**: Each module has a single responsibility
- **Scalability**: Easy to add new features or modify existing ones
- **Testing**: Modular structure enables easy unit testing
- **Collaboration**: Multiple developers can work on different components
- **Documentation**: Comprehensive documentation for each component

## 🔍 Scene Detection Methods

1. **FFmpeg Scene Filter**: Primary method using FFmpeg's built-in scene detection
2. **Frame Difference Analysis**: Fallback method analyzing frame differences
3. **Intelligent Splitting**: Smart fallback based on video duration and characteristics

## 🎯 Use Cases

- **Content Creators**: Split long videos into shorter clips for social media
- **Video Editors**: Automatically segment videos for editing workflows
- **Educators**: Break down long lectures into digestible segments
- **Streamers**: Organize recorded streams into highlight clips

## 📚 Documentation

- **Core Documentation**: See `docs/README.md` for detailed technical information
- **GUI Documentation**: See `features/video_editor/README.md` for GUI-specific details
- **Code Comments**: All code is thoroughly documented with examples

## 🤝 Contributing

This project is open for contributions. The clean architecture makes it easy to:
- Add new scene detection algorithms
- Enhance the GUI with new features
- Improve video processing capabilities
- Add support for new video formats

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using Clean Architecture principles**
