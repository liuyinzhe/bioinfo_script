# 导入 sys 模块，用于输出警告信息到标准错误流
import sys
# 导入 bisect 模块，提供二分查找功能，用于在有序列表中快速定位
import bisect
# 从 array 模块导入 array 类，用于创建紧凑的整型数组（'I'表示无符号整数）
from array import array
# 从 intervaltree 库导入 IntervalTree 类，用于快速存储和查询区间
from intervaltree import IntervalTree


def parse_bed_file(bed_file):
    """
    解析 BED 文件，返回染色体到 IntervalTree 的字典
    同时返回原始区间列表（用于后续合并）
    """
    # 初始化字典: 键为染色体名称，值为该染色体对应的区间树
    chrom_trees = {}
    # 初始化字典: 键为染色体名称，值为该染色体上所有原始区间的列表，每个元素为 (start, end) 元组
    raw_intervals = {}  # chrom -> list of (start, end)
    
    # 打开 BED 文件进行读取
    with open(bed_file, 'r') as f:
        # 逐行遍历文件，enumerate 从 1 开始计数行号，用于错误提示
        for line_num, line in enumerate(f, 1):
            # 去除行首尾空白字符（包括换行符）
            line = line.strip()
            # 如果是空行或以 # 开头的注释行，则跳过
            if not line or line.startswith('#'):
                continue
            # 以制表符分隔行内容，得到各个字段
            parts = line.split('\t')
            # 如果字段数少于 3，说明缺少染色质、起始或结束位置，视为无效行
            if len(parts) < 3:
                # 输出警告信息到标准错误，指出行号和内容
                print(f"Warning: Skipping invalid BED line {line_num}: {line}", file=sys.stderr)
                continue
            # 取第一列为染色体名称
            chrom = parts[0]
            # 取第二列为起始位置，转换为整数（BED 格式通常为 0-based）
            start = int(parts[1])
            # 取第三列为结束位置，转换为整数
            end = int(parts[2])
            # 如果起始等于结束，该区间长度为 0，跳过不处理
            if start == end:
                continue 
            if start > end:
                continue
            # 如果该染色体尚未在字典中出现，则创建对应的 IntervalTree 和空列表
            if chrom not in chrom_trees:
                chrom_trees[chrom] = IntervalTree()
                raw_intervals[chrom] = []
            # 将区间添加到 IntervalTree 中，区间键为 start:end，值为 (start, end) 元组
            # print(f"{chrom}:{start}-{end}")
            chrom_trees[chrom][start:end] = (start, end)
            # 同时将区间添加到原始区间列表中，用于后续合并操作
            raw_intervals[chrom].append((start, end))
    
    # 返回构建好的区间树字典和原始区间列表字典
    return chrom_trees, raw_intervals


def merge_intervals(intervals):
    """
    合并重叠或相邻的区间，返回排序后的非重叠区间列表
    """
    # 若输入区间列表为空，直接返回空列表
    if not intervals:
        return []
    # 对所有区间按起始位置进行升序排序
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    # 初始化合并后的区间列表
    merged = []
    # 取第一个区间的起始和结束作为当前合并区间的起点
    curr_start, curr_end = sorted_intervals[0]
    # 遍历剩余区间
    for start, end in sorted_intervals[1:]:
        # 如果当前区间的起始 <= 当前合并区间的结束，说明存在重叠或恰好相邻
        if start <= curr_end:  # 重叠或相邻
            # 扩展当前合并区间的结束位置为两者的最大值
            curr_end = max(curr_end, end)
        else:
            # 不重叠，将当前合并区间加入结果列表
            merged.append((curr_start, curr_end))
            # 更新当前合并区间为新的区间
            curr_start, curr_end = start, end
    # 循环结束后，将最后一个合并区间加入列表
    merged.append((curr_start, curr_end))
    # 返回合并后的区间列表
    return merged


