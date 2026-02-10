#!/bin/bash
# Example run script for NotebookLM Video Agent

set -e  # Exit on error

echo "🎬 NotebookLM Video Generator"
echo "=============================="

# Check if audio file exists
if [ ! -f "audio.mp3" ]; then
    echo "⚠️  Please add your NotebookLM audio as 'audio.mp3'"
    exit 1
fi

# Check if slides exist
if [ ! -d "slides" ] || [ -z "$(ls -A slides/)" ]; then
    echo "⚠️  Please add slides to the 'slides/' directory"
    exit 1
fi

# Create output directory
mkdir -p output

# Run the agent
echo "🚀 Generating video..."
python ../../notebooklm_video_agent.py \
    audio.mp3 \
    slides/ \
    -o output/video.mp4 \
    --resolution 1920x1080 \
    --fps 30

echo ""
echo "✅ Video generated successfully!"
echo "📁 Output: output/video.mp4"
echo ""
echo "Next steps:"
echo "1. Review the video"
echo "2. Check output/metadata.json for YouTube metadata"
echo "3. Upload to YouTube!"