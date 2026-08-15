from importlib.metadata import version

import pytest
from yt_dlp import YoutubeDL
from yt_dlp.postprocessor.exec import ExecPP
from yt_dlp.utils import UnsafeExecExpansionError

from riptube import downloader


def date_version(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split("."))


def test_ytdlp_is_patched_for_all_declared_advisories():
    assert date_version(version("yt-dlp")) >= (2026, 7, 4)


def test_unsafe_exec_metadata_conversion_is_rejected():
    with pytest.raises(UnsafeExecExpansionError):
        ExecPP(YoutubeDL({"quiet": True}), "echo %(title)s")


def test_wrapper_does_not_enable_dangerous_ytdlp_features(monkeypatch, tmp_path):
    observed: dict[str, object] = {}

    class FakeYoutubeDL:
        def __init__(self, options):
            observed["options"] = options

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def download(self, urls):
            observed["urls"] = urls

    monkeypatch.setattr(downloader.yt_dlp, "YoutubeDL", FakeYoutubeDL)
    monkeypatch.setattr(downloader, "check_dependencies", lambda: None)

    hostile_url = "https://example.invalid/video?title=x;touch+SHOULD_NOT_EXIST"
    output = str(tmp_path / downloader.DEFAULT_OUTTMPL)

    assert downloader.download_video(hostile_url, output=output)
    assert observed["urls"] == [hostile_url]

    options = observed["options"]
    dangerous = {
        "exec_cmd",
        "external_downloader",
        "netrc_cmd",
        "writedesktoplink",
        "writelink",
        "writeurllink",
    }
    assert dangerous.isdisjoint(options)
    assert options["outtmpl"].endswith(".%(ext)s")
