# YouTube Downloader

A robust command-line tool for downloading YouTube videos with the best possible quality.

## Features

- Downloads YouTube videos with the best available quality
- Supports specifying a custom output file path
- **Extracts audio tracks as MP3 files** (optional)
- Automatically cleans up partial downloads
- Implements progressive fallback to ensure successful downloads
- Sanitizes filenames to avoid special character issues
- Provides informative error messages and dependency checks

## Requirements

- Python 3.9 or higher
- FFmpeg (for video/audio merging and MP3 extraction)
- aria2 (optional, for faster downloads)

## Installation

### Using pipx (recommended)

The recommended way to install YouTube Downloader is with [pipx](https://pypa.github.io/pipx/):

```bash
# Install pipx if you don't have it
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install YouTube Downloader
pipx install git+https://github.com/tsilva/youtube-downloader.git
```

### Using pip

```bash
pip install git+https://github.com/tsilva/youtube-downloader.git
```

### From Source

```bash
git clone https://github.com/tsilva/youtube-downloader.git
cd youtube-downloader
pip install -e .
```

## Installing Dependencies

### Linux

```bash
sudo apt update
sudo apt install ffmpeg aria2
```

### macOS

```bash
brew install ffmpeg aria2
```

### Windows

Download and install FFmpeg from: https://ffmpeg.org/download.html

## Usage

### Basic Usage

```bash
youtube-downloader https://www.youtube.com/watch?v=XXXXXXXXXXX
```

This will download the video to the current directory with a filename based on the video title.

### Specify Output File

```bash
youtube-downloader https://www.youtube.com/watch?v=XXXXXXXXXXX -o downloaded_video.mp4
```

or

```bash
youtube-downloader https://www.youtube.com/watch?v=XXXXXXXXXXX -o /path/to/downloads/downloaded_video.mp4
```

### Extract Audio Track as MP3

```bash
youtube-downloader https://www.youtube.com/watch?v=XXXXXXXXXXX -a
```

This will download the video and also create an MP3 file with the same name.

You can combine with the output option:

```bash
youtube-downloader https://www.youtube.com/watch?v=XXXXXXXXXXX -o music_video.mp4 -a
```

This will create both `music_video.mp4` and `music_video.mp3`.

## Troubleshooting

### Common Issues

1. **403 Forbidden Errors**: These can happen due to YouTube's anti-bot protections. The program will automatically try alternative download strategies.

2. **Merge Errors**: If you see errors related to merging video and audio, make sure FFmpeg is properly installed and available in your PATH.

3. **Missing Dependencies**: The tool will notify you if FFmpeg or aria2 are missing and provide installation instructions.

## License

[MIT](LICENSE)

## Acknowledgments

- This tool uses [yt-dlp](https://github.com/yt-dlp/yt-dlp), a powerful YouTube download library
- Inspired by the need for a reliable YouTube downloading solution