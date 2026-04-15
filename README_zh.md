[🇬🇧 English](README.md)

# visortpy

**用纯 Python 语法可视化排序算法。**

作者: **pronoobe**

---

## 特性

- 用原生 Python 写排序算法，无需任何可视化代码
- 自动记录每次比较、读取、写入和交换操作
- 生成带颜色高亮的 GIF / MP4 动画
- 可选的"最终扫描"动画（柱状图从左到右依次变绿）
- 独立控制 X/Y 坐标轴显示
- 多进程并行渲染，带进度条显示
- 模块化渲染器架构，易于扩展

## 安装

```bash
pip install visortpy
```

生成 MP4 视频需要系统安装 ffmpeg：

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

如果只生成 GIF，则不需要 ffmpeg。

## 快速开始

### 冒泡排序

```python
from visortpy import VisualArray, create_video

arr = VisualArray([64, 34, 25, 12, 22, 11, 90])

for i in range(len(arr)):
    for j in range(len(arr) - i - 1):
        if arr[j] > arr[j + 1]:
            arr.swap(j, j + 1)

create_video(arr.history, output="bubble_sort.gif", fps=4)
```

### 选择排序

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

### 快速排序

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

## 最终扫描动画

排序完成后，加上 `final_sweep=True` 可以显示从左到右逐个变绿的动画。

```python
create_video(arr.history, output="sorted.gif", fps=8, final_sweep=True)
```

## 配置项

| 参数 | 默认值 | 说明 |
|---|---|---|
| `output` | `"output.mp4"` | 输出路径（.mp4, .gif） |
| `fps` | `4` | 帧率 |
| `style` | `"default"` | 预设风格：`"default"`, `"dark"`, `"sound"` |
| `bar_color` | `"#4a90d9"` | 默认柱状图颜色 |
| `highlight_compare` | `"#e74c3c"` | 比较高亮色（红色） |
| `highlight_swap` | `"#2ecc71"` | 交换高亮色（绿色） |
| `show_axes` | `True` | 显示或隐藏所有坐标轴 |
| `show_xaxis` | 跟随 `show_axes` | 显示或隐藏 X 轴 |
| `show_yaxis` | 跟随 `show_axes` | 显示或隐藏 Y 轴 |
| `final_sweep` | `False` | 启用最终扫描动画 |
| `sweep_color` | `"#2ecc71"` | 扫描动画颜色 |
| `num_workers` | `1` | 并行渲染进程数 |
| `show_progress` | `True` | 显示进度条 |

## 坐标轴控制

```python
# 只隐藏 X 轴
create_video(arr.history, output="no_x.gif", show_xaxis=False)

# 只隐藏 Y 轴
create_video(arr.history, output="no_y.gif", show_yaxis=False)

# 全部隐藏（等同于 show_axes=False）
create_video(arr.history, output="clean.gif", show_axes=False)
```

## 并行渲染

使用 `num_workers` 开启多进程并行渲染，加速生成。默认显示 tqdm 进度条。

```python
create_video(arr.history, output="fast.mp4", num_workers=4)

# 关闭进度条
create_video(arr.history, output="fast.mp4", num_workers=4, show_progress=False)
```

## 架构

```
VisualArray  ──记录──>  history (List[OperationRecord])  ──渲染──>  GIF/MP4
   算法操作        记录为        操作历史序列                渲染为      动画文件
```

核心设计将算法与渲染解耦。`VisualArray` 的行为与普通 Python 列表一致，算法代码保持简洁可测试。

## 许可

MIT
