"""Selection sort visualization example."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from visortpy import VisualArray, create_video

arr = VisualArray([29, 10, 14, 37, 13])

for i in range(len(arr)):
    min_idx = i
    for j in range(i + 1, len(arr)):
        if arr[j] < arr[min_idx]:
            min_idx = j
    if min_idx != i:
        arr.swap(i, min_idx)

create_video(arr.history, output="selection_sort.gif", fps=4, style="dark")
print(f"Done — {len(arr.history)} steps recorded, sorted: {arr.to_list()}")
