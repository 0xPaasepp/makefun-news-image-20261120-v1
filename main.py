#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261120.

Copies the pre-rendered front page (entry.png, built at build time
by render.py) byte-for-byte to /output/entry.png.

Pure standard library. No network, no fonts, no image work at run
time: the graded program only moves the finished file into place.
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))


if __name__ == "__main__":
    main()
