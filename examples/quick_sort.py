"""Quick sort visualization example."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from visortpy import VisualArray, create_video


def quicksort(arr: VisualArray, low: int, high: int) -> None:
    if low < high:
        pivot_idx = partition(arr, low, high)
        quicksort(arr, low, pivot_idx - 1)
        quicksort(arr, pivot_idx + 1, high)


def partition(arr: VisualArray, low: int, high: int) -> int:
    pivot = arr[high]  # READ recorded
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:  # READ + comparison
            i += 1
            arr.swap(i, j)
    arr.swap(i + 1, high)
    return i + 1


data = VisualArray([38, 27, 43, 3, 9, 82, 10])
quicksort(data, 0, len(data) - 1)

create_video(
    data.history,
    output="quick_sort.gif",
    fps=6,
    bar_color="#3498db",
    highlight_compare="#e74c3c",
    highlight_swap="#2ecc71",
    show_xaxis=True, 
    show_yaxis=False
)
print(f"Done — {len(data.history)} steps recorded, sorted: {data.to_list()}")
