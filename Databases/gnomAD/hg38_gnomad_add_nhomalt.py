#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hg38_gnomad_add_nhomalt.py
==========================
给 **ANNOVAR avinput 风格** 的 gnomAD 表(如 ``hg38_gnomad41_genome.txt``)
追加一列 ``gnomad_number_of_homozygotes``(gnomAD 同型合子个体数 nhomalt)。

数据流::

    hg38_gnomad41_genome.txt            gnomad_nhomalt_dic.pkl.gz
    (Chr Start End Ref Alt <AF...>)     (由 build_pkl4_annovar_add_nhomalt.py 生成)
                    \\                     /
                     \\                   /
                      v                 v
            hg38_gnomad41_genome_nhomalt.txt
            (原文件 + 末列 gnomad_number_of_homozygotes, 未命中写 '-')

key = "\\t".join([Chr, Start, End, Ref, Alt])   # 两个脚本必须一致

* 输入行的前 5 列**原样保留**(只去掉行尾 CR/LF), 保证下游按列解析不变;
* 表头自动识别(``#Chr`` 或 ``Chr`` 开头), 输出表头同步追加列名;
* 支持合并字典(单个 pkl.gz)与**按染色体分片字典**目录(``{chrom}.nhomalt.pkl.gz``),
  分片模式只驻留当前染色体字典, 显著降低内存峰值;
* 结束时输出命中/未命中统计, 用于快速发现 key 约定不一致(例如坐标偏移、chr 前缀差异)。

用法::

    python hg38_gnomad_add_nhomalt.py                       # 默认路径 + 默认文件名
    python hg38_gnomad_add_nhomalt.py -i demo.txt -o demo.nhomalt.txt -D ./gnomad_nhomalt_dic.pkl.gz
    python hg38_gnomad_add_nhomalt.py -D ./shards --shard-pattern '{chrom}.nhomalt.pkl.gz'
"""

from __future__ import annotations

import argparse
import datetime
import gzip
import logging
import pickle
import sys
import time
from collections import Counter
from pathlib import Path

#: 默认字典路径(与 build_pkl4_annovar_add_nhomalt.py 的输出保持一致)
DEFAULT_DATABASE = "/data/database/gnomAD/Genomes_table/gnomad_nhomalt_dic.pkl.gz"
DEFAULT_INPUT = "hg38_gnomad41_genome.txt"
DEFAULT_OUTPUT = "hg38_gnomad41_genome_nhomalt.txt"
DEFAULT_COLUMN = "gnomad_number_of_homozygotes"
DEFAULT_MISSING = "-"
DEFAULT_SHARD_PATTERN = "{chrom}.nhomalt.pkl.gz"

log = logging.getLogger(Path(__file__).stem)


# --------------------------------------------------------------------------- #
# 字典加载
# --------------------------------------------------------------------------- #
class MonoDictLookup:
    """合并字典(单个 pkl.gz, 全部读入内存)。"""

    def __init__(self, path):
        with gzip.open(path, mode="rb") as pkl_gz:
            self.dic = pickle.load(pkl_gz)
        log.info("载入字典 %s (keys=%d)", path, len(self.dic))

    def get(self, chrom, key):
        return self.dic.get(key)

    def close(self):
        self.dic = None


class ShardDictLookup:
    """按染色体分片字典, 只驻留 ``cache_size`` 个染色体(默认 2)。

    分片文件名由 ``--shard-pattern`` 决定, 默认 ``{chrom}.nhomalt.pkl.gz``。
    """

    def __init__(self, shard_dir, pattern=DEFAULT_SHARD_PATTERN, cache_size=2):
        self.dir = Path(shard_dir)
        self.pattern = pattern
        self.cache_size = max(int(cache_size), 1)
        self._cache = {}            # chrom -> dict
        self._order = []            # LRU 顺序
        self.loaded = Counter()     # 实际加载过的分片
        self.missing_shard = set()  # 不存在的分片
        if not self.dir.is_dir():
            raise NotADirectoryError("分片目录不存在: {}".format(self.dir))

    def _load(self, chrom):
        path = self.dir.joinpath(self.pattern.format(chrom=chrom))
        if not path.is_file():
            self.missing_shard.add(chrom)
            log.warning("分片不存在: %s", path)
            return None
        with gzip.open(path, mode="rb") as pkl_gz:
            dic = pickle.load(pkl_gz)
        log.info("载入分片 %s (keys=%d)", path, len(dic))
        self.loaded[chrom] += 1
        return dic

    def get(self, chrom, key):
        dic = self._cache.get(chrom)
        if dic is None:
            if chrom in self.missing_shard:
                return None
            dic = self._load(chrom)
            if dic is None:
                return None
            self._cache[chrom] = dic
            self._order.append(chrom)
            if len(self._order) > self.cache_size:
                old = self._order.pop(0)
                if old in self._cache and old != chrom:
                    del self._cache[old]
        return dic.get(key)

    def close(self):
        self._cache.clear()
        self._order.clear()


def resolve_database(database):
    """解析字典来源: 单个 pkl.gz 文件 或 分片目录。

    查找顺序: 显式路径 -> 当前目录同名文件 -> 脚本目录同名文件。
    """
    candidates = [Path(database),
                  Path.cwd().joinpath(Path(database).name),
                  Path(__file__).resolve().parent.joinpath(Path(database).name)]
    for path in candidates:
        if path.is_dir() or path.is_file():
            return path
    raise FileNotFoundError(
        "找不到字典 {}; 已尝试: {}".format(database, [str(c) for c in candidates]))


# --------------------------------------------------------------------------- #
# 行解析
# --------------------------------------------------------------------------- #
def parse_line(line):
    """解析一行 avinput 记录, 只做 5 次 find + 4 次小切片(不复制行尾注释列)。

    :param line: 已去掉行尾换行符的原始行
    :return: ``(key, chrom, ref, alt)``; 字段不足 5 个时返回 ``(None, None, None, None)``
    """
    t1 = line.find("\t")
    if t1 < 0:
        return None, None, None, None
    t2 = line.find("\t", t1 + 1)
    if t2 < 0:
        return None, None, None, None
    t3 = line.find("\t", t2 + 1)
    if t3 < 0:
        return None, None, None, None
    t4 = line.find("\t", t3 + 1)
    if t4 < 0:
        return None, None, None, None
    t5 = line.find("\t", t4 + 1)
    chrom = line[:t1]
    ref = line[t3 + 1:t4]
    alt = line[t4 + 1:t5] if t5 >= 0 else line[t4 + 1:]
    key = line if t5 < 0 else line[:t5]
    return key, chrom, ref, alt


def key_of_line(line):
    """仅取 key(兼容旧接口, 便于测试)。"""
    return parse_line(line)[0]


def class_of(ref, alt):
    """按 ANNOVAR avinput 形态分类: snv / mnv / del / ins / other。"""
    if ref == "-":
        return "ins"
    if alt == "-":
        return "del"
    if len(ref) == len(alt):
        return "snv" if len(ref) == 1 else "mnv"
    return "other"


def is_header_line(line):
    """判断首行是否为表头: 以 '#' 开头, 或第 2 列不是整数坐标。"""
    if line.startswith("#"):
        return True
    parts = line.split("\t", 2)
    if len(parts) < 2:
        return False
    try:
        int(parts[1])
        return False
    except ValueError:
        return True


def apply_chrom_alias(key, alias):
    """可选: 统一 chr 前缀(chr1 <-> 1), 用于字典与输入表染色体命名不一致的情况。"""
    if not key or alias == "none":
        return key
    chrom, sep, rest = key.partition("\t")
    if alias == "strip" and chrom.lower().startswith("chr"):
        chrom = chrom[3:]
    elif alias == "add" and not chrom.lower().startswith("chr"):
        chrom = "chr" + chrom
    return chrom + sep + rest


def open_text(path, mode="rt"):
    """透明支持 .gz / 普通文本。"""
    path = str(path)
    if path.endswith(".gz"):
        return gzip.open(path, mode, newline="")
    return open(path, mode, newline="")


# --------------------------------------------------------------------------- #
# 主流程
# --------------------------------------------------------------------------- #
def get_args(argv=None):
    parser = argparse.ArgumentParser(
        description="给 ANNOVAR avinput 风格 gnomAD 表追加 nhomalt 列",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-i", "--input", default=DEFAULT_INPUT,
                        help="输入表(ANNOVAR avinput 风格, 支持 .gz)")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT,
                        help="输出表")
    parser.add_argument("-D", "--database", default=DEFAULT_DATABASE,
                        help="字典文件(gnomad_nhomalt_dic.pkl.gz)或分片字典目录")
    parser.add_argument("--shard-pattern", default=DEFAULT_SHARD_PATTERN,
                        help="分片字典文件名模板, 需含 {chrom}")
    parser.add_argument("--shard-cache", type=int, default=2,
                        help="分片模式下同时驻留的染色体字典数量")
    parser.add_argument("--column-name", default=DEFAULT_COLUMN,
                        help="追加列的表头名")
    parser.add_argument("--missing", default=DEFAULT_MISSING,
                        help="未命中时写入的值")
    parser.add_argument("--chrom-alias", choices=["none", "strip", "add"],
                        default="none",
                        help="染色体命名统一: strip 去掉 chr 前缀, add 添加 chr 前缀")
    parser.add_argument("--progress", type=int, default=1000000,
                        help="每处理多少行打印一次进度(0=关闭)")
    parser.add_argument("--log", default=None, help="日志文件(默认只输出到终端)")
    return parser.parse_args(argv)


def setup_logging(log_path=None):
    formatter = logging.Formatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    root.addHandler(sh)
    if log_path:
        fh = logging.FileHandler(log_path, mode="w", encoding="utf-8")
        fh.setFormatter(formatter)
        root.addHandler(fh)


def main(argv=None):
    args = get_args(argv)
    setup_logging(args.log)
    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.is_file():
        raise FileNotFoundError("输入表不存在: {}".format(input_path))

    db_path = resolve_database(args.database)
    if db_path.is_dir():
        lookup = ShardDictLookup(db_path, args.shard_pattern, args.shard_cache)
        log.info("字典来源: 分片目录 %s (pattern=%s)", db_path, args.shard_pattern)
    else:
        lookup = MonoDictLookup(db_path)
        log.info("字典来源: 合并字典 %s", db_path)

    stats = Counter()
    stats_by_class = Counter()
    hit_by_class = Counter()
    # 热循环用局部变量计数(实测比每行更新 dict/Counter 快 15%+)
    n_hit = n_miss = n_blank = n_bad = 0
    c_snv = c_mnv = c_del = c_ins = c_other = 0
    h_snv = h_mnv = h_del = h_ins = h_other = 0
    first_line = True
    use_alias = args.chrom_alias != "none"
    progress_step = max(int(args.progress), 0)
    missing = args.missing

    try:
        with open_text(input_path) as fh, open_text(output_path, "wt") as out:
            write = out.write
            for line in fh:
                line = line.rstrip("\r\n")   # 行尾换行先去掉, 输出统一 '\n'
                if first_line:
                    first_line = False
                    if is_header_line(line):
                        write(line + "\t" + args.column_name + "\n")
                        continue
                if not line or line.isspace():
                    # 空行原样透传(不追加列), 避免破坏原有行结构
                    n_blank += 1
                    write(line + "\n")
                    continue
                key, chrom, ref, alt = parse_line(line)
                if key is None:
                    n_bad += 1
                    write(line + "\n")
                    continue
                if use_alias:
                    key = apply_chrom_alias(key, args.chrom_alias)
                    chrom = key.split("\t", 1)[0]
                # 分类(便于定位“某类变异全未命中”的 key 约定问题)
                if ref == "-":
                    c_ins += 1
                elif alt == "-":
                    c_del += 1
                elif len(ref) == len(alt):
                    if len(ref) == 1:
                        c_snv += 1
                    else:
                        c_mnv += 1
                else:
                    c_other += 1
                value = lookup.get(chrom, key)
                if value is None:
                    n_miss += 1
                    write(line + "\t" + missing + "\n")
                    continue
                n_hit += 1
                if ref == "-":
                    h_ins += 1
                elif alt == "-":
                    h_del += 1
                elif len(ref) == len(alt):
                    if len(ref) == 1:
                        h_snv += 1
                    else:
                        h_mnv += 1
                else:
                    h_other += 1
                write(line + "\t" + str(value) + "\n")
                if progress_step and (n_hit + n_miss) % progress_step == 0:
                    log.info("已处理 %d 行, 命中 %d, 未命中 %d",
                             n_hit + n_miss, n_hit, n_miss)
    finally:
        lookup.close()

    stats.update({"lines": n_hit + n_miss + n_blank + n_bad, "hit": n_hit,
                  "miss": n_miss, "blank_lines": n_blank, "malformed": n_bad})
    stats_by_class.update({"snv": c_snv, "mnv": c_mnv, "del": c_del,
                           "ins": c_ins, "other": c_other})
    hit_by_class.update({"snv": h_snv, "mnv": h_mnv, "del": h_del,
                         "ins": h_ins, "other": h_other})
    log.info("输出文件: %s", output_path)
    report(stats, stats_by_class, hit_by_class)
    return 0


def report(stats, stats_by_class, hit_by_class):
    total = stats["hit"] + stats["miss"]
    rate = stats["hit"] / total if total else 0.0
    log.info("统计: 总行数=%d(variant=%d, 空行=%d, 字段不足=%d), 命中=%d, 未命中=%d, "
             "命中率=%.2f%%", stats["lines"], total, stats["blank_lines"],
             stats["malformed"], stats["hit"], stats["miss"], rate * 100)
    for cls in sorted(stats_by_class):
        n = stats_by_class[cls]
        h = hit_by_class[cls]
        log.info("  分类 %-9s 行数=%-10d 命中=%-10d 命中率=%.2f%%",
                 cls, n, h, (h / n * 100 if n else 0.0))

    # 健全性检查: 帮助快速定位 key 约定不一致(坐标偏移 / chr 前缀 / 字典版本不对)
    if total >= 1000 and rate == 0.0:
        log.error("命中率为 0! 请检查字典与输入表是否同一 genome build、是否为 "
                  "ANNOVAR avinput 风格 key(start 是否偏移)、字典是否由配套的 "
                  "build_pkl4_annovar_add_nhomalt.py 生成")
    elif total >= 1000 and rate < 0.3:
        log.warning("命中率偏低(%.2f%%), 建议检查 key 约定/染色体命名/字典版本",
                    rate * 100)
    snv_n = stats_by_class.get("snv", 0)
    if snv_n >= 1000 and hit_by_class.get("snv", 0) / snv_n < 0.5:
        log.warning("SNV 命中率偏低, 大概率是坐标体系或 chr 前缀不一致")


if __name__ == "__main__":
    start_time = time.perf_counter()
    try:
        sys.exit(main())
    finally:
        end_time = time.perf_counter()
        message = "%s %s %s\n" % (
            "main()", "use", str(datetime.timedelta(seconds=end_time - start_time)))
        print(message)
        logging.info(message)
