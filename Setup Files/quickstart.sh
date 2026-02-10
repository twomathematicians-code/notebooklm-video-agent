#!/bin/bash
# Quickstart script for new users

echo "🚀 NotebookLM Video Agent - Quickstart"
echo "======================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $PYTHON_VERSION"

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg not found!"
    echo ""
    echo "Please install FFmpeg:"
    echo "  macOS:   brew install ffmpeg"
    echo "  Ubuntu:  sudo apt-get install ffmpeg"
    echo "  Windows: https://ffmpeg.org/download.html"
    exit 1
fi

echo "✅ FFmpeg found"

# Setup virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "⬇️  Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your NotebookLM audio file to this directory"
echo "2. Create a 'slides/' folder with your slide images"
echo "3. Run: python notebooklm_video_agent.py your_audio.mp3 slides/ -o video.mp4"
echo ""
echo "For more options, see USAGE.md"