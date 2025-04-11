# YouTube Downloader

A simple command-line tool to download YouTube videos with the best available quality.

## Installation

You can install this tool directly using `pipx`:

```bash
pipx install . --force
```

## Usage

After installation, you can use the tool as follows:

```bash
youtube-downloader <video-url>
```

This will download the video to the current directory with the best resolution and encoding available.

### Options

- `-o, --output`: Specify the output directory (default is current directory)

Example:
```bash
youtube-downloader https://www.youtube.com/watch?v=dQw4w9WgXcQ -o ~/Videos
```

## Requirements

- Python 3.6+
- yt-dlp

## License

See the LICENSE file for details.