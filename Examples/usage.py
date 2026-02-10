#!/usr/bin/env python3
"""
Example: Using the NotebookLM Video Agent programmatically
"""

from notebooklm_video_agent import NotebookLMVideoAgent, VideoConfig

# Custom configuration
config = VideoConfig(
    output_resolution=(1920, 1080),
    fps=30,
    transition_duration=0.8,
    caption_enabled=True,
    caption_style="modern"
)

# Initialize agent
agent = NotebookLMVideoAgent(config)

# Process video
try:
    results = agent.process_notebooklm_export(
        audio_path="my_podcast.mp3",
        visual_assets_dir="my_slides/",
        output_path="youtube_video.mp4",
        style="slides"
    )

    print(f"✅ Video created: {results['output_video']}")
    print(f"⏱️  Duration: {results['segments'][-1]['end']:.1f} seconds")
    print(f"📝 Captions: {len(results['captions'])} segments")

    # Access generated metadata
    import json
    with open('video_metadata.json', 'w') as f:
        json.dump(results, f, indent=2)

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    agent.cleanup()


# Example 2: Batch processing multiple videos
import os
import glob

def batch_process(audio_dir: str, slides_base_dir: str, output_dir: str):
    """Process multiple NotebookLM exports at once"""

    agent = NotebookLMVideoAgent()

    audio_files = glob.glob(os.path.join(audio_dir, "*.mp3"))

    for audio_path in audio_files:
        basename = os.path.splitext(os.path.basename(audio_path))[0]
        slides_dir = os.path.join(slides_base_dir, basename)
        output_path = os.path.join(output_dir, f"{basename}.mp4")

        if not os.path.exists(slides_dir):
            print(f"⚠️  Skipping {basename} - no slides found")
            continue

        print(f"\n🎬 Processing {basename}...")

        try:
            agent.process_notebooklm_export(
                audio_path=audio_path,
                visual_assets_dir=slides_dir,
                output_path=output_path,
                style="slides"
            )
            print(f"✅ Complete: {output_path}")
        except Exception as e:
            print(f"❌ Failed: {e}")

    agent.cleanup()

# Uncomment to run batch processing:
# batch_process("audio/", "slides/", "output/")