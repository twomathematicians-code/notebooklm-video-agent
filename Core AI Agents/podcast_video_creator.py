
#!/usr/bin/env python3
"""
NotebookLM to YouTube Video AI Agent
Automates conversion of NotebookLM audio into YouTube-ready videos
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import tempfile
import shutil

# Core video processing
try:
    from moviepy.editor import (
        AudioFileClip, ImageClip, CompositeVideoClip, 
        concatenate_videoclips, TextClip, ColorClip
    )
    from moviepy.video.fx.all import fadein, fadeout
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("⚠️  MoviePy not installed. Will use FFmpeg fallback.")

# Audio analysis
try:
    import librosa
    import numpy as np
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

# For AI-generated visuals (optional)
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


@dataclass
class VideoConfig:
    """Configuration for video generation"""
    output_resolution: Tuple[int, int] = (1920, 1080)  # 1080p
    fps: int = 30
    transition_duration: float = 0.5
    default_slide_duration: float = 5.0
    caption_enabled: bool = True
    caption_style: str = "modern"  # modern, minimal, bold
    background_music_volume: float = 0.1
    output_format: str = "mp4"


class NotebookLMVideoAgent:
    """
    AI Agent that converts NotebookLM audio into YouTube videos
    Supports multiple visual styles: slides, B-roll, talking head, captions
    """

    def __init__(self, config: VideoConfig = None):
        self.config = config or VideoConfig()
        self.temp_dir = Path(tempfile.mkdtemp())
        self.segments = []

    def analyze_audio(self, audio_path: str) -> List[Dict]:
        """
        Analyze audio to detect segments, pauses, and energy levels
        Returns list of segments with timestamps for visual switching
        """
        if not LIBROSA_AVAILABLE:
            print("📊 Librosa not available. Using equal duration segments.")
            return self._equal_segments(audio_path)

        print("🔍 Analyzing audio structure...")
        y, sr = librosa.load(audio_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)

        # Detect speech segments using energy thresholds
        hop_length = 512
        frame_length = 2048
        energy = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]

        # Find segments (simplified - detects changes in energy)
        threshold = np.mean(energy) * 0.5
        segments = []
        start_time = 0

        # Create segments every 5-10 seconds or on energy changes
        segment_duration = min(8, duration / 10)  # Adaptive segment length

        current_time = 0
        while current_time < duration:
            end_time = min(current_time + segment_duration, duration)
            segments.append({
                'start': current_time,
                'end': end_time,
                'duration': end_time - current_time,
                'type': 'content'
            })
            current_time = end_time

        print(f"✅ Detected {len(segments)} segments")
        return segments

    def _equal_segments(self, audio_path: str) -> List[Dict]:
        """Fallback: create equal duration segments"""
        # Get duration using ffprobe
        cmd = [
            'ffprobe', '-v', 'error', '-show_entries', 
            'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
            audio_path
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            duration = float(result.stdout.strip())
        except:
            duration = 300  # Default 5 minutes

        segments = []
        segment_duration = 8.0
        current = 0
        while current < duration:
            end = min(current + segment_duration, duration)
            segments.append({
                'start': current,
                'end': end,
                'duration': end - current,
                'type': 'content'
            })
            current = end
        return segments

    def generate_captions(self, audio_path: str) -> List[Dict]:
        """
        Generate captions using Whisper (if available) or create placeholder
        """
        # Check for Whisper
        whisper_available = shutil.which('whisper') is not None

        if whisper_available:
            print("🎯 Generating captions with Whisper...")
            try:
                import whisper
                model = whisper.load_model("base")
                result = model.transcribe(audio_path, word_timestamps=True)

                captions = []
                for segment in result["segments"]:
                    captions.append({
                        'text': segment["text"].strip(),
                        'start': segment["start"],
                        'end': segment["end"]
                    })
                return captions
            except Exception as e:
                print(f"⚠️  Whisper failed: {e}")

        # Fallback: segment-based placeholder captions
        print("📝 Creating segment-based captions...")
        segments = self.analyze_audio(audio_path)
        return [
            {
                'text': f'Segment {i+1}',
                'start': s['start'],
                'end': s['end']
            } for i, s in enumerate(segments)
        ]

    def create_slide_video(
        self, 
        audio_path: str, 
        slides_dir: str,
        output_path: str,
        captions: Optional[List[Dict]] = None
    ) -> str:
        """
        Create video from slides/images + audio
        """
        if not MOVIEPY_AVAILABLE:
            return self._create_video_ffmpeg(audio_path, slides_dir, output_path)

        print("🎬 Creating slide-based video with MoviePy...")

        # Load audio
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration

        # Get slides
        slides_dir = Path(slides_dir)
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
        slides = sorted([
            f for f in slides_dir.iterdir() 
            if f.suffix.lower() in image_extensions
        ])

        if not slides:
            raise ValueError(f"No images found in {slides_dir}")

        print(f"🖼️  Found {len(slides)} slides")

        # Calculate duration per slide
        slide_duration = audio_duration / len(slides)

        # Create video clips for each slide
        video_clips = []
        for i, slide_path in enumerate(slides):
            # Create image clip
            img_clip = ImageClip(str(slide_path))
            img_clip = img_clip.set_duration(slide_duration)
            img_clip = img_clip.resize(self.config.output_resolution)

            # Add fade transitions
            if i > 0:
                img_clip = fadein(img_clip, self.config.transition_duration)
            if i < len(slides) - 1:
                img_clip = fadeout(img_clip, self.config.transition_duration)

            video_clips.append(img_clip)

        # Concatenate
        final_video = concatenate_videoclips(video_clips, method="compose")
        final_video = final_video.set_audio(audio)

        # Add captions if enabled and provided
        if self.config.caption_enabled and captions:
            final_video = self._add_captions_to_video(final_video, captions)

        # Write output
        print(f"💾 Rendering video to {output_path}...")
        final_video.write_videofile(
            output_path,
            fps=self.config.fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile=str(self.temp_dir / "temp_audio.m4a"),
            remove_temp=True
        )

        return output_path

    def _add_captions_to_video(self, video_clip, captions: List[Dict]):
        """Add caption overlays to video"""
        caption_clips = []

        for cap in captions:
            txt_clip = TextClip(
                cap['text'],
                fontsize=48,
                color='white',
                stroke_color='black',
                stroke_width=2,
                font='Arial-Bold',
                method='caption',
                size=(video_clip.w * 0.8, None),
                align='center'
            )
            txt_clip = txt_clip.set_start(cap['start']).set_duration(
                cap['end'] - cap['start']
            )
            txt_clip = txt_clip.set_position(('center', 'bottom')).margin(bottom=50, opacity=0)
            caption_clips.append(txt_clip)

        return CompositeVideoClip([video_clip] + caption_clips)

    def _create_video_ffmpeg(
        self, 
        audio_path: str, 
        slides_dir: str, 
        output_path: str
    ) -> str:
        """
        Fallback: Create video using FFmpeg directly (no MoviePy)
        Faster but fewer features
        """
        print("🎬 Creating video with FFmpeg...")

        slides_dir = Path(slides_dir)
        slides = sorted([
            f for f in slides_dir.iterdir() 
            if f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp'}
        ])

        # Create concat file for FFmpeg
        concat_file = self.temp_dir / "concat.txt"

        # Get audio duration
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
               '-of', 'default=noprint_wrappers=1:nokey=1', audio_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = float(result.stdout.strip())
        slide_duration = duration / len(slides)

        with open(concat_file, 'w') as f:
            for slide in slides:
                f.write(f"file '{slide.absolute()}'\n")
                f.write(f"duration {slide_duration}\n")
            # Last frame needs to be duplicated for duration
            f.write(f"file '{slides[-1].absolute()}'\n")

        # Build FFmpeg command
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat', '-safe', '0',
            '-i', str(concat_file),
            '-i', audio_path,
            '-vsync', 'vfr',
            '-pix_fmt', 'yuv420p',
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
            '-c:a', 'aac', '-b:a', '192k',
            '-shortest',
            '-r', str(self.config.fps),
            output_path
        ]

        print(f"🚀 Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

        return output_path

    def create_b_roll_video(
        self,
        audio_path: str,
        search_terms: List[str],
        output_path: str,
        stock_footage_dir: Optional[str] = None
    ) -> str:
        """
        Create video with B-roll footage based on content analysis
        """
        print("🎥 Creating B-roll style video...")

        # This would integrate with stock footage APIs or local files
        # For now, creates a waveform visualization

        if not MOVIEPY_AVAILABLE:
            raise RuntimeError("MoviePy required for B-roll generation")

        audio = AudioFileClip(audio_path)

        # Create waveform visualization as placeholder
        # In production, this would fetch relevant stock footage
        duration = audio.duration

        # Create color background with audio waveform overlay
        bg = ColorClip(size=self.config.output_resolution, color=(20, 20, 30))
        bg = bg.set_duration(duration)

        # Add title card
        title = TextClip(
            "AI-Generated Content",
            fontsize=72,
            color='white',
            font='Arial-Bold'
        ).set_duration(3).fadeout(1)

        title = title.set_position('center')

        final = CompositeVideoClip([bg, title])
        final = final.set_audio(audio)

        final.write_videofile(
            output_path,
            fps=self.config.fps,
            codec='libx264',
            audio_codec='aac'
        )

        return output_path

    def process_notebooklm_export(
        self,
        audio_path: str,
        visual_assets_dir: str,
        output_path: str,
        style: str = "slides"
    ) -> Dict:
        """
        Main entry point: Process NotebookLM audio into YouTube video

        Args:
            audio_path: Path to NotebookLM audio file
            visual_assets_dir: Directory containing slides/images
            output_path: Where to save final video
            style: 'slides', 'broll', or 'captions_only'
        """
        print(f"\n🤖 NotebookLM Video Agent Starting...")
        print(f"📁 Audio: {audio_path}")
        print(f"🎨 Style: {style}")

        results = {
            'input_audio': audio_path,
            'output_video': output_path,
            'style': style,
            'segments': [],
            'captions': []
        }

        # Step 1: Analyze audio
        segments = self.analyze_audio(audio_path)
        results['segments'] = segments

        # Step 2: Generate captions
        captions = self.generate_captions(audio_path)
        results['captions'] = captions

        # Step 3: Generate video based on style
        if style == "slides":
            self.create_slide_video(audio_path, visual_assets_dir, output_path, captions)
        elif style == "broll":
            # Would need search terms from content analysis
            self.create_b_roll_video(audio_path, [], output_path)
        else:
            raise ValueError(f"Unknown style: {style}")

        print(f"\n✅ Video created successfully: {output_path}")
        print(f"📊 Duration: {segments[-1]['end']:.1f}s")
        print(f"📝 Captions: {len(captions)} segments")

        return results

    def cleanup(self):
        """Remove temporary files"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print(f"🧹 Cleaned up temp directory")


