# visortpy

**Visualize sorting algorithms with pure Python syntax.**

用纯 Python 语法可视化排序算法。

Author / 作者: **pronoobe**

---

## Features / 特性

- Write sorting algorithms in plain Python — no visualization code needed
- 用原生 Python 写排序算法，无需任何可视化代码
- Auto-records every comparison, read, write, and swap
- 自动记录每次比较、读取、写入和交换操作
- Generates GIF / MP4 animations with color-coded highlights
- 生成带颜色高亮的 GIF / MP4 动画
- Optional "final sweep" animation (bars turn green left-to-right)
- 可选的"最终扫描"动画（柱状图从左到右依次变绿）
- Modular renderer architecture — easy to extend
- 模块化渲染器架构，易于扩展

## Installation / 安装

```bash
pip install visortpy
```

## Quick Start / 快速开始

### Bubble Sort / 冒泡排序

```python
from visortpy import VisualArray, create_video

arr = VisualArray([64, 34, 25, 12, 22, 11, 90])

for i in range(len(arr)):
    for j in range(len(arr) - i - 1):
        if arr[j] > arr[j + 1]:
            arr.swap(j, j + 1)

create_video(arr.history, output="bubble_sort.gif", fps=4)
```

### Selection Sort / 选择排序

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

### Quick Sort / 快速排序

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

## Final Sweep Animation / 最终扫描动画

Add `final_sweep=True` to show a left-to-right green sweep after sorting completes.

排序完成后，加上 `final_sweep=True` 可以显示从左到右逐个变绿的动画。

```python
create_video(arr.history, output="sorted.gif", fps=8, final_sweep=True)
```

## Configuration / 配置项

| Parameter / 参数 | Default / 默认值 | Description / 说明 |
|---|---|---|
| `output` | `"output.mp4"` | Output path (.mp4, .gif) / 输出路径 |
| `fps` | `4` | Frames per second / 帧率 |
| `style` | `"default"` | Preset style: `"default"`, `"dark"`, `"sound"` / 预设风格 |
| `bar_color` | `"#4a90d9"` | Default bar color / 默认柱状图颜色 |
| `highlight_compare` | `"#e74c3c"` | Compare highlight (red) / 比较高亮色 |
| `highlight_swap` | `"#2ecc71"` | Swap highlight (green) / 交换高亮色 |
| `final_sweep` | `False` | Enable final green sweep / 启用最终扫描动画 |
| `sweep_color` | `"#2ecc71"` | Sweep bar color / 扫描动画颜色 |

## Architecture / 架构

```
VisualArray  ──records──>  history (List[OperationRecord])  ──renders──>  GIF/MP4
   算法操作         记录为         操作历史序列                  渲染为       动画文件
```

The core design decouples algorithms from rendering. `VisualArray` behaves like a normal Python list — your algorithm code stays clean and testable.

核心设计将算法与渲染解耦。`VisualArray` 的行为与普通 Python 列表一致，算法代码保持简洁可测试。

## License / 许可

MIT
