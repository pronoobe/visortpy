"""Odd-even sort visualization example."""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from visortpy import VisualArray, create_video

if __name__ == '__main__':
    N = 50
    arr = VisualArray([random.randint(1, 100) for _ in range(N)])

    sorted_ = False
    while not sorted_:
        sorted_ = True
        for i in range(1, len(arr) - 1, 2):  # odd
            if arr[i] > arr[i + 1]:
                arr.swap(i, i + 1)
                sorted_ = False
        for i in range(0, len(arr) - 1, 2):  # even
            if arr[i] > arr[i + 1]:
                arr.swap(i, i + 1)
                sorted_ = False

    create_video(
        arr.history,
        output="odd_even_sort.mp4",
        fps=60,
        bar_color="#2980b9",
        show_xaxis=False,
        show_yaxis=False,
        final_sweep=True,
        num_workers=8,
    )
    print(f"Done — {len(arr.history)} steps recorded")
