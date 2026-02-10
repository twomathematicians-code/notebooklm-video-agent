from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="podcast-video-creation-from-ppt-and-audio",
    version="1.0.0",
    author="Mahesh Solanki",
    author_email="your.email@example.com",
    description="AI agent for converting NotebookLM audio to YouTube videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/twomathematicians-code/podcast-video-creation-from-ppt-and-audio",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Content Creators",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "notebooklm-video=notebooklm_video_agent:main",
            "notebooklm-video-advanced=advanced_video_agent:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)