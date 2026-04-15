"""Comb sort visualization example."""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from visortpy import VisualArray, create_video

if __name__ == '__main__':
    N = 80
    arr = VisualArray([random.randint(1, 100) for _ in range(N)])

    gap = len(arr)
    shrink = 1.3
    sorted_ = False

    while not sorted_:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_ = True
        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr.swap(i, i + gap)
                sorted_ = False

    create_video(
        arr.history,
        output="comb_sort.mp4",
        fps=80,
        bar_color="#e67e22",
        show_xaxis=False,
        show_yaxis=False,
        final_sweep=True,
        num_workers=8,
    )
    print(f"Done — {len(arr.history)} steps recorded")