def build_coverage_arrays(chrom_trees, raw_intervals):
    """
    为每条染色体构建覆盖深度数组，并返回映射关系
    返回:
        coverage_arrays: dict chrom -> array('I') 长度为合并后总碱基数
        chrom_index_map: dict chrom -> (merged_intervals, starts, offsets)
            merged_intervals: 合并后的区间列表 [(start, end), ...]
            starts: 每个区间的起始位置列表 [start1, start2, ...]
            offsets: 每个区间在数组中的起始索引 [offset1, offset2, ...]
    """
    # 初始化字典，存储每条染色体对应的覆盖率数组
    coverage_arrays = {}
    # 初始化字典，存储每条染色体的位置映射信息
    chrom_index_map = {}
    
    # 遍历所有染色体（只处理在区间树中出现的染色体）
    for chrom in chrom_trees.keys():
        # 获取该染色体的原始区间列表，如果未记录则为空列表
        raw = raw_intervals.get(chrom, [])
        # 对原始区间进行合并，得到非重叠且相邻合并的区间列表
        merged = merge_intervals(raw)
        # 计算合并后所有区间的总碱基数（距离和）
        total_len = sum(end - start for start, end in merged)
        
        # 创建一个总长度为 total_len 的无符号整数数组，初始全为 0
        # 注意: array('I', [0]) * total_len 会复制数组内容多次
        arr = array('I', [0]) * total_len
        # 将该数组存入覆盖数组字典，键为染色体名称
        coverage_arrays[chrom] = arr
        
        # 建立从基因组位置到数组索引的映射
        # starts 列表将存储每个合并区间的起始基因组坐标
        starts = []
        # offsets 列表将存储每个合并区间在覆盖数组中对应的起始索引（偏移量）
        offsets = []
        # 当前在数组中的累积偏移量，初始为 0
        offset = 0
        # 遍历合并后的每个区间
        for start, end in merged:
            # 记录该区间的起始坐标
            starts.append(start)
            # 记录该区间在数组中的起始索引
            offsets.append(offset)
            # 更新偏移量，加上该区间的长度
            offset += (end - start)
        
        # 将合并区间列表、起始坐标列表和偏移列表一起存入索引映射字典
        chrom_index_map[chrom] = (merged, starts, offsets)
    
    # 返回覆盖数组和索引映射字典
    return coverage_arrays, chrom_index_map


def get_array_index(pos, starts, offsets, merged_intervals):
    """
    根据基因组位置 pos (0-based) 查找在覆盖数组中的索引
    若不在任何合并区间内，返回 None
    """
    # 利用 bisect_right 查找 pos 应该插入 starts 列表中的位置索引，减 1 得到最后一个起始 <= pos 的区间索引
    idx = bisect.bisect_right(starts, pos) - 1
    # 如果 idx 小于 0，说明 pos 比所有起始位置都小，不在任何区间内
    if idx < 0:
        return None
    # 取出对应区间的起始和结束
    start, end = merged_intervals[idx]
    # 判断 pos 是否在该区间内（包含起始，不包含结束，确保 0-based 半开区间吻合 BED 惯例）
    if start <= pos < end:
        # 返回偏移量 + (pos - start)，得到在覆盖数组中的具体索引
        return offsets[idx] + (pos - start)
    # 若不在区间内，返回 None
    return None


def main():
    chrom_trees, raw_intervals = parse_bed_file("vv.bed")
    '''
    {
        'chr7': IntervalTree(
                    [   
                        Interval(906676, 912305, (906676, 912305)), 
                        Interval(1372081, 1380835, (1372081, 1380835)), 
                        Interval(13113098, 13119839, (13113098, 13119839))
                    ]
                )

    }
    '''
    # print(chrom_trees)
    for chrom in raw_intervals:
        merged = merge_intervals(raw_intervals[chrom])
        total_len = sum(end - start for start, end in merged)
        # print(merged)
        # [(6493136, 6493937), (11633369, 11634750)]
    
    # pass

    # get_array_index 示例
    # 首先准备一些合并后的区间数据，模拟来自某条染色体
    merged_intervals = [(100, 200), (300, 500), (600, 700)]
    # starts 列表是每个区间的起始
    starts = [100, 300, 600]
    # offsets 列表是每个区间在覆盖率数组中的起始索引，计算方式：每个区间长度分别为100,200,100，累计偏移为0,100,300
    offsets = [0, 100, 300]

    # 测试几个位置
    # 位置150: 在第一个区间内
    idx = get_array_index(150, starts, offsets, merged_intervals)
    print(f"Position 150 -> index {idx}")  # 预期：offset[0] + (150-100) = 0+50 = 50

    # 位置350: 在第二个区间内
    idx = get_array_index(350, starts, offsets, merged_intervals)
    print(f"Position 350 -> index {idx}")  # 预期：100 + (350-300) = 150

    # 位置550: 不在任何区间内
    idx = get_array_index(550, starts, offsets, merged_intervals)
    print(f"Position 550 -> index {idx}")  # 预期：None

    # 位置700: 不在区间内（因为半开区间，end不包含）
    idx = get_array_index(700, starts, offsets, merged_intervals)
    print(f"Position 700 -> index {idx}")  # 预期：None


if __name__ == "__main__":
    main()
