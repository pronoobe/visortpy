"""Matplotlib-based renderer for VisualArray history."""

from __future__ import annotations

import os
import tempfile
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Tuple

from tqdm import tqdm

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from ..operations import OperationRecord, OperationType
from ..styles import get_style
from .base import BaseRenderer


def _render_frame(args: Tuple) -> str:
    """Render a single frame to PNG. Top-level function for pickling."""
    (
        frame_idx, array_state, operation, indices,
        step, is_sweep, sweep_idx, final_state,
        config, output_path,
    ) = args

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fps = config["fps"]
    figsize = config["figsize"]
    bar_color = config["bar_color"]
    hl_compare = config["highlight_compare"]
    hl_swap = config["highlight_swap"]
    hl_write = config["highlight_write"]
    bg = config["background"]
    text_color = config["text_color"]
    show_xaxis = config["show_xaxis"]
    show_yaxis = config["show_yaxis"]
    sweep_color = config["sweep_color"]
    max_val = config["max_val"]

    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    if is_sweep:
        state = final_state
        colors = [bar_color] * len(state)
        for k in range(sweep_idx + 1):
            colors[k] = sweep_color
        title_text = "Sorted!"
    else:
        state = array_state
        colors = [bar_color] * len(state)
        for idx in indices:
            if 0 <= idx < len(state):
                if operation == "compare":
                    colors[idx] = hl_compare
                elif operation == "swap":
                    colors[idx] = hl_swap
                elif operation == "write":
                    colors[idx] = hl_write
                else:
                    colors[idx] = hl_compare
        title_text = f"Step {step}  [{operation.upper()}]"

    x = list(range(len(state)))
    ax.bar(x, state, color=colors)
    ax.set_title(title_text, color=text_color, fontsize=14)
    ax.tick_params(colors=text_color)
    if not show_xaxis:
        ax.set_xticks([])
        ax.spines["bottom"].set_visible(False)
        ax.spines["top"].set_visible(False)
    if not show_yaxis:
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
    ax.set_ylim(0, max_val)

    fig.savefig(output_path, facecolor=fig.get_facecolor())
    plt.close(fig)
    return output_path


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
        show_xaxis: bool = style.get("show_xaxis", show_axes)
        show_yaxis: bool = style.get("show_yaxis", show_axes)
        sound_markers: bool = style.get("sound_markers", False)
        final_sweep: bool = style.get("final_sweep", False)
        sweep_color: str = style.get("sweep_color", "#2ecc71")
        num_workers: int = style.get("num_workers", 1)
        show_progress: bool = style.get("show_progress", True)

        max_val = max(max(r.array_state) for r in history) * 1.1
        final_state = list(history[-1].array_state)
        sweep_frame_count = len(final_state) if final_sweep else 0
        total_frames = len(history) + sweep_frame_count

        if num_workers > 1:
            return self._render_parallel(
                history, output_path, fps, figsize, bar_color,
                hl_compare, hl_swap, hl_write, bg, text_color,
                show_xaxis, show_yaxis, sweep_color, max_val,
                final_state, final_sweep, sweep_frame_count,
                total_frames, sound_markers, num_workers,
                show_progress,
            )

        return self._render_sequential(
            history, output_path, fps, figsize, bar_color,
            hl_compare, hl_swap, hl_write, bg, text_color,
            show_xaxis, show_yaxis, sound_markers, final_sweep,
            sweep_color, max_val, final_state, sweep_frame_count,
            total_frames, show_progress,
        )

    # -- sequential path (original FuncAnimation) --

    def _render_sequential(
        self, history, output_path, fps, figsize, bar_color,
        hl_compare, hl_swap, hl_write, bg, text_color,
        show_xaxis, show_yaxis, sound_markers, final_sweep,
        sweep_color, max_val, final_state, sweep_frame_count,
        total_frames, show_progress,
    ) -> str:
        markers: List[Dict[str, Any]] = []
        pbar = tqdm(total=total_frames, desc="Rendering", unit="frame",
                     disable=not show_progress)

        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)

        n = len(history[0].array_state)
        x = list(range(n))

        bars = ax.bar(x, history[0].array_state, color=bar_color)
        title = ax.set_title("Step 0", color=text_color, fontsize=14)
        ax.tick_params(colors=text_color)
        if not show_xaxis:
            ax.set_xticks([])
            ax.spines["bottom"].set_visible(False)
            ax.spines["top"].set_visible(False)
        if not show_yaxis:
            ax.set_yticks([])
            ax.spines["left"].set_visible(False)
            ax.spines["right"].set_visible(False)
        ax.set_ylim(0, max_val)

        def _update(frame: int) -> list:
            if frame < len(history):
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
                sweep_idx = frame - len(history)
                colors = [bar_color] * len(final_state)
                for k in range(sweep_idx + 1):
                    colors[k] = sweep_color
                for bar, h, c in zip(bars, final_state, colors):
                    bar.set_height(h)
                    bar.set_color(c)
                title.set_text("Sorted!")
            pbar.update(1)
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
        pbar.close()

        if sound_markers:
            import json
            marker_path = output_path + ".markers.json"
            with open(marker_path, "w") as f:
                json.dump(markers, f, indent=2)

        return os.path.abspath(output_path)

    # -- parallel path (multi-process frame rendering) --

    def _render_parallel(
        self, history, output_path, fps, figsize, bar_color,
        hl_compare, hl_swap, hl_write, bg, text_color,
        show_xaxis, show_yaxis, sweep_color, max_val,
        final_state, final_sweep, sweep_frame_count,
        total_frames, sound_markers, num_workers,
        show_progress,
    ) -> str:
        tmp_dir = tempfile.mkdtemp(prefix="visortpy_")
        try:
            render_config = {
                "fps": fps, "figsize": figsize,
                "bar_color": bar_color,
                "highlight_compare": hl_compare,
                "highlight_swap": hl_swap,
                "highlight_write": hl_write,
                "background": bg, "text_color": text_color,
                "show_xaxis": show_xaxis, "show_yaxis": show_yaxis,
                "sweep_color": sweep_color, "max_val": max_val,
            }

            tasks = []
            for i in range(total_frames):
                png_path = os.path.join(tmp_dir, f"frame_{i:06d}.png")
                if i < len(history):
                    rec = history[i]
                    tasks.append((
                        i, list(rec.array_state), rec.operation.value,
                        list(rec.indices), rec.step,
                        False, 0, final_state,
                        render_config, png_path,
                    ))
                else:
                    sweep_idx = i - len(history)
                    tasks.append((
                        i, [], "", [], 0,
                        True, sweep_idx, final_state,
                        render_config, png_path,
                    ))

            with ProcessPoolExecutor(max_workers=num_workers) as pool:
                list(tqdm(
                    pool.map(_render_frame, tasks),
                    total=total_frames, desc="Rendering", unit="frame",
                    disable=not show_progress,
                ))

            # Assemble frames into video
            ext = os.path.splitext(output_path)[1].lower()
            if ext == ".gif":
                from PIL import Image
                frames = []
                for i in range(total_frames):
                    png_path = os.path.join(tmp_dir, f"frame_{i:06d}.png")
                    frames.append(Image.open(png_path).copy())
                frames[0].save(
                    output_path, save_all=True, append_images=frames[1:],
                    duration=1000 // fps, loop=0,
                )
            else:
                import subprocess
                pattern = os.path.join(tmp_dir, "frame_%06d.png")
                subprocess.run([
                    "ffmpeg", "-y", "-framerate", str(fps),
                    "-i", pattern, "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", output_path,
                ], check=True, capture_output=True)

            if sound_markers:
                import json
                markers = []
                for i, rec in enumerate(history):
                    if rec.operation in (OperationType.SWAP, OperationType.COMPARE):
                        markers.append({
                            "time": i / fps,
                            "operation": rec.operation.value,
                            "indices": list(rec.indices),
                        })
                marker_path = output_path + ".markers.json"
                with open(marker_path, "w") as f:
                    json.dump(markers, f, indent=2)
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

        return os.path.abspath(output_path)
