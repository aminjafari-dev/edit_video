#!/usr/bin/env python3
"""
Video Editor Dependencies Setup Script

This script downloads and installs all dependencies needed for the Video Editor application.
It will install Python packages and FFmpeg binaries for video processing.

Usage:
    python setup_dependencies.py
    python3 setup_dependencies.py

Requirements:
    - Python 3.7+
    - pip (Python package installer)
    - Internet connection for downloading packages
"""

import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import tarfile
import shutil
from pathlib import Path
import json

# Configuration
PYTHON_PACKAGES = [
    "opencv-python",      # Computer vision library for video processing
    "numpy",              # Numerical computing library
    "pillow",             # Image processing library
    "tkinter",            # GUI framework (usually comes with Python)
    "pathlib",            # Path manipulation (Python 3.4+)
    "typing",             # Type hints (Python 3.5+)
]

# FFmpeg download URLs for different platforms
FFMPEG_URLS = {
    "Windows": {
        "url": "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
        "filename": "ffmpeg-windows.zip",
        "extract_dir": "ffmpeg-windows"
    },
    "Darwin": {  # macOS
        "url": "https://evermeet.cx/ffmpeg/getrelease/zip",
        "filename": "ffmpeg-macos.zip",
        "extract_dir": "ffmpeg-macos"
    },
    "Linux": {
        "url": "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz",
        "filename": "ffmpeg-linux.tar.xz",
        "extract_dir": "ffmpeg-linux"
    }
}

