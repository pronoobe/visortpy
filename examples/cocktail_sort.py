"""Cocktail shaker sort visualization example."""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from visortpy import VisualArray, create_video

if __name__ == '__main__':
    N = 50
    arr = VisualArray([random.randint(1, 100) for _ in range(N)])

    swapped = True
    start, end = 0, len(arr) - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr.swap(i, i + 1)
                swapped = True
        if not swapped:
            break
        end -= 1
        swapped = False
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr.swap(i, i + 1)
                swapped = True
        start += 1

    create_video(
        arr.history,
        output="cocktail_sort.mp4",
        fps=60,
        bar_color="#9b59b6",
        show_xaxis=False,
        show_yaxis=False,
        final_sweep=True,
        num_workers=8,
    )
    print(f"Done — {len(arr.history)} steps recorded")
