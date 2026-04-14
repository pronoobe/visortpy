from visortpy import VisualArray, create_video

def stalin_sort_visual(arr):
    """
    斯大林排序可视化实现
    不符合顺序的元素会被"送往古拉格"（标记为0并高亮显示）
    """
    if len(arr) <= 1:
        return arr
    
    # 记录当前最大值的位置
    max_idx = 0
    
    for i in range(1, len(arr)):
        # 比较当前元素与当前最大值
        # 高亮正在比较的两个元素
        arr.compare(max_idx, i)
        
        if arr[i] >= arr[max_idx]:
            # 符合顺序，保留！更新最大值位置
            max_idx = i
        else:
            # 不符合顺序，送往"古拉格"！
            # 这里我们用 swap 来模拟删除效果（与0交换）
            # 实际效果是该位置被"清除"
            arr[i] = 0  # 标记为已删除（古拉格）
    
    return arr

# 测试数据
data = [1, 2, 5, 3, 5, 7, 2, 8, 4, 9]
print(f"原始数组: {data}")

arr = VisualArray(data)
stalin_sort_visual(arr)

# 生成动画 - 使用深色主题更适合"古拉格"氛围
create_video(
    arr.history, 
    output="stalin_sort.gif", 
    fps=2,
    style="dark",
    bar_color="#4a90d9",      # 正常柱子颜色
    highlight_compare="#e74c3c",  # 比较时高亮（红色警告）
    highlight_swap="#2c3e50",   # "删除"后的颜色（深灰色-古拉格）
    final_sweep=True,
    sweep_color="#27ae60"     # 最终存活的元素变绿
)

print("斯大林排序完成！被送往古拉格的元素标记为0")
print(f"幸存的有序序列: {[x for x in data if x != 0]}")