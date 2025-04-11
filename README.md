# 🎬 youtube-downloader

<p align="center">
  <img src="logo.jpg" alt="PDF Unlocker Logo" width="400"/>
</p>

🎯 A simple CLI tool to download YouTube videos and extract audio tracks.

## 📖 Overview

YouTube Downloader is a command-line utility that lets you download videos from YouTube with the highest available quality. It handles the complexities of video downloading with features like audio extraction, custom output paths, and automatic fallback strategies to ensure successful downloads even when facing anti-bot protections.

Built on top of yt-dlp, this tool provides a simplified interface while maintaining powerful functionality for both casual users and power users.

## 🚀 Installation

```bash
pipx install . --force
```

Dependencies:
- FFmpeg (required for video/audio processing)
- aria2 (optional, for faster downloads)

### Installing Dependencies

**Linux:**
```bash
sudo apt update && sudo apt install ffmpeg aria2
```

**macOS:**
```bash
brew install ffmpeg aria2
```

**Windows:**
Download FFmpeg from: https://ffmpeg.org/download.html

## 🛠️ Usage

### Basic Download

```bash
youtube-downloader https://www.youtube.com/watch?v=XXXXXXXXXXX
```

### Specify Output File

```bash
youtube-downloader https://www.youtube.com/watch?v=XXXXXXXXXXX -o downloaded_video.mp4
```

### Extract Audio as MP3

```bash
youtube-downloader https://www.youtube.com/watch?v=XXXXXXXXXXX -a
```

### Using Browser Cookies (for restricted videos)

```bash
youtube-downloader https://www.youtube.com/watch?v=XXXXXXXXXXX -b chrome
```

### Combine Options

```bash
youtube-downloader https://www.youtube.com/watch?v=XXXXXXXXXXX -o music_video.mp4 -a -b firefox
```

## 📄 License

[MIT](LICENSE)