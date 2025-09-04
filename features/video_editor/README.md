# Video Editor GUI - Separated Components

This directory contains the separated GUI components for the Video Editor application. The original monolithic `video_gui.py` file has been broken down into smaller, more manageable modules.

## Structure

```
src/gui/
├── __init__.py                 # Package initialization
├── video_editor_gui.py         # Main GUI class and entry point
├── widgets/                    # Reusable widget components
│   ├── __init__.py
│   ├── sidebar.py             # Sidebar with controls and options
│   └── status_bar.py          # Status bar widget
├── tabs/                       # Tab-based content areas
│   ├── __init__.py
│   ├── processing_tab.py      # Progress and statistics display
│   ├── logs_tab.py            # Processing logs and controls
│   ├── results_tab.py         # Results tree view
│   └── help_tab.py            # Help and documentation
└── utils/                      # Utility functions
    ├── __init__.py
    └── gui_utils.py           # Common GUI operations
```

## Components

### Main GUI Class (`video_editor_gui.py`)
- **Purpose**: Main application window and coordination
- **Responsibilities**: 
  - Window setup and styling
  - Component initialization
  - Event handling coordination
  - Thread management for processing

### Sidebar Widget (`widgets/sidebar.py`)
- **Purpose**: Left sidebar with all main controls
- **Features**:
  - File selection (single/multiple)
  - Processing options configuration
  - Control buttons (start/stop/preview)
  - Settings and preferences
  - Scene preview functionality

### Status Bar Widget (`widgets/status_bar.py`)
- **Purpose**: Bottom status display
- **Features**:
  - Current status messages
  - Version information

### Processing Tab (`tabs/processing_tab.py`)
- **Purpose**: Main processing interface
- **Features**:
  - Overall progress bar
  - Current file progress indicator
  - Status messages
  - Statistics display (file counts, clips, time)

### Logs Tab (`tabs/logs_tab.py`)
- **Purpose**: Detailed processing logs
- **Features**:
  - Timestamped log entries
  - Clear logs functionality
  - Save logs to file
  - Copy logs to clipboard

### Results Tab (`tabs/results_tab.py`)
- **Purpose**: Processing results display
- **Features**:
  - Tree view of processed videos
  - Clip counts and file sizes
  - Output folder information
  - Refresh and clear functionality

### Help Tab (`tabs/help_tab.py`)
- **Purpose**: User documentation and help
- **Features**:
  - Usage instructions
  - Feature descriptions
  - Troubleshooting guide
  - Tips and best practices

### GUI Utils (`utils/gui_utils.py`)
- **Purpose**: Common utility functions
- **Features**:
  - File operations
  - System-specific folder opening
  - Error handling and dialogs
  - Formatting utilities
  - Validation functions

## Usage

### Running the Separated GUI

1. **Direct execution**:
   ```bash
   python src/main_gui.py
   ```

2. **From the main directory**:
   ```bash
   python src/gui/video_editor_gui.py
   ```

### Importing Components

```python
# Import main GUI class
from src.gui.video_editor_gui import VideoEditorGUI

# Import individual components
from src.gui.widgets.sidebar import SidebarWidget
from src.gui.tabs.processing_tab import ProcessingTab
from src.gui.utils.gui_utils import GuiUtils

# Create and run the application
app = VideoEditorGUI()
app.run()
```

## Benefits of Separation

1. **Maintainability**: Each component has a single responsibility
2. **Reusability**: Components can be used independently
3. **Testing**: Easier to test individual components
4. **Collaboration**: Multiple developers can work on different components
5. **Debugging**: Easier to isolate and fix issues
6. **Code Organization**: Clear structure and separation of concerns

## Dependencies

The separated components maintain the same dependencies as the original:
- `tkinter` - GUI framework
- `main_processor` - Video processing logic
- `video_utils` - Video utility functions
- `scene_detection` - Scene detection algorithms
- `video_processor` - Video processing operations

## Testing

Use the provided test script to verify the separation works:

```bash
python test_separated_gui.py
```

This will test all imports and basic functionality of the separated components.

## Migration Notes

- The original `video_gui.py` file remains unchanged
- All functionality has been preserved in the separated components
- The main entry point (`main` function) is available in both files
- Import paths have been updated to use relative imports within the package

## Future Enhancements

With the separated structure, it's now easier to:
- Add new tabs or widgets
- Implement new features in isolated components
- Create different GUI themes or layouts
- Add unit tests for individual components
- Implement plugin architecture
- Create alternative interfaces (e.g., web-based)
