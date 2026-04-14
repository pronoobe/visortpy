"""Renderer registry for visualgo."""

from typing import Dict, Type

from .base import BaseRenderer
from .matplotlib_renderer import MatplotlibRenderer

_REGISTRY: Dict[str, Type[BaseRenderer]] = {
    "matplotlib": MatplotlibRenderer,
}


def get_renderer(name: str = "matplotlib") -> BaseRenderer:
    """Return an instance of the named renderer."""
    cls = _REGISTRY.get(name)
    if cls is None:
        raise ValueError(f"Unknown renderer {name!r}. Available: {list(_REGISTRY)}")
    return cls()


def register_renderer(name: str, cls: Type[BaseRenderer]) -> None:
    """Register a custom renderer class."""
    _REGISTRY[name] = cls
