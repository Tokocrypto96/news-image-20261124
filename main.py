#!/usr/bin/env python3
"""Entry point for news-image-20261124 (program/v1, Python 3.13, stdlib only).

The front page image is drawn by render.py (Pillow) and shipped beside this
file as entry.png; this program copies it to the output directory so the
grader sees exactly the bytes that were reviewed.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
src = os.path.join(HERE, "entry.png")
dst = os.path.join(OUT, "entry.png")
shutil.copyfile(src, dst)
# Gate guard: the entry must stay a whole PNG of at most 1 MiB.
size = os.path.getsize(dst)
assert size <= 1048576, f"entry.png too big: {size} bytes"
print("wrote", dst, size, "bytes")
