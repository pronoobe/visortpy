"""Abstract base class for all visualgo renderers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ..operations import OperationRecord


class BaseRenderer(ABC):
    """Base class that all renderers must implement."""

    @abstractmethod
    def render(
        self,
        history: List[OperationRecord],
        output_path: str,
        **config: Any,
    ) -> str:
        """Render the operation history to a visual output file.

        Args:
            history: List of OperationRecord from VisualArray.
            output_path: Destination file path.
            **config: Renderer-specific configuration.

        Returns:
            The absolute path of the generated file.
        """
        ...
