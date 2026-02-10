# 🎬 Podcast Video Creation from PPT and Audio

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/twomathematicians-code/notebooklm-video-agent?style=social)](https://github.com/twomathematicians-code/notebooklm-video-agent/stargazers)

&gt; **AI-powered tool that converts audio podcasts and PowerPoint slides into professional YouTube videos automatically**

**By: [Mahesh Solanki](https://github.com/twomathematicians-code)** ([@twomathematicians-code](https://github.com/twomathematicians-code))

---

## 🎯 What Does This Tool Do?

**Podcast Video Creator** automatically converts audio files (from NotebookLM, podcasts, or recordings) into professional YouTube videos by synchronizing them with PowerPoint slides or images.

### The Problem It Solves
- You have great audio content (podcast, NotebookLM export, lecture recording)
- You have visual slides (PPT, Google Slides, Canva designs)
- **But** manually syncing them takes 2-4 hours per video
- **And** you need captions, transitions, and proper formatting for YouTube

### The Solution
This AI agent automates everything:
1. **🎵 Audio Analysis** - Detects natural segments and timing
2. **🖼️ Slide Sync** - Automatically matches slides to audio duration
3. **📝 AI Captions** - Generates accurate captions with OpenAI Whisper
4. **🎬 Video Rendering** - Outputs 1080p/4K with smooth transitions
5. **📊 Metadata** - Creates YouTube descriptions, timestamps, and tags

**⏱️ Time Saved: 2-4 hours → 5 minutes**

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/twomathematicians-code/notebooklm-video-agent.git
cd notebooklm-video-agent

# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg (required for video processing)
# macOS: brew install ffmpeg
# Ubuntu: sudo apt-get install ffmpeg
# Windows: https://ffmpeg.org/download.html
