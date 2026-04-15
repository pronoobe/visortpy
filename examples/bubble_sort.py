"""Bubble sort visualization example."""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from visortpy import VisualArray, create_video

import random

if __name__ == '__main__':

    N = 30  # 数据长度（可以调到 100~200，看你机器性能）
    arr = [random.randint(1, 100) for _ in range(N)]
    arr = VisualArray(arr)
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr.swap(j, j + 1)

    create_video(arr.history, output="bubble_sort.mp4",
                 fps=50,
                 num_workers=15,
                 style="default",
                 show_xaxis=False,
                 show_yaxis=False,
                 final_sweep=True,
                 )
    print(f"Done — {len(arr.history)} steps recorded, sorted: {arr.to_list()}")
