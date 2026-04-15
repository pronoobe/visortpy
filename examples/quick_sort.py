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


if __name__ == '__main__':
    import random

    N = 200  # 数据长度（可以调到 100~200，看你机器性能）
    data = [random.randint(1, 100) for _ in range(N)]
    data = VisualArray(data)
    quicksort(data, 0, len(data) - 1)

    create_video(
        data.history,
        output="quick_sort.gif",
        fps=60,
        bar_color="#3498db",
        highlight_compare="#e74c3c",
        highlight_swap="#2ecc71",
        show_xaxis=False,
        show_yaxis=False,
        final_sweep=True,
        num_workers=5
    )
    print(f"Done — {len(data.history)} steps recorded, sorted: {data.to_list()}")
