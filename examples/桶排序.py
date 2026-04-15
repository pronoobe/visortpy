import math
from visortpy import VisualArray, create_video

def bucket_sort(arr: VisualArray):
    """
    对 VisualArray 执行桶排序。
    操作会被自动记录，用于生成可视化动画。
    """
    n = len(arr)
    if n == 0:
        return

    # 1. 找到数组中的最小值和最大值（会触发读取操作，记录在 history 中）
    min_val = arr[0]
    max_val = arr[0]
    for i in range(1, n):
        val = arr[i]          # 读取操作，记录高亮
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val

    # 如果所有元素相同，直接返回
    if min_val == max_val:
        return

    # 2. 创建桶（普通 Python 列表，不会记录操作）
    bucket_count = min(n, 10)  # 桶数量，可调整
    buckets = [[] for _ in range(bucket_count)]

    # 计算每个桶的区间范围
    value_range = max_val - min_val
    bucket_size = value_range / bucket_count

    # 3. 将元素分配到桶中（读取每个元素，触发读取高亮）
    for i in range(n):
        val = arr[i]                        # 读取操作
        # 计算桶索引（确保索引在 [0, bucket_count-1] 内）
        idx = int((val - min_val) / bucket_size)
        if idx == bucket_count:             # 处理边界情况（最大值）
            idx -= 1
        buckets[idx].append(val)

    # 4. 对每个桶内部进行排序（使用 Python 内置排序，不产生可视化记录）
    for bucket in buckets:
        bucket.sort()

    # 5. 将桶中元素按顺序写回原数组（每个写入操作都会被记录，并高亮显示）
    write_pos = 0
    for bucket in buckets:
        for val in bucket:
            arr[write_pos] = val            # 写入操作，记录高亮（通常为绿色）
            write_pos += 1

# -------------------- 运行示例 --------------------
if __name__ == "__main__":
    # 创建测试数据
    data = [29, 10, 14, 37, 13, 42, 7, 21, 18, 33]

    # 用 VisualArray 包装数据，启用操作记录
    arr = VisualArray(data)

    # 执行桶排序（所有读取、写入操作会被自动记录）
    bucket_sort(arr)

    # 生成可视化动画
    create_video(
        arr.history,                 # 操作历史记录
        output="bucket_sort.gif",    # 输出文件名（支持 .mp4 / .gif）
        fps=4,                       # 帧率
        style="default",             # 可选 "dark" 或自定义颜色
        final_sweep=True,            # 排序完成后，从左到右扫一遍绿色
        show_axes=True,              # 显示坐标轴
        num_workers=2,               # 并行渲染加速（根据 CPU 核心数调整）
        show_progress=True           # 显示进度条
    )

    print("✅ 桶排序动画已生成：bucket_sort.gif")