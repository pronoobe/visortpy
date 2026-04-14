"""Bubble sort visualization example."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from visortpy import VisualArray, create_video

arr = VisualArray([64, 34, 25, 12, 22, 11, 90])

for i in range(len(arr)):
    for j in range(len(arr) - i - 1):
        if arr[j] > arr[j + 1]:
            arr.swap(j, j + 1)

create_video(arr.history, output="bubble_sort.gif", fps=4)
print(f"Done — {len(arr.history)} steps recorded, sorted: {arr.to_list()}")
