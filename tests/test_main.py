#!/usr/bin/env python3
"""Tests for main.py: the graded program copies entry.png byte-for-byte
to /output/entry.png and the result is a valid 1024x1024 PNG.

Pure standard library (unittest + subprocess + struct).
"""
import hashlib
import os
import struct
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG file"
    width, height = struct.unpack(">II", head[16:24])
    return width, height


class TestMain(unittest.TestCase):
    def test_copies_entry_byte_for_byte(self):
        src = os.path.join(REPO, "entry.png")
        self.assertTrue(os.path.exists(src), "entry.png missing from repo")
        with tempfile.TemporaryDirectory() as tmp:
            # Run from an unrelated cwd, the way the grader does.
            env = dict(os.environ)
            proc = subprocess.run(
                [sys.executable, "-P", "-s",
                 os.path.join(REPO, "main.py")],
                cwd=tmp, capture_output=True, text=True, env=env)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            dst = os.path.join("/output", "entry.png")
            self.assertTrue(os.path.exists(dst), "/output/entry.png missing")
            with open(src, "rb") as fh:
                want = fh.read()
            with open(dst, "rb") as fh:
                got = fh.read()
            self.assertEqual(hashlib.sha256(got).hexdigest(),
                             hashlib.sha256(want).hexdigest(),
                             "output differs from entry.png")

    def test_entry_is_1024x1024_png(self):
        src = os.path.join(REPO, "entry.png")
        self.assertEqual(png_size(src), (1024, 1024))
        self.assertLessEqual(os.path.getsize(src), 1024 * 1024,
                             "entry.png over the 1 MiB cap")


if __name__ == "__main__":
    unittest.main()
