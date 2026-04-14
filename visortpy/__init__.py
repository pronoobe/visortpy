"""visortpy — visualize sorting algorithms with pure Python syntax."""

from .core import VisualArray
from .operations import OperationRecord, OperationType
from .renderers import get_renderer, register_renderer
from .renderers.base import BaseRenderer
from .renderers.matplotlib_renderer import MatplotlibRenderer

from typing import Any, List


def create_video(
    history: List[OperationRecord],
    output: str = "output.mp4",
    renderer: str = "matplotlib",
    **kwargs: Any,
) -> str:
    """Render operation history to a video/animation file.

    Args:
        history: Operation history from ``VisualArray.history``.
        output: Output file path (.mp4, .gif, or .html).
        renderer: Renderer backend name (default ``'matplotlib'``).
        **kwargs: Passed to the renderer (fps, style, colors, etc.).

    Returns:
        Absolute path of the generated file.

    Example::

        from visortpy import VisualArray, create_video

        arr = VisualArray([64, 34, 25, 12, 22, 11, 90])
        for i in range(len(arr)):
            for j in range(len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr.swap(j, j + 1)
        create_video(arr.history, output="bubble_sort.mp4", fps=2)
    """
    r = get_renderer(renderer)
    return r.render(history, output, **kwargs)


__all__ = [
    "VisualArray",
    "OperationType",
    "OperationRecord",
    "BaseRenderer",
    "MatplotlibRenderer",
    "create_video",
    "get_renderer",
    "register_renderer",
]
