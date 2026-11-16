"""Offline regressions for failures that must precede any PyPI upload."""

import hashlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("check_distributions", HERE / "check-distributions.py")
CHECKS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKS)


class DistributionChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dist = Path(self.temp.name)
        self.source = self.dist / "cypari2-2.2.7.tar.gz"
        with tarfile.open(self.source, "w:gz") as archive:
            content = b"Name: cypari2\nVersion: 2.2.7\n"
            info = tarfile.TarInfo("cypari2-2.2.7/PKG-INFO")
            info.size = len(content)
            archive.addfile(info, io.BytesIO(content))
        for python in ("cp313", "cp314", "cp315"):
            for platform in ("macosx_15_0_arm64", "macosx_15_0_x86_64",
                             "manylinux_2_28_aarch64", "manylinux_2_28_x86_64",
                             "musllinux_1_2_aarch64", "musllinux_1_2_x86_64"):
                self.wheel(python, platform)

    def wheel(self, python, platform, version="2.2.7"):
        path = self.dist / f"cypari2-2.2.7-{python}-{python}-{platform}.whl"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("cypari2-2.2.7.dist-info/METADATA", f"Name: cypari2\nVersion: {version}\n")
        return path

    def test_complete_set(self):
        self.assertEqual(CHECKS.check(self.dist), "2.2.7")

    def test_rejects_original_darwin_27_failure(self):
        self.wheel("cp313", "macosx_27_0_arm64")
        with self.assertRaisesRegex(ValueError, "Unsupported wheel platform"):
            CHECKS.check(self.dist)

    def test_missing_platform_fails_before_publish(self):
        self.wheel("cp315", "musllinux_1_2_aarch64").unlink()
        with self.assertRaisesRegex(ValueError, "Incomplete wheel matrix"):
            CHECKS.check(self.dist)

    def test_mixed_metadata_fails(self):
        self.wheel("cp314", "macosx_15_0_arm64", version="2.2.6")
        with self.assertRaisesRegex(ValueError, "Inconsistent wheel metadata"):
            CHECKS.check(self.dist)

    def test_changed_source_archive_fails(self):
        digest = hashlib.sha256(self.source.read_bytes()).hexdigest()
        command = [sys.executable, str(HERE / "verify-sdist.py"), str(self.dist), "--sha256", digest]
        subprocess.run(command, check=True, capture_output=True)
        with self.source.open("ab") as archive:
            archive.write(b"changed")
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("checksum mismatch", result.stderr)


if __name__ == "__main__":
    unittest.main()
