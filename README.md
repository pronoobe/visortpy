[🇨🇳 中文版](README_zh.md)

# visortpy

**Visualize sorting algorithms with pure Python syntax.**

Author: **pronoobe**

---

## Features

- Write sorting algorithms in plain Python — no visualization code needed
- Auto-records every comparison, read, write, and swap
- Generates GIF / MP4 animations with color-coded highlights
- Optional "final sweep" animation (bars turn green left-to-right)
- Independent X/Y axis visibility control
- Multi-process parallel rendering with progress bar
- Modular renderer architecture — easy to extend

## Installation

```bash
pip install visortpy
```

MP4 output requires ffmpeg installed on your system:

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows (scoop)
scoop install ffmpeg

# Windows (choco)
choco install ffmpeg
```

GIF output does not require ffmpeg.

## Quick Start

### Bubble Sort

```python
from visortpy import VisualArray, create_video

arr = VisualArray([64, 34, 25, 12, 22, 11, 90])

for i in range(len(arr)):
    for j in range(len(arr) - i - 1):
        if arr[j] > arr[j + 1]:
            arr.swap(j, j + 1)

create_video(arr.history, output="bubble_sort.gif", fps=4)
```

### Selection Sort

```python
arr = VisualArray([29, 10, 14, 37, 13])

for i in range(len(arr)):
    min_idx = i
    for j in range(i + 1, len(arr)):
        if arr[j] < arr[min_idx]:
            min_idx = j
    if min_idx != i:
        arr.swap(i, min_idx)

create_video(arr.history, output="selection_sort.gif", fps=4, style="dark")
```

### Quick Sort

```python
from visortpy import VisualArray, create_video

def quicksort(arr, low, high):
    if low < high:
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr.swap(i, j)
        arr.swap(i + 1, high)
        quicksort(arr, low, i)
        quicksort(arr, i + 2, high)

data = VisualArray([38, 27, 43, 3, 9, 82, 10])
quicksort(data, 0, len(data) - 1)
create_video(data.history, output="quick_sort.gif", fps=6)
```

## Final Sweep Animation

Add `final_sweep=True` to show a left-to-right green sweep after sorting completes.

```python
create_video(arr.history, output="sorted.gif", fps=8, final_sweep=True)
```

## Configuration

| Parameter | Default | Description |
|---|---|---|
| `output` | `"output.mp4"` | Output path (.mp4, .gif) |
| `fps` | `4` | Frames per second |
| `style` | `"default"` | Preset style: `"default"`, `"dark"`, `"sound"` |
| `bar_color` | `"#4a90d9"` | Default bar color |
| `highlight_compare` | `"#e74c3c"` | Compare highlight (red) |
| `highlight_swap` | `"#2ecc71"` | Swap highlight (green) |
| `show_axes` | `True` | Show/hide both axes |
| `show_xaxis` | follows `show_axes` | Show/hide X axis (indices) |
| `show_yaxis` | follows `show_axes` | Show/hide Y axis (values) |
| `final_sweep` | `False` | Enable final green sweep |
| `sweep_color` | `"#2ecc71"` | Sweep bar color |
| `num_workers` | `1` | Parallel render processes |
| `show_progress` | `True` | Show tqdm progress bar |

## Axis Control

```python
# Hide X axis only
create_video(arr.history, output="no_x.gif", show_xaxis=False)

# Hide Y axis only
create_video(arr.history, output="no_y.gif", show_yaxis=False)

# Hide both (same as show_axes=False)
create_video(arr.history, output="clean.gif", show_axes=False)
```

## Parallel Rendering

Use `num_workers` to speed up rendering with multiple processes. A tqdm progress bar is shown by default.

```python
create_video(arr.history, output="fast.mp4", num_workers=4)

# Disable progress bar
create_video(arr.history, output="fast.mp4", num_workers=4, show_progress=False)
```

## Architecture

```
VisualArray  ──records──>  history (List[OperationRecord])  ──renders──>  GIF/MP4
```

The core design decouples algorithms from rendering. `VisualArray` behaves like a normal Python list — your algorithm code stays clean and testable.

## License

MIT
