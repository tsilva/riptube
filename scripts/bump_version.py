#!/usr/bin/env python3

from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
INIT_FILE = ROOT / "riptube" / "__init__.py"
VERSION_RE = re.compile(r'(?m)^version = "(\d+)\.(\d+)\.(\d+)"$')
FALLBACK_VERSION_RE = re.compile(r'(?m)^    __version__ = "(\d+)\.(\d+)\.(\d+)"$')


def read_version() -> str:
    match = VERSION_RE.search(PYPROJECT.read_text())
    if match is None:
        raise SystemExit("Could not find project version in pyproject.toml")
    return ".".join(match.groups())


def bump_version(current: str, part: str) -> str:
    major, minor, patch = (int(piece) for piece in current.split("."))
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise SystemExit(f"Unsupported version part: {part}")
    return f"{major}.{minor}.{patch}"


def replace_once(path: pathlib.Path, pattern: re.Pattern[str], replacement: str) -> None:
    text = path.read_text()
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"Could not update version in {path}")
    path.write_text(updated)


def main() -> int:
    parser = argparse.ArgumentParser(description="Bump the project version.")
    parser.add_argument("part", nargs="?", choices=["patch", "minor", "major"])
    parser.add_argument(
        "--current",
        action="store_true",
        help="Print the current version and exit.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the next version without writing files.",
    )
    args = parser.parse_args()

    current = read_version()
    if args.current:
        print(current)
        return 0

    if args.part is None:
        parser.error("the following arguments are required: part")

    new_version = bump_version(current, args.part)
    if args.dry_run:
        print(new_version)
        return 0

    replace_once(PYPROJECT, VERSION_RE, f'version = "{new_version}"')
    replace_once(INIT_FILE, FALLBACK_VERSION_RE, f'    __version__ = "{new_version}"')
    print(new_version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
