"""Record or verify the one source archive shared by distribution jobs."""

import argparse
import hashlib
from pathlib import Path
import tarfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--sha256")
    parser.add_argument("--extract", type=Path)
    args = parser.parse_args()
    archives = list(args.directory.glob("*.tar.gz"))
    if len(archives) != 1:
        raise SystemExit(f"Expected one sdist, found {archives}")
    archive = archives[0]
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if args.sha256 is not None and digest != args.sha256:
        raise SystemExit(f"Source archive checksum mismatch: {digest}")
    if args.extract:
        args.extract.mkdir(exist_ok=False)
        with tarfile.open(archive) as source:
            source.extractall(args.extract, filter="data")
        roots = list(args.extract.iterdir())
        if len(roots) != 1 or not (roots[0] / "Makefile").is_file():
            raise SystemExit("The sdist does not contain one complete test source tree")
        print(f"source={roots[0]}")
    print(f"filename={archive.name}")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
