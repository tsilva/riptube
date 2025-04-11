#!/usr/bin/env python3
import sys
import argparse
from .downloader import download_video


def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos with best quality")
    parser.add_argument("url", help="YouTube video URL to download")
    parser.add_argument("-o", "--output", help="Output file path (default: auto-generated from video title)", default=None)
    args = parser.parse_args()

    success = download_video(args.url, args.output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()