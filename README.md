# 🎬 YouTube Downloader

🔽 A simple CLI tool to download YouTube videos with the best available quality

## 📖 Overview

YouTube Downloader is a command-line utility that lets you download YouTube videos in the highest quality available. Built on top of yt-dlp, it handles format selection, filename sanitization, and dependency management automatically. The tool includes fallback mechanisms to ensure successful downloads even when the best quality isn't available.

## 🚀 Installation

Install the tool using pipx:

```bash
pipx install . --force
```

## 🛠️ Usage

After installation, download videos with a simple command:

```bash
youtube-downloader <video-url>
```

This downloads the video to your current directory with the best resolution and encoding available.

### Options

```bash
youtube-downloader https://www.youtube.com/watch?v=dQw4w9WgXcQ -o ~/Videos
```

Available options:
- `-o, --output`: Specify the output directory (default: current directory)

## ✨ Features

- Downloads videos in best quality (up to 1080p)
- Sanitizes filenames automatically
- Uses aria2 for faster downloads on Linux/macOS
- Handles browser cookies for access to restricted videos
- Includes multiple fallback strategies for reliable downloads
- Cleans up partial downloads automatically

## 🧰 Requirements

- Python 3.8+ (3.9+ recommended)
- FFmpeg
- aria2 (recommended on Linux/macOS)

## 📄 License

This project is licensed under the [MIT License](LICENSE).

AI: I've created a clean, modern README for your YouTube Downloader project. The README highlights the key features and functionality while providing clear installation and usage instructions. I've organized it with emojis for better readability and included all the essential information a user would need to get started with your tool.