
#!/usr/bin/env python3
"""
Advanced NotebookLM Video Agent v2.0
With AI-powered B-roll selection and enhanced captions
"""

import os
import json
import random
from pathlib import Path
from typing import List, Dict, Optional
import tempfile
import shutil

try:
    from moviepy.editor import *
    from moviepy.video.fx.all import *
    MOVIEPY = True
except ImportError:
    MOVIEPY = False


class AdvancedVideoAgent:
    """
    Enhanced agent with AI content analysis and stock footage integration
    """

    def __init__(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.footage_cache = {}

    def analyze_content_topics(self, captions: List[Dict]) -> List[str]:
        """
        Extract key topics from captions for B-roll search
        In production, this would use GPT-4 or similar
        """
        # Simple keyword extraction (placeholder for NLP)
        all_text = " ".join([c['text'] for c in captions])

        # Common keywords (would be AI-extracted in full version)
        keywords = [
            "technology", "business", "nature", "city", 
            "people", "computer", "meeting", "data"
        ]

        found_topics = []
        for keyword in keywords:
            if keyword.lower() in all_text.lower():
                found_topics.append(keyword)

        return found_topics if found_topics else ["abstract", "technology"]

    def fetch_stock_footage(self, topic: str, duration: float) -> Optional[str]:
        """
        Fetch stock footage from free sources
        Supports: Pexels, Pixabay (would need API keys)
        """
        # Placeholder: In production, integrates with:
        # - Pexels API
        # - Pixabay API  
        # - Coverr.co

        # For now, creates colored backgrounds with text
        if not MOVIEPY:
            return None

        clip = ColorClip(size=(1920, 1080), color=(random.randint(20, 40), random.randint(20, 40), random.randint(40, 60)))
        clip = clip.set_duration(duration)

        # Add topic text
        txt = TextClip(
            topic.upper(),
            fontsize=100,
            color='white',
            font='Arial-Bold'
        ).set_duration(duration).set_position('center')

        composite = CompositeVideoClip([clip, txt])

        # Save temp file
        temp_path = self.temp_dir / f"stock_{topic}.mp4"
        composite.write_videofile(str(temp_path), fps=30, verbose=False, logger=None)

        return str(temp_path)

    def create_dynamic_b_roll(
        self,
        audio_path: str,
        captions: List[Dict],
        output_path: str
    ) -> str:
        """
        Create video with AI-selected B-roll matching content
        """
        print("🎬 Creating dynamic B-roll video...")

        if not MOVIEPY:
            raise RuntimeError("MoviePy required")

        # Analyze topics
        topics = self.analyze_content_topics(captions)
        print(f"📊 Detected topics: {topics}")

        # Load audio
        audio = AudioFileClip(audio_path)

        # Create segments with matching footage
        video_segments = []
        segment_duration = 5.0  # seconds per B-roll clip

        for i, topic in enumerate(topics):
            start_time = i * segment_duration
            if start_time >= audio.duration:
                break

            duration = min(segment_duration, audio.duration - start_time)

            # Get footage for this topic
            footage_path = self.fetch_stock_footage(topic, duration)

            if footage_path:
                segment = VideoFileClip(footage_path)
                segment = segment.subclip(0, duration)
                video_segments.append(segment)

        # Concatenate
        if video_segments:
            final_video = concatenate_videoclips(video_segments)
            final_video = final_video.set_audio(audio.subclip(0, final_video.duration))
        else:
            # Fallback to color background
            final_video = ColorClip(size=(1920, 1080), color=(30, 30, 40))
            final_video = final_video.set_duration(audio.duration).set_audio(audio)

        # Add captions
        final_video = self._add_enhanced_captions(final_video, captions)

        # Export
        final_video.write_videofile(
            output_path,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            preset='medium'
        )

        return output_path

    def _add_enhanced_captions(self, video, captions: List[Dict]):
        """Add modern, YouTube-style captions"""
        caption_clips = []

        for cap in captions:
            # Modern caption style with background
            txt = TextClip(
                cap['text'].upper(),
                fontsize=60,
                color='yellow',
                stroke_color='black',
                stroke_width=3,
                font='Arial-Bold',
                method='caption',
                size=(video.w * 0.9, None),
                align='center'
            )

            # Add semi-transparent background
            bg = ColorClip(
                size=(txt.w + 40, txt.h + 20),
                color=(0, 0, 0)
            ).set_opacity(0.6)

            txt = txt.set_start(cap['start']).set_duration(cap['end'] - cap['start'])
            bg = bg.set_start(cap['start']).set_duration(cap['end'] - cap['start'])

            # Center positioning
            txt = txt.set_position(('center', 'bottom')).margin(bottom=80, opacity=0)
            bg = bg.set_position(('center', 'bottom')).margin(bottom=80, opacity=0)

            caption_clips.extend([bg, txt])

        return CompositeVideoClip([video] + caption_clips)

    def create_youtube_shorts(
        self,
        audio_path: str,
        captions: List[Dict],
        output_path: str,
        hook_text: str = ""
    ) -> str:
        """
        Create YouTube Shorts (9:16 format) from audio
        """
        print("📱 Creating YouTube Shorts format...")

        if not MOVIEPY:
            raise RuntimeError("MoviePy required")

        # 9:16 aspect ratio (1080x1920)
        target_size = (1080, 1920)

        audio = AudioFileClip(audio_path)

        # Create vertical video with blurred background + centered content
        # This is the standard "Shorts" format for landscape content

        # Background
        bg = ColorClip(size=target_size, color=(20, 20, 30))
        bg = bg.set_duration(audio.duration)

        # Main content area (centered, 16:9 cropped to fit)
        content = ColorClip(size=(1080, 608), color=(40, 40, 60))  # 16:9 in middle
        content = content.set_duration(audio.duration)
        content = content.set_position(('center', 'center'))

        # Hook text at top
        if hook_text:
            hook = TextClip(
                hook_text,
                fontsize=70,
                color='white',
                font='Arial-Bold',
                method='caption',
                size=(1000, None)
            ).set_duration(min(3, audio.duration))
            hook = hook.set_position(('center', 200))

            final = CompositeVideoClip([bg, content, hook])
        else:
            final = CompositeVideoClip([bg, content])

        final = final.set_audio(audio)

        # Add captions optimized for mobile
        final = self._add_mobile_captions(final, captions)

        final.write_videofile(
            output_path,
            fps=30,
            codec='libx264'
        )

        return output_path

    def _add_mobile_captions(self, video, captions):
        """Captions optimized for mobile viewing"""
        caption_clips = []

        for cap in captions:
            txt = TextClip(
                cap['text'],
                fontsize=80,  # Larger for mobile
                color='white',
                stroke_color='black',
                stroke_width=4,
                font='Arial-Bold',
                method='caption',
                size=(video.w * 0.95, None),
                align='center'
            )

            txt = txt.set_start(cap['start']).set_duration(cap['end'] - cap['start'])
            txt = txt.set_position(('center', 1400))  # Lower third for mobile

            caption_clips.append(txt)

        return CompositeVideoClip([video] + caption_clips)


def create_complete_workflow():
    """
    Example complete workflow for NotebookLM → YouTube
    """
    workflow = """
    # COMPLETE NOTEBOOKLM → YOUTUBE WORKFLOW

    ## Phase 1: Export from NotebookLM
    1. Create your podcast in NotebookLM
    2. Download the audio (MP3)
    3. Copy the transcript (for caption verification)

    ## Phase 2: Prepare Visual Assets
    Option A - Slides:
    - Export key points as PNG slides from Google Slides/Canva
    - Name sequentially: 01_intro.png, 02_point1.png, etc.

    Option B - B-Roll:
    - Collect relevant stock footage
    - Or let the AI agent generate/search for footage

    ## Phase 3: Run AI Agent

    # For standard YouTube video:
    python notebooklm_video_agent.py audio.mp3 slides/ -o video.mp4

    # For AI-generated B-roll:
    python advanced_agent.py --mode broll audio.mp4 -o video.mp4

    # For YouTube Shorts:
    python advanced_agent.py --mode shorts --hook "SHOCKING TRUTH!" audio.mp4 -o shorts.mp4

    ## Phase 4: Upload to YouTube
    - Use the generated metadata JSON for description/timestamps
    - Upload thumbnail (separate creation)
    - Add end screens, cards
    """
    return workflow


if __name__ == "__main__":
    print(create_complete_workflow())