#!/bin/bash
# Setup script for NotebookLM Video AI Agent

echo "🚀 Setting up NotebookLM Video AI Agent..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "📊 Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "⬇️  Installing dependencies..."
pip install moviepy librosa numpy Pillow imageio[ffmpeg]

# Optional: Install Whisper for captions
echo "🎯 Install Whisper for AI captions? (y/n)"
read -r install_whisper
if [ "$install_whisper" = "y" ]; then
    pip install openai-whisper
fi

# Check FFmpeg
echo "🔍 Checking FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg found: $(ffmpeg -version | head -n1)"
else
    echo "⚠️  FFmpeg not found! Please install:"
    echo "   Mac: brew install ffmpeg"
    echo "   Ubuntu: sudo apt-get install ffmpeg"
    echo "   Windows: Download from ffmpeg.org"
fi

# Create project structure
echo "📁 Creating project structure..."
mkdir -p projects/my_first_video/slides
mkdir -p projects/my_first_video/output
mkdir -p projects/my_first_video/assets

# Create sample config
cat > projects/my_first_video/config.json << 'EOF'
{
  "video_style": "slides",
  "resolution": "1920x1080",
  "fps": 30,
  "captions_enabled": true,
  "caption_style": "youtube",
  "transition_duration": 0.5,
  "output_format": "mp4"
}
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Place your NotebookLM audio in: projects/my_first_video/"
echo "2. Add slide images to: projects/my_first_video/slides/"
echo "3. Run: python notebooklm_video_agent.py projects/my_first_video/audio.mp3 projects/my_first_video/slides/ -o projects/my_first_video/output/video.mp4"