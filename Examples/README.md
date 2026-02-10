Example Project: NotebookLM to YouTube
This example demonstrates a complete workflow from NotebookLM export to YouTube upload.
Files
sample_podcast.mp3 - Example audio from NotebookLM (replace with your own)
slides/ - Sample slides showing proper naming convention
config.json - Custom configuration
run.sh - One-command script to generate video
Usage
bash
Copy
# Run the example
cd examples/basic_project
bash run.sh

# Output will be in output/ directory
Slide Creation Tips
Use 16:9 aspect ratio (1920x1080)
Name sequentially: 01_intro.png, 02_topic.png, etc.
Keep text minimal - let audio do the talking
Use high-contrast colors for readability
Customization
Edit config.json to change:
Video resolution
Caption style
Transition effects
Output format