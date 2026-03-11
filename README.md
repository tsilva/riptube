<div align="center">
  <img src="logo.png" alt="riptube" width="512"/>

  # riptube

  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
  [![yt-dlp](https://img.shields.io/badge/Powered%20by-yt--dlp-red.svg)](https://github.com/yt-dlp/yt-dlp)

  **📺 Download YouTube videos and extract audio with one command 🎵**

  [Installation](#installation) · [Usage](#usage) · [Options](#options)
</div>

## Overview

[![CI](https://github.com/tsilva/riptube/actions/workflows/release.yml/badge.svg)](https://github.com/tsilva/riptube/actions/workflows/release.yml)

A CLI tool for downloading YouTube videos and extracting audio tracks. Built on top of yt-dlp, it handles the complexities of video downloading with automatic format selection, audio extraction, and cookie support for restricted content.

## Features

- **Best quality by default** - Automatically selects the highest available video and audio quality
- **Audio extraction** - Extract audio tracks as MP3 files with a single flag
- **Cookie support** - Access age-restricted or private videos using browser cookies
- **Clean filenames** - Automatic sanitization of video titles for safe file names

## Installation

```bash
pipx install riptube
```

### Development install with uv

```bash
uv tool install . --editable
```

The package is published on PyPI as `riptube`, and the installed command is `riptube`.

If you want to use it as a Python package instead of the CLI:

```bash
pip install riptube
```

```python
import riptube
from riptube import download_video

print(riptube.__version__)
download_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

### Dependencies

| Dependency | Required | Purpose |
|------------|----------|---------|
| FFmpeg | Yes | Video/audio processing and merging |
| aria2 | No | Faster downloads (optional) |

**macOS:**
```bash
brew install ffmpeg aria2
```

**Linux:**
```bash
sudo apt install ffmpeg aria2
```

**Windows:**
Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

### Download a video

```bash
riptube https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Specify output file

```bash
riptube https://www.youtube.com/watch?v=dQw4w9WgXcQ -o video.mp4
```

### Extract audio only

```bash
riptube https://www.youtube.com/watch?v=dQw4w9WgXcQ -a
```

### Use cookies for restricted videos

```bash
riptube https://www.youtube.com/watch?v=dQw4w9WgXcQ -c cookies.txt
```

## Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output file path (default: auto-generated from video title) |
| `-a, --audio` | Extract audio track as MP3 |
| `-c, --cookies` | Path to Netscape format cookies.txt file |

## Development

```bash
# Clone and install in development mode
git clone https://github.com/tsilva/riptube.git
cd riptube
uv tool install . --editable

# Or install with pipx
pipx install . --force

# Run directly without installing
python -m riptube.cli <url>
```

## Releases

Bumping the version in `pyproject.toml` on `main` triggers the release workflow, which builds the package, publishes it to PyPI, and then creates the matching GitHub release. The workflow can also be re-run manually from GitHub via `workflow_dispatch`.

## License

[MIT](LICENSE)
