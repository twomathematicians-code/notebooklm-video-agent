Usage Guide
Table of Contents
Quick Start
Command Line Interface
Python API
Configuration
Video Styles
Troubleshooting
Quick Start
1. Installation
bash
Copy
# Clone repository
git clone https://github.com/twomathematicians-code/podcast-video-creation-from-ppt-and-audio.git
cd podcast-video-creation-from-ppt-and-audio

# Setup
chmod +x setup.sh
./setup.sh
2. First Video
bash
Copy
# Prepare your files
mkdir -p my_video/slides
# Copy your NotebookLM audio to my_video/audio.mp3
# Copy your slides (PNG/JPG) to my_video/slides/

# Generate video
python notebooklm_video_agent.py my_video/audio.mp3 my_video/slides/ -o my_video/output.mp4
Command Line Interface
Basic Syntax
bash
Copy
python notebooklm_video_agent.py <audio> <slides_dir> [options]
Arguments
Table
Copy
Argument	Description	Required
audio	Path to audio file (MP3, WAV, etc.)	Yes
slides_dir	Directory containing slide images	Yes
-o, --output	Output video path	No (default: output.mp4)
--resolution	Video resolution (WxH)	No (default: 1920x1080)
--fps	Frames per second	No (default: 30)
--style	Video style (slides/broll)	No (default: slides)
--no-captions	Disable captions	No
Examples
Standard YouTube video:
bash
Copy
python notebooklm_video_agent.py podcast.mp3 slides/ -o video.mp4
4K resolution:
bash
Copy
python notebooklm_video_agent.py podcast.mp3 slides/ -o video.mp4 --resolution 3840x2160
Without captions:
bash
Copy
python notebooklm_video_agent.py podcast.mp3 slides/ -o video.mp4 --no-captions
Fast rendering (lower quality):
bash
Copy
python notebooklm_video_agent.py podcast.mp3 slides/ -o video.mp4 --resolution 1280x720 --fps 24
Python API
Basic Usage
Python
Copy
from notebooklm_video_agent import NotebookLMVideoAgent, VideoConfig

# Configure
config = VideoConfig(
    output_resolution=(1920, 1080),
    fps=30,
    caption_enabled=True
)

# Create agent
agent = NotebookLMVideoAgent(config)

# Generate video
results = agent.process_notebooklm_export(
    audio_path="audio.mp3",
    visual_assets_dir="slides/",
    output_path="video.mp4",
    style="slides"
)

# Cleanup
agent.cleanup()
Advanced Usage
See examples/programmatic_usage.py for:
Batch processing
Custom configurations
Error handling
Metadata extraction
Configuration
VideoConfig Options
Python
Copy
@dataclass
class VideoConfig:
    output_resolution: Tuple[int, int] = (1920, 1080)  # 1080p default
    fps: int = 30
    transition_duration: float = 0.5  # Seconds
    default_slide_duration: float = 5.0
    caption_enabled: bool = True
    caption_style: str = "modern"  # modern, minimal, bold
    background_music_volume: float = 0.1
    output_format: str = "mp4"
JSON Configuration File
Create a config.json file:
JSON
Copy
{
  "video_settings": {
    "resolution": "1920x1080",
    "fps": 30
  },
  "captions": {
    "enabled": true,
    "style": "youtube",
    "font_size": 48
  }
}
Load it in Python:
Python
Copy
import json
from notebooklm_video_agent import VideoConfig

with open('config.json') as f:
    config_data = json.load(f)

config = VideoConfig(
    output_resolution=tuple(map(int, config_data['video_settings']['resolution'].split('x'))),
    fps=config_data['video_settings']['fps'],
    caption_enabled=config_data['captions']['enabled']
)
Video Styles
Slides Style
Best for: Educational content, presentations, tutorials
Static images synced to audio
Smooth transitions between slides
Caption overlay support
Requirements:
Folder of PNG/JPG images
Recommended: 1920x1080 resolution
Naming: Sequential (01_intro.png, 02_topic.png)
B-Roll Style (Advanced Agent)
Best for: Storytelling, dynamic content, news
AI-selected stock footage
Content-matched visuals
Automatic scene detection
Usage:
bash
Copy
python advanced_video_agent.py --mode broll audio.mp3 -o video.mp4
YouTube Shorts
Best for: Short-form content, mobile viewers
9:16 vertical format (1080x1920)
Mobile-optimized captions
Hook text overlay
Usage:
bash
Copy
python advanced_video_agent.py --mode shorts --hook "AMAZING!" audio.mp3 -o shorts.mp4
Troubleshooting
Common Issues
"FFmpeg not found"
bash
Copy
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
# Add to PATH
"MoviePy fails to render"
Check disk space (need 2-3x audio file size)
Verify image dimensions match resolution setting
Try: export TEMP=/path/to/large/disk before running
"Captions not accurate"
Install Whisper: pip install openai-whisper
Or manually edit the generated captions.json file
"Out of memory"
Reduce resolution: --resolution 1280x720
Process shorter segments
Close other applications
Performance Tips
Use SSD for temp files
Lower FPS for static content: --fps 24
Reduce resolution for testing
Batch process overnight
Getting Help
Check Issues for known problems
Open a new issue with:
Error message
Command you ran
System info (OS, Python version)
Sample files (if possible)