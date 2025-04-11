#!/usr/bin/env python3

import os
import re
import sys
import glob
import shutil
import yt_dlp

def sanitize_filename(filename):
    """Sanitize filename to remove special characters that might cause issues."""
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', filename)
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized.strip('_')

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

def download_video(url, cookies_file=None, output=None, audio_only=False, browser="none"):
    """
    Download a video from YouTube with given parameters.
    
    Args:
        url (str): YouTube video URL
        cookies_file (str, optional): Path to a Netscape format cookies.txt file
        output (str, optional): Output file path template
        audio_only (bool, optional): Extract audio as MP3
        browser (str, optional): Browser to extract cookies from as fallback
    
    Returns:
        bool: True if download was successful, False otherwise
    """
    check_python_version()
    check_dependencies()

    cleanup_part_files()

    # Set yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
        'merge_output_format': 'mkv',  # yt-dlp merges to mkv by default
        'quiet': False,
        'no_warnings': False,
        'verbose': True,
    }
    
    # Add output template if specified
    if output:
        ydl_opts['outtmpl'] = output
    else:
        ydl_opts['outtmpl'] = '%(title)s [%(id)s].%(ext)s'
    
    # Add cookies file if specified
    if cookies_file:
        if os.path.isfile(cookies_file):
            ydl_opts['cookiefile'] = cookies_file
        else:
            print(f"Warning: Cookies file not found: {cookies_file}")
    
    # Configure browser cookies if specified and not 'none'
    if browser and browser.lower() != "none":
        ydl_opts['cookiesfrombrowser'] = (browser, None, None, None)
    
    # Configure audio extraction if requested
    if audio_only:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading: {url}")
            ydl.download([url])
            return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False
    finally:
        cleanup_part_files()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 youtube_downloader.py <YouTube URL>")
        sys.exit(1)

    url = sys.argv[1]
    success = download_video(url)
    sys.exit(0 if success else 1)