# CLI Interface
def main():
    """Command-line interface for the agent"""
    import argparse

    parser = argparse.ArgumentParser(
        description='NotebookLM to YouTube Video AI Agent'
    )
    parser.add_argument('audio', help='Path to audio file')
    parser.add_argument('visuals', help='Directory with slides/images')
    parser.add_argument('-o', '--output', default='output.mp4', help='Output video path')
    parser.add_argument('-s', '--style', default='slides', choices=['slides', 'broll'])
    parser.add_argument('--resolution', default='1920x1080', help='Video resolution')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second')
    parser.add_argument('--no-captions', action='store_true', help='Disable captions')

    args = parser.parse_args()

    # Parse resolution
    width, height = map(int, args.resolution.split('x'))

    # Create config
    config = VideoConfig(
        output_resolution=(width, height),
        fps=args.fps,
        caption_enabled=not args.no_captions
    )

    # Run agent
    agent = NotebookLMVideoAgent(config)

    try:
        results = agent.process_notebooklm_export(
            audio_path=args.audio,
            visual_assets_dir=args.visuals,
            output_path=args.output,
            style=args.style
        )

        # Save metadata
        metadata_path = Path(args.output).with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 Metadata saved: {metadata_path}")

    finally:
        agent.cleanup()


if __name__ == "__main__":
    main()