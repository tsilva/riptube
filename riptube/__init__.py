from importlib.metadata import PackageNotFoundError, version

from .downloader import download_video

__all__ = ["download_video", "__version__"]

try:
    __version__ = version("riptube")
except PackageNotFoundError:
    # Fallback for local execution before the distribution is installed.
    __version__ = "0.1.0"
