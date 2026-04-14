from visortpy import VisualArray, create_video

def merge_sort(arr, left, right):
    """
    归并排序递归函数
    """
    if left < right:
        mid = (left + right) // 2

        # 递归排序左右两部分
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)

        # 合并两个有序子数组
        merge(arr, left, mid, right)


def merge(arr, left, mid, right):
    """
    合并 arr[left..mid] 和 arr[mid+1..right]
    """
    # 创建临时数组存放左半部分（深拷贝数值，避免引用问题）
    left_part = [arr[i] for i in range(left, mid + 1)]
    right_part = [arr[j] for j in range(mid + 1, right + 1)]

    i = j = 0
    k = left

    # 归并过程：每次比较左、右数组当前元素，将较小者放回原数组
    while i < len(left_part) and j < len(right_part):
        # 比较操作：这里会触发比较高亮（默认红色）
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]   # 写入操作：触发写入高亮
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1

    # 处理剩余元素
    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1


if __name__ == "__main__":
    # 1. 创建一个包含 20 个元素的乱序数组，用于展示更丰富的动画
    original_data = [42, 17, 89, 3, 56, 21, 74, 9, 68, 33,
                     5, 91, 27, 50, 12, 81, 36, 64, 19, 70]
    arr = VisualArray(original_data)

    # 2. 执行归并排序（算法本身完全使用原生 Python 语法）
    merge_sort(arr, 0, len(arr) - 1)

    # 3. 生成动画，展示所有常用配置项
    create_video(
        arr.history,                       # 自动记录的操作历史
        output="merge_sort_demo.gif",      # 输出文件名（支持 .gif / .mp4）
        fps=6,                             # 帧率：每秒 6 帧，动画速度适中
        style="dark",                      # 预设风格："default", "dark", "sound"
        bar_color="#FFA07A",               # 默认柱状图颜色（浅鲑鱼色）
        highlight_compare="#FF4500",       # 比较时的高亮色（橙红色）
        highlight_swap="#32CD32",          # 交换/写入时的高亮色（酸橙绿）
        final_sweep=True,                  # 排序完成后从左到右绿色扫掠
        sweep_color="#00FA9A"              # 扫掠动画的柱子颜色（中等春绿色）
    )

    print("动画已生成：merge_sort_demo.gif")