class DependencyInstaller:
    """Handles installation of all dependencies for the Video Editor application."""
    
    def __init__(self):
        """Initialize the installer with system information."""
        self.system = platform.system()
        self.python_version = sys.version_info
        self.project_root = Path(__file__).parent.absolute()
        self.downloads_dir = self.project_root / "downloads"
        self.ffmpeg_dir = self.project_root / "ffmpeg"
        
        # Create necessary directories
        self.downloads_dir.mkdir(exist_ok=True)
        self.ffmpeg_dir.mkdir(exist_ok=True)
        
        print(f"🚀 Video Editor Dependencies Setup")
        print(f"📁 Project Root: {self.project_root}")
        print(f"💻 System: {self.system}")
        print(f"🐍 Python Version: {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        print("=" * 60)
    
    def check_python_version(self):
        """Check if Python version meets requirements."""
        print("🔍 Checking Python version...")
        
        if self.python_version < (3, 7):
            print(f"❌ Python {self.python_version.major}.{self.python_version.minor} is not supported.")
            print("   Please install Python 3.7 or higher.")
            sys.exit(1)
        
        print(f"✅ Python {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro} is supported")
    
    def check_pip(self):
        """Check if pip is available and working."""
        print("🔍 Checking pip availability...")
        
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ pip is available: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ pip is not available or not working properly.")
            print("   Please install pip or ensure it's in your PATH.")
            return False
    
    def install_python_packages(self):
        """Install required Python packages using pip."""
        print("\n📦 Installing Python packages...")
        
        for package in PYTHON_PACKAGES:
            # Skip built-in packages
            if package in ["tkinter", "pathlib", "typing"]:
                print(f"   ⏭️  Skipping {package} (built-in package)")
                continue
            
            print(f"   📥 Installing {package}...")
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], capture_output=True, text=True, check=True)
                print(f"   ✅ {package} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Failed to install {package}: {e}")
                print(f"   Error output: {e.stderr}")
                return False
        
        print("✅ All Python packages installed successfully")
        return True
    
    def download_ffmpeg(self):
        """Download FFmpeg for the current platform."""
        print(f"\n🎬 Downloading FFmpeg for {self.system}...")
        
        if self.system not in FFMPEG_URLS:
            print(f"❌ Unsupported operating system: {self.system}")
            print("   Please install FFmpeg manually for your system.")
            return False
        
        ffmpeg_info = FFMPEG_URLS[self.system]
        download_path = self.downloads_dir / ffmpeg_info["filename"]
        
        print(f"   📥 Downloading from: {ffmpeg_info['url']}")
        print(f"   💾 Saving to: {download_path}")
        
        try:
            # Download FFmpeg
            urllib.request.urlretrieve(ffmpeg_info["url"], download_path)
            print(f"   ✅ Download completed: {download_path.stat().st_size / (1024*1024):.1f} MB")
            
            # Extract FFmpeg
            return self.extract_ffmpeg(download_path, ffmpeg_info)
            
        except Exception as e:
            print(f"   ❌ Download failed: {e}")
            return False
    
    def extract_ffmpeg(self, archive_path, ffmpeg_info):
        """Extract FFmpeg from downloaded archive."""
        print(f"   📦 Extracting FFmpeg...")
        
        try:
            if archive_path.suffix == ".zip":
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(self.downloads_dir)
            elif archive_path.suffix == ".tar.xz":
                with tarfile.open(archive_path, 'r:xz') as tar_ref:
                    tar_ref.extractall(self.downloads_dir)
            else:
                print(f"   ❌ Unsupported archive format: {archive_path.suffix}")
                return False
            
            print(f"   ✅ Extraction completed")
            
            # Move FFmpeg binaries to the project's ffmpeg directory
            return self.setup_ffmpeg_binaries(ffmpeg_info["extract_dir"])
            
        except Exception as e:
            print(f"   ❌ Extraction failed: {e}")
            return False
    
    def setup_ffmpeg_binaries(self, extract_dir):
        """Setup FFmpeg binaries in the project directory."""
        print(f"   🔧 Setting up FFmpeg binaries...")
        
        extracted_path = self.downloads_dir / extract_dir
        
        if not extracted_path.exists():
            print(f"   ❌ Extracted directory not found: {extracted_path}")
            return False
        
        try:
            # Find FFmpeg binaries
            ffmpeg_bin = None
            ffprobe_bin = None
            
            for root, dirs, files in os.walk(extracted_path):
                for file in files:
                    if file == "ffmpeg" or file == "ffmpeg.exe":
                        ffmpeg_bin = Path(root) / file
                    elif file == "ffprobe" or file == "ffprobe.exe":
                        ffprobe_bin = Path(root) / file
            
            if not ffmpeg_bin or not ffprobe_bin:
                print(f"   ❌ FFmpeg binaries not found in extracted files")
                return False
            
            # Copy binaries to project's ffmpeg directory
            shutil.copy2(ffmpeg_bin, self.ffmpeg_dir)
            shutil.copy2(ffprobe_bin, self.ffmpeg_dir)
            
            # Make binaries executable on Unix systems
            if self.system != "Windows":
                os.chmod(self.ffmpeg_dir / ffmpeg_bin.name, 0o755)
                os.chmod(self.ffmpeg_dir / ffprobe_bin.name, 0o755)
            
            print(f"   ✅ FFmpeg binaries setup completed")
            return True
            
        except Exception as e:
            print(f"   ❌ Setup failed: {e}")
            return False
    
    def create_requirements_txt(self):
        """Create a requirements.txt file for future use."""
        print("\n📝 Creating requirements.txt...")
        
        requirements_path = self.project_root / "requirements.txt"
        
        try:
            with open(requirements_path, 'w') as f:
                for package in PYTHON_PACKAGES:
                    if package not in ["tkinter", "pathlib", "typing"]:
                        f.write(f"{package}\n")
            
            print(f"   ✅ requirements.txt created: {requirements_path}")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create requirements.txt: {e}")
            return False
    
    def create_environment_script(self):
        """Create environment setup script for the current platform."""
        print("\n🔧 Creating environment setup script...")
        
        if self.system == "Windows":
            script_path = self.project_root / "setup_env.bat"
            script_content = f"""@echo off
REM Video Editor Environment Setup Script for Windows
echo Setting up Video Editor environment...

REM Add FFmpeg to PATH for this session
set PATH={self.ffmpeg_dir};%PATH%

REM Verify FFmpeg installation
ffmpeg -version
ffprobe -version

echo.
echo Environment setup completed!
echo You can now run: python run.py
pause
"""
        else:  # Unix-like systems (macOS, Linux)
            script_path = self.project_root / "setup_env.sh"
            script_content = f"""#!/bin/bash
# Video Editor Environment Setup Script for {self.system}
echo "Setting up Video Editor environment..."

# Add FFmpeg to PATH for this session
export PATH="{self.ffmpeg_dir}:$PATH"

# Verify FFmpeg installation
ffmpeg -version
ffprobe -version

echo ""
echo "Environment setup completed!"
echo "You can now run: python3 run.py"
"""
            # Make script executable
            os.chmod(script_path, 0o755)
        
        try:
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            print(f"   ✅ Environment script created: {script_path}")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create environment script: {e}")
            return False
    
    def verify_installation(self):
        """Verify that all dependencies are properly installed."""
        print("\n🔍 Verifying installation...")
        
        # Check Python packages
        print("   📦 Checking Python packages...")
        for package in PYTHON_PACKAGES:
            if package in ["tkinter", "pathlib", "typing"]:
                continue
            
            try:
                __import__(package.replace("-", "_"))
                print(f"      ✅ {package} is available")
            except ImportError:
                print(f"      ❌ {package} is not available")
                return False
        
        # Check FFmpeg
        print("   🎬 Checking FFmpeg...")
        ffmpeg_path = self.ffmpeg_dir / ("ffmpeg.exe" if self.system == "Windows" else "ffmpeg")
        ffprobe_path = self.ffmpeg_dir / ("ffprobe.exe" if self.system == "Windows" else "ffprobe")
        
        if not ffmpeg_path.exists():
            print(f"      ❌ FFmpeg not found: {ffmpeg_path}")
            return False
        
        if not ffprobe_path.exists():
            print(f"      ❌ FFprobe not found: {ffprobe_path}")
            return False
        
        print(f"      ✅ FFmpeg binaries found")
        
        # Test FFmpeg functionality
        try:
            result = subprocess.run([str(ffmpeg_path), "-version"], 
                                  capture_output=True, text=True, check=True)
            print(f"      ✅ FFmpeg is working: {result.stdout.split()[2]}")
        except subprocess.CalledProcessError:
            print(f"      ❌ FFmpeg test failed")
            return False
        
        print("✅ All dependencies verified successfully")
        return True
    
    def cleanup_downloads(self):
        """Clean up downloaded files to save space."""
        print("\n🧹 Cleaning up download files...")
        
        try:
            if self.downloads_dir.exists():
                shutil.rmtree(self.downloads_dir)
                print("   ✅ Download files cleaned up")
            return True
        except Exception as e:
            print(f"   ⚠️  Cleanup failed: {e}")
            return True  # Don't fail the installation for cleanup issues
    
    def run(self):
        """Run the complete installation process."""
        print("🚀 Starting Video Editor dependencies installation...\n")
        
        # Step 1: Check Python version
        self.check_python_version()
        
        # Step 2: Check pip
        if not self.check_pip():
            return False
        
        # Step 3: Install Python packages
        if not self.install_python_packages():
            return False
        
        # Step 4: Download and setup FFmpeg
        if not self.download_ffmpeg():
            return False
        
        # Step 5: Create requirements.txt
        if not self.create_requirements_txt():
            return False
        
        # Step 6: Create environment setup script
        if not self.create_environment_script():
            return False
        
        # Step 7: Verify installation
        if not self.verify_installation():
            return False
        
        # Step 8: Cleanup
        self.cleanup_downloads()
        
        print("\n" + "=" * 60)
        print("🎉 Installation completed successfully!")
        print("\n📋 Next steps:")
        print(f"   1. Run the environment setup script:")
        if self.system == "Windows":
            print(f"      {self.project_root / 'setup_env.bat'}")
        else:
            print(f"      {self.project_root / 'setup_env.sh'}")
        print(f"   2. Launch the application:")
        print(f"      python{'3' if self.system != 'Windows' else ''} run.py")
        print("\n📚 For more information, see the README.md file.")
        
        return True


def main():
    """Main entry point for the setup script."""
    try:
        installer = DependencyInstaller()
        success = installer.run()
        
        if success:
            print("\n✅ Setup completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Setup failed. Please check the error messages above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


