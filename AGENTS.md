# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A CLI tool for downloading YouTube videos and extracting audio tracks, built on top of yt-dlp.

## Commands

### Installation
```bash
pipx install . --force
```

### Run directly (development)
```bash
python -m youtube_downloader.cli <url>
```

### After installation
```bash
youtube-downloader <url> [-o output.mp4] [-a] [-c cookies.txt]
```

## Architecture

Simple two-module structure:
- `cli.py` - Argument parsing and entry point (`main()`)
- `downloader.py` - Core download logic via `download_video()` function

The `download_video()` function wraps yt-dlp with options for cookies, custom output paths, and audio-only extraction.

## Dependencies

- **yt-dlp**: Core download library
- **FFmpeg**: Required for video/audio processing (external)
- **aria2**: Optional, for faster downloads (external)

## Project Guidelines

- README.md must be kept up to date with any significant project changes
