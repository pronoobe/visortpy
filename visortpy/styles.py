"""Preset color/style configurations for renderers."""

from typing import Any, Dict

STYLES: Dict[str, Dict[str, Any]] = {
    "default": {
        "bar_color": "#4a90d9",
        "highlight_compare": "#e74c3c",
        "highlight_swap": "#2ecc71",
        "highlight_write": "#f39c12",
        "background": "#ffffff",
        "text_color": "#333333",
        "show_axes": True,
        "show_xaxis": True,
        "show_yaxis": True,
        "figsize": (10, 6),
    },
    "dark": {
        "bar_color": "#3498db",
        "highlight_compare": "#e74c3c",
        "highlight_swap": "#2ecc71",
        "highlight_write": "#f39c12",
        "background": "#1e1e1e",
        "text_color": "#cccccc",
        "show_axes": False,
        "show_xaxis": False,
        "show_yaxis": False,
        "figsize": (10, 6),
    },
    "sound": {
        "bar_color": "#4a90d9",
        "highlight_compare": "#e74c3c",
        "highlight_swap": "#2ecc71",
        "highlight_write": "#f39c12",
        "background": "#ffffff",
        "text_color": "#333333",
        "show_axes": True,
        "show_xaxis": True,
        "show_yaxis": True,
        "figsize": (10, 6),
        "sound_markers": True,
    },
}


def get_style(name: str) -> Dict[str, Any]:
    """Return a copy of the named style, or raise ValueError."""
    if name not in STYLES:
        raise ValueError(f"Unknown style {name!r}. Available: {list(STYLES)}")
    return dict(STYLES[name])
