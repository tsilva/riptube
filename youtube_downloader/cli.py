#!/usr/bin/env python3
import sys
import argparse
from .downloader import download_video


def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos with best quality")
    parser.add_argument("url", help="YouTube video URL to download")
    parser.add_argument("-c", "--cookies", dest="cookies_file", help="Path to a Netscape format cookies.txt file", default=None)
    parser.add_argument("-o", "--output", help="Output file path (default: auto-generated from video title)", default=None)
    parser.add_argument("-a", "--audio", dest="audio_only", help="Extract audio track as MP3 file", action="store_true")
    args = parser.parse_args()

    success = download_video(args.url, args.cookies_file, args.output, args.audio_only)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()