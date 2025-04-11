#!/usr/bin/env python3
import os
import re
import sys
import glob
import shutil
import platform
import subprocess
import yt_dlp

def sanitize_filename(filename):
    """Sanitize filename to remove special characters that might cause issues."""
    # Replace problematic characters with underscore
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', filename)
    # Replace multiple underscores with a single one
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized

def check_python_version():
    """Check if Python version is supported and print warning if needed."""
    python_version = sys.version_info
    if (python_version.major == 3 and python_version.minor < 9):
        print("Deprecated Feature: Support for Python version 3.8 has been deprecated. Please update to Python 3.9 or above")

def check_dependencies():
    """Check if required external dependencies are available."""
    missing_deps = []
    
    # Check FFmpeg
    if not shutil.which('ffmpeg'):
        missing_deps.append('FFmpeg')
    
    # Check aria2c on Linux systems
    if platform.system() != 'Windows' and not shutil.which('aria2c'):
        missing_deps.append('aria2')
    
    if missing_deps:
        print(f"Warning: Missing dependencies: {', '.join(missing_deps)}")
        print("\nInstallation instructions:")
        if 'FFmpeg' in missing_deps:
            if platform.system() == 'Linux':
                print("  FFmpeg: sudo apt install ffmpeg")
            elif platform.system() == 'Darwin':  # macOS
                print("  FFmpeg: brew install ffmpeg")
            else:
                print("  FFmpeg: https://ffmpeg.org/download.html")
        
        if 'aria2' in missing_deps:
            if platform.system() == 'Linux':
                print("  aria2: sudo apt install aria2")
            elif platform.system() == 'Darwin':  # macOS
                print("  aria2: brew install aria2")
        
        return False
    return True

def cleanup_part_files(directory=None):
    """Clean up any leftover .part files in the specified directory."""
    if directory is None:
        directory = os.getcwd()
        
    # Find and remove all .part files in the directory
    part_files = glob.glob(os.path.join(directory, "*.part"))
    for part_file in part_files:
        try:
            os.remove(part_file)
            print(f"Cleaned up leftover file: {os.path.basename(part_file)}")
        except OSError as e:
            print(f"Warning: Could not remove {part_file}: {str(e)}")

def download_video(url, output_path=None):
    """
    Download YouTube video with the best quality available.
    
    Args:
        url: URL of the YouTube video
        output_path: Optional path for the output file. If not specified, 
                    filename will be auto-generated from video title.
    """
    try:
        # Check Python version
        check_python_version()
        
        # Check dependencies
        has_dependencies = check_dependencies()
        
        # Determine output directory and filename
        if output_path:
            output_dir = os.path.dirname(output_path)
            output_filename = os.path.basename(output_path)
            if not output_dir:  # If only filename was provided
                output_dir = os.getcwd()
                output_path = os.path.join(output_dir, output_filename)
        else:
            output_dir = os.getcwd()
            output_filename = None  # Will be determined from video title
        
        # Create output directory if it doesn't exist
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create options with pre-configured PO tokens
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'merge_output_format': 'mp4',
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': True,
            'geo_bypass': True,
            'nocheckcertificate': True,
            'extractor_retries': 3,
            'file_access_retries': 3,
            'fragment_retries': 3,
            'skip_download_archive': True,
            'cookiesfrombrowser': ('firefox',),  # Try to use browser cookies
            # Better handling of filenames
            'restrictfilenames': True,
            # Avoid PO token warnings
            'extractor_args': {
                'youtube': {
                    'player_client': ['web'],  # Use only web client to avoid PO token errors
                    'player_skip': ['js', 'configs'],  # Skip problematic player extractions
                }
            },
        }
        
        # Add external downloader if aria2c is available
        if platform.system() != 'Windows' and shutil.which('aria2c'):
            ydl_opts.update({
                'external_downloader': 'aria2c',
                'external_downloader_args': ['--min-split-size=1M', '--max-connection-per-server=16', '--retry-wait=2'],
            })
        
        # Clean up any leftover .part files before starting
        cleanup_part_files(output_dir)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # First extract info without downloading
            info = ydl.extract_info(url, download=False)
            if not info:
                raise Exception("Could not retrieve video information")
                
            video_title = info.get('title', 'Video')
            
            # If custom output path is specified, use it; otherwise, use sanitized title
            if output_filename:
                # Force mp4 extension if not specified
                if not os.path.splitext(output_filename)[1]:
                    output_filename += '.mp4'
                ydl_opts['outtmpl'] = output_path
            else:
                sanitized_title = sanitize_filename(video_title)
                ydl_opts['outtmpl'] = os.path.join(output_dir, sanitized_title + '.%(ext)s')
            
            # Download the video
            print(f"Downloading: {video_title}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Get the actual filename that was downloaded
            if output_filename:
                downloaded_file = output_path
            else:
                # Find the newest mp4 file in the directory that matches our sanitized title
                mp4_files = glob.glob(os.path.join(output_dir, sanitized_title + ".mp4"))
                if mp4_files:
                    downloaded_file = mp4_files[0]
                else:
                    downloaded_file = "unknown"
            
            print(f"Downloaded: {video_title} successfully to {os.path.basename(downloaded_file)}!")
            
            # Clean up any leftover .part files after download
            cleanup_part_files(output_dir)
            return True
    except yt_dlp.utils.DownloadError as e:
        print(f"Download Error: {str(e)}")
        # Fall back to a simpler format if the best format fails
        try:
            print("Trying with a simpler format...")
            ydl_opts['format'] = 'best[ext=mp4]/best'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"Downloaded with alternate format: {video_title} successfully!")
            
            # Clean up any leftover .part files after download
            cleanup_part_files(output_dir)
            return True
        except Exception as e2:
            print(f"Second attempt failed: {str(e2)}")
            
            # Last resort - try with YouTube-DL compatibility mode
            try:
                print("Trying with YouTube-DL compatibility mode...")
                ydl_opts['format'] = '18/22/best'  # Standard formats that usually work
                ydl_opts['compat_opts'] = ['youtube-dl']
                ydl_opts['postprocessors'] = []  # Disable postprocessors
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                print("Downloaded with best available format!")
                
                # Clean up any leftover .part files after download
                cleanup_part_files(output_dir)
                return True
            except Exception as e3:
                print(f"Final attempt failed: {str(e3)}")
                
                # Clean up any leftover .part files after failed download
                cleanup_part_files(output_dir)
                return False
    except Exception as e:
        print(f"Error: {str(e)}")
        # Clean up any leftover .part files after exception
        cleanup_part_files(output_dir if output_dir else os.getcwd())
        return False
    finally:
        # Always make sure to clean up part files, even if an unhandled exception occurs
        cleanup_part_files(output_dir if output_dir else os.getcwd())