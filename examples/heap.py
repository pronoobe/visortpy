from visortpy import VisualArray, create_video
import random

# ========= Heap Sort =========
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr.swap(i, largest)
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)

    # 建堆
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # 排序
    for i in range(n - 1, 0, -1):
        arr.swap(0, i)
        heapify(arr, i, 0)

# ========= 随机数据 =========
N = 100  # 数据长度（可以调到 100~200，看你机器性能）
data_list = [random.randint(1, 100) for _ in range(N)]

arr = VisualArray(data_list)

heap_sort(arr)

# ========= 可视化 =========
create_video(
    arr.history,
    output="heap_sort_dark.gif",
    fps=30,                     # 高帧率更丝滑
    style="dark",               # 黑底
    bar_color="#ffffff",        # 白色柱子
    highlight_compare="#888888",# 比较：灰色（低调）
    highlight_swap="#ffffff",   # swap：保持白色（极简）
    final_sweep=True,
    sweep_color="#ffffff",
    show_xaxis=True,
    show_yaxis=False,
    num_workers=10

)