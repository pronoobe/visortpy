"""Gnome sort visualization example."""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from visortpy import VisualArray, create_video

if __name__ == '__main__':
    N = 40
    arr = VisualArray([random.randint(1, 100) for _ in range(N)])

    i = 0
    while i < len(arr):
        if i == 0 or arr[i] >= arr[i - 1]:
            i += 1
        else:
            arr.swap(i, i - 1)
            i -= 1

    create_video(
        arr.history,
        output="gnome_sort.mp4",
        fps=60,
        bar_color="#1abc9c",
        show_xaxis=False,
        show_yaxis=False,
        final_sweep=True,
        num_workers=8,
    )
    print(f"Done — {len(arr.history)} steps recorded")
