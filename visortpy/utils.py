"""Utility helpers for the visualgo package."""

import os
from typing import Optional


def detect_format(path: str) -> str:
    """Detect output format from file extension.

    Returns one of 'mp4', 'gif', or 'html'. Defaults to 'mp4'.
    """
    ext = os.path.splitext(path)[1].lower()
    mapping = {".mp4": "mp4", ".gif": "gif", ".html": "html"}
    return mapping.get(ext, "mp4")
