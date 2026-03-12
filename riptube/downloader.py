#!/usr/bin/env python3

import glob
import os
import re
import shutil
import sys

import yt_dlp

DEFAULT_OUTTMPL = '%(id)s - %(title)s.%(ext)s'
VIDEO_ID_PREFIX_RE = re.compile(r'^([A-Za-z0-9_-]{11}) - ')
VIDEO_ID_SUFFIX_RE = re.compile(r'\[([A-Za-z0-9_-]{11})\](?:\.[^.]+)?$')


def sanitize_filename(filename):
    """Sanitize filename to remove special characters that might cause issues."""
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', filename)
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized.strip('_')


def get_output_directory(output_template):
    """Return the directory where downloaded files will be written."""
    template_path = os.path.expanduser(output_template)
    directory = os.path.dirname(template_path)
    return directory or "."


def collect_existing_video_ids(directory):
    """Collect video IDs from existing filenames in the target directory."""
    existing_ids = set()
    if not os.path.isdir(directory):
        return existing_ids

    for entry in os.scandir(directory):
        if not entry.is_file():
            continue

        prefix_match = VIDEO_ID_PREFIX_RE.match(entry.name)
        if prefix_match:
            existing_ids.add(prefix_match.group(1))
            continue

        suffix_match = VIDEO_ID_SUFFIX_RE.search(entry.name)
        if suffix_match:
            existing_ids.add(suffix_match.group(1))

    return existing_ids


def looks_like_playlist_url(url):
    return "/playlist" in url or "list=" in url


def get_entry_url(entry):
    webpage_url = entry.get("webpage_url") or entry.get("original_url")
    if webpage_url:
        return webpage_url

    entry_url = entry.get("url")
    if entry_url and entry_url.startswith("http"):
        return entry_url

    video_id = entry.get("id")
    if video_id:
        return f"https://www.youtube.com/watch?v={video_id}"

    return None


def get_missing_playlist_urls(url, cookies_file, existing_ids):
    """Return missing playlist entry URLs by comparing entry IDs against local files."""
    info_opts = {
        'extract_flat': True,
        'ignoreerrors': True,
        'noplaylist': False,
        'quiet': True,
        'skip_download': True,
    }

    if cookies_file and os.path.isfile(cookies_file):
        info_opts['cookiefile'] = cookies_file

    with yt_dlp.YoutubeDL(info_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    if not isinstance(info, dict) or info.get('_type') != 'playlist':
        return None

    entries = [entry for entry in info.get('entries', []) if entry]
    missing_urls = []
    skipped_count = 0

    for entry in entries:
        video_id = entry.get('id')
        if video_id and video_id in existing_ids:
            skipped_count += 1
            continue

        entry_url = get_entry_url(entry)
        if entry_url:
            missing_urls.append(entry_url)

    return {
        'total_count': len(entries),
        'missing_urls': missing_urls,
        'playlist_title': info.get('title') or 'playlist',
        'skipped_count': skipped_count,
    }

def check_python_version():
    if sys.version_info < (3, 9):
        print("Warning: Python 3.8 is deprecated. Please use Python 3.9 or higher.")

def check_dependencies():
    if not shutil.which('ffmpeg'):
        print("Warning: FFmpeg not found. Install with:")
        print("  sudo apt install ffmpeg")
    # aria2c is optional, not needed for yt-dlp to work basically

def cleanup_part_files(directory="."):
    part_files = glob.glob(os.path.join(directory, "*.part"))
    for part_file in part_files:
        try:
            os.remove(part_file)
            print(f"Removed leftover part file: {os.path.basename(part_file)}")
        except Exception as e:
            print(f"Could not remove {part_file}: {e}")

def download_video(url, cookies_file=None, output=None, audio_only=False):
    """
    Download a YouTube video or playlist with given parameters.
    
    Args:
        url (str): YouTube video or playlist URL
        cookies_file (str, optional): Path to a Netscape format cookies.txt file
        output (str, optional): Output file path template
        audio_only (bool, optional): Extract audio as MP3
    
    Returns:
        bool: True if download was successful, False otherwise
    """
    check_python_version()
    check_dependencies()

    output_template = output or DEFAULT_OUTTMPL
    output_directory = get_output_directory(output_template)

    cleanup_part_files(output_directory)

    # Set yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
        'merge_output_format': 'mkv',  # yt-dlp merges to mkv by default
        'noplaylist': False,
        'quiet': False,
        'no_warnings': False,
        'verbose': True,
    }
    
    # Add output template if specified
    ydl_opts['outtmpl'] = output_template
    
    # Add cookies file if specified
    if cookies_file:
        if os.path.isfile(cookies_file):
            ydl_opts['cookiefile'] = cookies_file
        else:
            print(f"Warning: Cookies file not found: {cookies_file}")
    
    # Configure audio extraction if requested
    if audio_only:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        download_urls = [url]

        if looks_like_playlist_url(url):
            existing_ids = collect_existing_video_ids(output_directory)
            playlist_info = get_missing_playlist_urls(url, cookies_file, existing_ids)

            if playlist_info:
                skipped_count = playlist_info['skipped_count']
                total_count = playlist_info['total_count']
                download_urls = playlist_info['missing_urls']

                if skipped_count:
                    print(
                        f"Skipping {skipped_count} already-downloaded videos from "
                        f"{playlist_info['playlist_title']}."
                    )

                if total_count and not download_urls:
                    print(
                        f"All {total_count} videos from {playlist_info['playlist_title']} "
                        "are already present."
                    )
                    return True

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading: {url}")
            ydl.download(download_urls)
            return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False
    finally:
        cleanup_part_files(output_directory)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 youtube_downloader.py <YouTube URL>")
        sys.exit(1)

    url = sys.argv[1]
    success = download_video(url)
    sys.exit(0 if success else 1)
