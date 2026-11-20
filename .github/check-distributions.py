"""Reject incomplete release sets and unsupported tags before uploading files."""

from email.parser import BytesParser
import os
from pathlib import Path
import re
import sys
import tarfile
import urllib.error
import urllib.request
import zipfile


def check(directory):
    sources = list(directory.glob("*.tar.gz"))
    if len(sources) != 1:
        raise ValueError("Expected exactly one source distribution")
    with tarfile.open(sources[0]) as source:
        metadata_files = [m for m in source.getmembers() if m.name.count("/") == 1 and m.name.endswith("/PKG-INFO")]
        if len(metadata_files) != 1:
            raise ValueError("Expected one top-level sdist PKG-INFO")
        metadata = BytesParser().parsebytes(source.extractfile(metadata_files[0]).read())
    version = metadata["Version"]
    if metadata["Name"] != "cypari2":
        raise ValueError("Unexpected sdist project")
    seen = set()
    for wheel in directory.glob("*.whl"):
        fields = wheel.name[:-4].split("-")
        if len(fields) != 5 or fields[:2] != ["cypari2", version]:
            raise ValueError(f"Unexpected wheel name/version: {wheel.name}")
        _, _, python, abi, platforms = fields
        if python not in {"cp313", "cp314", "cp315"} or abi != python:
            raise ValueError(f"Unexpected interpreter tag: {wheel.name}")
        for tag in platforms.split("."):
            match = re.fullmatch(r"macosx_15_0_(arm64|x86_64)", tag)
            if match:
                family = "macosx", match[1]
            else:
                match = re.fullmatch(r"(manylinux|musllinux)(?:_\d+_\d+|2014|2010|1)_(aarch64|x86_64)", tag)
                if not match:
                    raise ValueError(f"Unsupported wheel platform: {tag}")
                family = match[1], match[2]
            seen.add((python, *family))
        with zipfile.ZipFile(wheel) as archive:
            meta_files = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
            if len(meta_files) != 1:
                raise ValueError(f"Missing or ambiguous metadata: {wheel.name}")
            wheel_meta = BytesParser().parsebytes(archive.read(meta_files[0]))
            if wheel_meta["Name"] != "cypari2" or wheel_meta["Version"] != version:
                raise ValueError(f"Inconsistent wheel metadata: {wheel.name}")
    expected = {
        (python, system, arch)
        for python in ("cp313", "cp314", "cp315")
        for system, arch in (("macosx", "arm64"), ("macosx", "x86_64"),
                             ("manylinux", "aarch64"), ("manylinux", "x86_64"),
                             ("musllinux", "aarch64"), ("musllinux", "x86_64"))
    }
    if seen != expected:
        raise ValueError(f"Incomplete wheel matrix: missing={expected - seen}, extra={seen - expected}")
    if set(directory.iterdir()) != set(sources) | set(directory.glob("*.whl")):
        raise ValueError("Unexpected files in the release directory")
    return version


if __name__ == "__main__":
    version = check(Path(sys.argv[1]))
    # PyPI uploads are per-file, not transactional. Check all files and refuse
    # an existing version before the publisher can create a partial release.
    if os.environ.get("GITHUB_EVENT_NAME") == "push" and os.environ.get("GITHUB_REF", "").startswith("refs/tags/"):
        if os.environ["GITHUB_REF_NAME"].removeprefix("v") != version:
            raise SystemExit("Release tag and package version disagree")
        try:
            with urllib.request.urlopen(f"https://pypi.org/pypi/cypari2/{version}/json", timeout=30) as response:
                response.read()
        except urllib.error.HTTPError as error:
            if error.code != 404:
                raise
        else:
            raise SystemExit(f"PyPI version {version} already exists; choose a new release version")
    print(f"Complete distribution set verified for cypari2 {version}")
