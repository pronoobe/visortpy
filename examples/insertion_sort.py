"""Insertion sort visualization example."""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from visortpy import VisualArray, create_video

if __name__ == '__main__':
    N = 50
    arr = VisualArray([random.randint(1, 100) for _ in range(N)])

    for i in range(1, len(arr)):
        j = i
        while j > 0 and arr[j] < arr[j - 1]:
            arr.swap(j, j - 1)
            j -= 1

    create_video(
        arr.history,
        output="insertion_sort.mp4",
        fps=60,
        show_xaxis=False,
        show_yaxis=False,
        final_sweep=True,
        num_workers=8,
    )
    print(f"Done — {len(arr.history)} steps recorded")
