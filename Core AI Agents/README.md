🤖 NotebookLM Video AI Agent
Transform your NotebookLM audio podcasts into professional YouTube videos automatically.
📋 What This Agent Does
This AI agent automates the entire workflow from NotebookLM audio export to YouTube-ready video:
Audio Analysis - Detects natural segments and energy changes
Caption Generation - AI-powered transcription with Whisper
Visual Synchronization - Syncs slides/B-roll to audio timing
Professional Rendering - 1080p/4K output with smooth transitions
Metadata Generation - Creates descriptions, timestamps, tags
🎯 Quick Start
Installation
bash
Copy
# Clone or download the agent files
git clone <repository-url>
cd podcast-video-creation-from-ppt-and-audio

# Run setup script
chmod +x setup.sh
./setup.sh
Or manual installation:
bash
Copy
pip install moviepy librosa numpy Pillow
# Install FFmpeg on your system (required)
Basic Usage
Slide-based video:
bash
Copy
python notebooklm_video_agent.py \
    your_audio.mp3 \
    slides_folder/ \
    -o output_video.mp4
With captions:
bash
Copy
python notebooklm_video_agent.py \
    audio.mp3 \
    slides/ \
    -o video.mp4 \
    --captions
YouTube Shorts (vertical):
bash
Copy
python advanced_video_agent.py \
    --mode shorts \
    --hook "AMAZING DISCOVERY!" \
    audio.mp3 \
    -o shorts.mp4
📁 Project Structure
plain
Copy
my_video_project/
├── audio.mp3                 # NotebookLM export
├── slides/
│   ├── 01_intro.png         # Name sequentially
│   ├── 02_topic1.png
│   ├── 03_topic2.png
│   └── 04_conclusion.png
├── assets/
│   ├── logo.png             # Optional watermark
│   └── intro_music.mp3      # Optional background
├── output/
│   ├── video.mp4            # Generated video
│   └── metadata.json        # YouTube metadata
└── config.json              # Video settings
🎨 Video Styles
1. Slides Mode (--style slides)
Syncs static slides to audio duration
Best for: Educational content, presentations
Requirements: PNG/JPG images in folder
2. B-Roll Mode (--style broll)
AI selects relevant stock footage
Best for: Storytelling, dynamic content
Requirements: API keys for stock footage (optional)
3. Shorts Mode (--mode shorts)
Vertical 9:16 format
Mobile-optimized captions
Best for: YouTube Shorts, TikTok, Reels
⚙️ Configuration Options
Edit VideoConfig class or use CLI flags:
Table
Copy
Option	Description	Default
--resolution	Video resolution	1920x1080
--fps	Frames per second	30
--transition	Transition duration (sec)	0.5
--no-captions	Disable captions	false
--style	Visual style	slides
🔧 Advanced Features
AI Caption Generation
The agent uses OpenAI Whisper for accurate transcription:
Python
Copy
# In your script
agent = NotebookLMVideoAgent()
captions = agent.generate_captions("audio.mp3")
# Returns: [{'text': '...', 'start': 0.0, 'end': 3.5}, ...]
Content-Aware B-Roll
Automatically fetches relevant stock footage:
Python
Copy
agent = AdvancedVideoAgent()
agent.create_dynamic_b_roll(
    audio_path="audio.mp3",
    captions=captions,
    output_path="video.mp4"
)
Batch Processing
Process multiple videos:
bash
Copy
for audio in *.mp3; do
    python notebooklm_video_agent.py "$audio" slides/ -o "output/${audio%.mp3}.mp4"
done
📊 Workflow Integration
From NotebookLM to YouTube:
Export audio from NotebookLM
Create slides in Canva/Google Slides (16:9 format)
Export slides as PNG sequence
Run the AI agent
Upload to YouTube with generated metadata
Automation Ideas:
Webhook trigger: Auto-process when audio uploaded to Dropbox
Scheduled: Process daily/weekly content
Pipeline: Integrate with YouTube API for auto-upload
🛠️ Troubleshooting
Common Issues:
"FFmpeg not found"
bash
Copy
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
"MoviePy fails to render"
Ensure sufficient disk space (2-3x audio file size)
Check image dimensions match resolution setting
Try FFmpeg fallback mode
"Captions not accurate"
Install Whisper: pip install openai-whisper
Or manually edit generated captions.json
🚀 Performance Tips
Use SSD for temp files (set TEMP env variable)
Lower resolution for testing: --resolution 1280x720
Reduce FPS for static content: --fps 24
Batch process overnight for multiple videos
📝 Output Metadata
The agent generates a JSON file alongside your video:
JSON
Copy
{
  "input_audio": "podcast.mp3",
  "output_video": "video.mp4",
  "duration": 245.5,
  "segments": 12,
  "captions": [...],
  "suggested_title": "AI-Generated Title",
  "suggested_tags": ["ai", "technology", "podcast"],
  "timestamps": [
    {"time": "0:00", "label": "Introduction"},
    {"time": "1:30", "label": "Main Topic"}
  ]
}
🎓 Example Use Cases
Educational Channels: Turn NotebookLM study guides into videos
News Summaries: Daily podcast → YouTube video
Book Summaries: Chapter-by-chapter video series
Research Explainers: Academic papers → Accessible videos
📈 Future Enhancements
[ ] AI thumbnail generation
[ ] Auto-upload to YouTube API
[ ] Voice cloning for consistency
[ ] Multi-language caption translation
[ ] AI-generated B-roll with DALL-E/Stable Diffusion
🤝 Contributing
This is an open automation framework. Contributions welcome for:
Additional video styles
Stock footage API integrations
Better content analysis
GUI interface
📄 License
MIT License - Free for personal and commercial use.
Created for content creators who want to scale their NotebookLM content to YouTube automatically.
👤 Author
Mahesh Solanki (@twomathematicians-code)
GitHub: github.com/twomathematicians-code
Project: podcast-video-creation-from-ppt-and-audio
If this project helps you, please consider giving it a ⭐ on GitHub!