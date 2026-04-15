"""Shell sort visualization example."""
import sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from visortpy import VisualArray, create_video

if __name__ == '__main__':
    N = 80
    arr = VisualArray([random.randint(1, 100) for _ in range(N)])

    gap = len(arr) // 2
    while gap > 0:
        for i in range(gap, len(arr)):
            j = i
            while j >= gap and arr[j] < arr[j - gap]:
                arr.swap(j, j - gap)
                j -= gap
        gap //= 2

    create_video(
        arr.history,
        output="shell_sort.mp4",
        fps=80,
        show_xaxis=False,
        show_yaxis=False,
        final_sweep=True,
        num_workers=8,
    )
    print(f"Done — {len(arr.history)} steps recorded")
