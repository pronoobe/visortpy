"""Matplotlib-based renderer for VisualArray history."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from ..operations import OperationRecord, OperationType
from ..styles import get_style
from .base import BaseRenderer


class MatplotlibRenderer(BaseRenderer):
    """Renders sorting history as a bar-chart animation (MP4 or GIF)."""

    def render(
        self,
        history: List[OperationRecord],
        output_path: str,
        **config: Any,
    ) -> str:
        if not history:
            raise ValueError("Cannot render empty history.")

        # Merge style defaults with user overrides
        style_name = config.pop("style", "default")
        style = get_style(style_name)
        style.update(config)

        fps: int = style.get("fps", 4)
        figsize = style.get("figsize", (10, 6))
        bar_color: str = style.get("bar_color", "#4a90d9")
        hl_compare: str = style.get("highlight_compare", "#e74c3c")
        hl_swap: str = style.get("highlight_swap", "#2ecc71")
        hl_write: str = style.get("highlight_write", "#f39c12")
        bg: str = style.get("background", "#ffffff")
        text_color: str = style.get("text_color", "#333333")
        show_axes: bool = style.get("show_axes", True)
        sound_markers: bool = style.get("sound_markers", False)
        final_sweep: bool = style.get("final_sweep", False)
        sweep_color: str = style.get("sweep_color", "#2ecc71")

        # Sound marker collection
        markers: List[Dict[str, Any]] = []

        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)

        n = len(history[0].array_state)
        x = list(range(n))

        bars = ax.bar(x, history[0].array_state, color=bar_color)
        title = ax.set_title("Step 0", color=text_color, fontsize=14)
        ax.tick_params(colors=text_color)
        if not show_axes:
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)

        max_val = max(max(r.array_state) for r in history) * 1.1
        ax.set_ylim(0, max_val)

        # Build sweep frames: after sorting, bars turn green left-to-right
        final_state = history[-1].array_state
        sweep_frame_count = len(final_state) if final_sweep else 0
        total_frames = len(history) + sweep_frame_count

        def _update(frame: int) -> list:
            if frame < len(history):
                # Normal history frame
                rec = history[frame]
                state = rec.array_state
                colors = [bar_color] * len(state)

                for idx in rec.indices:
                    if 0 <= idx < len(state):
                        if rec.operation == OperationType.COMPARE:
                            colors[idx] = hl_compare
                        elif rec.operation == OperationType.SWAP:
                            colors[idx] = hl_swap
                        elif rec.operation == OperationType.WRITE:
                            colors[idx] = hl_write
                        else:
                            colors[idx] = hl_compare

                for bar, h, c in zip(bars, state, colors):
                    bar.set_height(h)
                    bar.set_color(c)

                title.set_text(f"Step {rec.step}  [{rec.operation.value.upper()}]")

                if sound_markers and rec.operation in (
                    OperationType.SWAP, OperationType.COMPARE
                ):
                    markers.append({
                        "time": frame / fps,
                        "operation": rec.operation.value,
                        "indices": rec.indices,
                    })
            else:
                # Sweep frame: progressively turn bars green
                sweep_idx = frame - len(history)
                colors = [bar_color] * len(final_state)
                for k in range(sweep_idx + 1):
                    colors[k] = sweep_color
                for bar, h, c in zip(bars, final_state, colors):
                    bar.set_height(h)
                    bar.set_color(c)
                title.set_text("Sorted!")

            return list(bars) + [title]

        anim = animation.FuncAnimation(
            fig, _update, frames=total_frames, interval=1000 // fps, blit=False
        )

        ext = os.path.splitext(output_path)[1].lower()
        if ext == ".gif":
            anim.save(output_path, writer="pillow", fps=fps)
        else:
            anim.save(output_path, writer="ffmpeg", fps=fps)

        plt.close(fig)

        if sound_markers:
            marker_path = output_path + ".markers.json"
            import json
            with open(marker_path, "w") as f:
                json.dump(markers, f, indent=2)

        return os.path.abspath(output_path)
