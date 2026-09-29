#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_pkl4_annovar_add_nhomalt.py
=================================
把 gnomAD(Genomes) 的“逐染色体转换表”(``*.txt.gz``) 构建成
**ANNOVAR avinput 风格 key -> nhomalt** 的字典，并序列化为
``gnomad_nhomalt_dic.pkl.gz``，供 ``hg38_gnomad_add_nhomalt.py`` 查询。

输入表列(至少, tab 分隔, 首行为表头)::

    chrom   start   stop    ref     alt     allele_type     AF      AF_eas  nhomalt

其中 ``start/stop/ref/alt`` 是 **VCF 风格**(indel 带锚定碱基):

* SNV        : ``chr1  10000  10000  A   G``
* 缺失 del   : ``chr1  10108  10114  CAACCCT  C``   (锚定碱基 C + 缺失 AACCCT)
* 插入 ins   : ``chr1  10108  10108  C        CA``  (锚定碱基 C + 插入 A)

输出 key 规范(tab 分隔, 1-based, 与 ANNOVAR avinput 完全一致)::

    "\\t".join([chrom, start, stop, ref, alt])

ANNOVAR avinput 的 indel 约定(官方文档):
https://annovar.openbioinformatics.org/en/latest/user-guide/input/
https://github.com/wglab/doc-annovar/blob/master/docs/user-guide/input.md

* 缺失: ``1  13211293  13211294  TC  -``  -> start = VCF POS + 1,
  stop = VCF POS + len(REF) - 1, ref = REF[1:], alt = ``-``
* 插入: ``1  11403596  11403596  -   AT`` -> start = stop = VCF POS,
  ref = ``-``, alt = ALT[1:]
* 替换/block substitution(REF/ALT 等长): 5 列原样保留

即 **只有缺失需要把 start 右移 1 位**。旧版脚本漏了这一步, 会把所有 del 漏掉
(真实 chrY 数据实测漏检 83152/83152, 见文档 BUG#1)。

性能要点(相对旧版逐行 ``zip(polars Series)`` 循环):
  * key 用 polars 表达式一次性生成(不用 Python 逐行拼接);
  * 不做 ``unique()``(它比 dict 覆盖贵得多), 用 ``dict.update`` 完成去重/优先级;
  * 重复 key 只在真正出现时才走“先出现优先”的慢路径;
  * 不再对每条重复记录打日志(旧版重复日志本身可能是主要耗时);
  * ``nhomalt`` 尽量存 int(小整数是 CPython 缓存对象, 省内存)；
  * pickle 用最高协议 + gzip level 1(压缩速度优先, 可用 --compress-level 调回 9)。

用法::

    python build_pkl4_annovar_add_nhomalt.py                      # 当前目录 *.txt.gz -> ./gnomad_nhomalt_dic.pkl.gz
    python build_pkl4_annovar_add_nhomalt.py -d /data/gnomad/Genomes_table \\
        -o /data/database/gnomAD/Genomes_table/gnomad_nhomalt_dic.pkl.gz
    python build_pkl4_annovar_add_nhomalt.py --shard-dir ./shards  # 额外输出按染色体分片字典(降低内存峰值)
"""

from __future__ import annotations

import argparse
import datetime
import gzip
import logging
import pickle
import re
import sys
import time
from collections import Counter
from pathlib import Path

import polars as pl

LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "
DATE_FORMAT = "%Y-%m-%d  %H:%M:%S %A "

#: 构建 key 必需的最小列集合
REQUIRED_COLUMNS = ("chrom", "start", "stop", "ref", "alt", "nhomalt")
#: 可选列(存在时用于交叉校验)
OPTIONAL_COLUMNS = ("allele_type",)
#: 默认输出文件名(与第二个脚本的默认查找路径保持一致)
DEFAULT_OUTPUT_NAME = "gnomad_nhomalt_dic.pkl.gz"
DEFAULT_SHARD_SUFFIX = ".nhomalt.pkl.gz"
#: 输入表自带的 allele_type 取值(用于与序列形态交叉校验)
KNOWN_ALLELE_TYPES = ("snv", "del", "ins")

log = logging.getLogger(Path(__file__).stem)


# --------------------------------------------------------------------------- #
# 基础工具
# --------------------------------------------------------------------------- #
def natural_key(text):
    """自然排序 key：chr1 < chr2 < ... < chr10 < chrX。"""
    return [int(part) if part.isdigit() else part.lower()
            for part in re.split(r"(\d+)", str(text))]


def GetAllFilePaths(pwd, wildcard="*", exclude=None):
    """获取目录下(含子目录)所有匹配文件的全路径列表(排除符号链接/目录)。

    :param pwd: 目录
    :param wildcard: 通配符, 例如 ``*.txt.gz``
    :param exclude: 需要排除的文件名通配符(可迭代), 例如 ``['*nhomalt_dic.pkl.gz']``
    :return: 按自然顺序排序后的路径字符串列表
    """
    exclude = list(exclude or ())
    files_lst = []
    target_path = Path(pwd)
    for child in target_path.rglob(wildcard):
        if child.is_symlink() or child.is_dir() or not child.is_file():
            continue
        if any(child.match(pat) for pat in exclude):
            continue
        files_lst.append(str(child))
    # 排序保证多文件合并顺序可复现(旧版 rglob 顺序依赖文件系统)
    return sorted(files_lst, key=natural_key)


def peek_header(path):
    """只读取(可能是 gzip 的)文件第一行, 返回列名列表。"""
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, mode="rt", newline="") as fh:
        for line in fh:
            line = line.rstrip("\n").rstrip("\r")
            if line.strip():
                return line.split("\t")
    return []


def read_table(path, columns):
    """用 polars 读取 gnomAD 转换表。

    * 全部列按字符串读取(``infer_schema_length=0``, 坐标/AF 不做类型推断);
    * 关闭 quote 解析(基因组文本表不使用 CSV 引号规则);
    * 仅读取需要的列, 减少 IO/解析开销。
    """
    return pl.read_csv(
        path,
        separator="\t",
        infer_schema_length=0,      # 0 => 不推断 schema, 全部 String (polars 官方语义)
        columns=list(columns),
        quote_char=None,
        truncate_ragged_lines=True,
        has_header=True,
    )


# --------------------------------------------------------------------------- #
# key 构建(向量化)
# --------------------------------------------------------------------------- #
def _non_null_frame(df, col):
    """返回 ``col`` 列非空的子集; 全非空时直接复用原 frame(省一次过滤)。"""
    if df[col].null_count() == 0:
        return df
    return df.filter(pl.col(col).is_not_null())


def build_key_frame(df, keep_raw_indel_keys=True, compat_anchor_del=False):
    """把 gnomAD 表展开成 "按优先级排列的 key 块" + 统计信息。

    行分类与产出(polars 表达式全部向量化, 无 Python 逐行循环):

    =================  =====================================================
    输入行形态          产出的 key
    =================  =====================================================
    等长(SNV/MNV)       raw     : chrom start stop ref alt
    纯缺失(len(alt)=1   annovar : chrom start+1 stop ref[1:] -
     且 alt == ref[0])   + raw(可选, 默认保留)
    纯插入(len(ref)=1   annovar : chrom start stop - alt[1:]
     且 ref == alt[0])   + raw(可选, 默认保留)
    其他(复杂 indel/    raw     : chrom start stop ref alt (回退, 尽量不漏)
     未 left-normalize)
    =================  =====================================================

    返回值 ``(blocks, stats)``: ``blocks`` 按**优先级从低到高**排列,
    每项是 ``(frame, key_column)``; 合并字典时后者覆盖前者。
    """
    ref, alt = pl.col("ref"), pl.col("alt")
    ref_len, alt_len = ref.str.len_chars(), alt.str.len_chars()
    start_int = pl.col("start").cast(pl.Int64, strict=False)

    eq_len = ref_len == alt_len                       # 替换(SNV/MNV/blocksub)
    is_del = (alt_len == 1) & (ref_len > 1) & (alt == ref.str.slice(0, 1))
    is_ins = (ref_len == 1) & (alt_len > 1) & (ref == alt.str.slice(0, 1))

    raw_key = pl.concat_str(["chrom", "start", "stop", "ref", "alt"],
                            separator="\t", ignore_nulls=False)
    # 缺失: ANNOVAR 约定 start = VCF POS + 1, ref = REF[1:], alt = '-'
    del_lead = pl.concat_str([
        pl.col("chrom"), (start_int + 1).cast(pl.String), pl.col("stop"),
        ref.str.slice(1), pl.lit("-"),
    ], separator="\t", ignore_nulls=False)
    # 兼容历史数据: 缺失起点不加 1 的写法(仅在 --compat-anchor-del 时生成)
    del_anchor = pl.concat_str([
        pl.col("chrom"), pl.col("start"), pl.col("stop"),
        ref.str.slice(1), pl.lit("-"),
    ], separator="\t", ignore_nulls=False)
    # 插入: ANNOVAR 约定 ref = '-', alt = ALT[1:], start = stop = VCF POS
    ins_annovar = pl.concat_str([
        pl.col("chrom"), pl.col("start"), pl.col("stop"),
        pl.lit("-"), alt.str.slice(1),
    ], separator="\t", ignore_nulls=False)

    shape = (pl.when(eq_len).then(pl.lit("sub"))
             .when(is_del).then(pl.lit("del"))
             .when(is_ins).then(pl.lit("ins"))
             .otherwise(pl.lit("other")))
    # 只有 del/ins 需要额外的 ANNOVAR key; 等长替换的 raw key 就是 ANNOVAR key
    ann_key = (pl.when(is_del & start_int.is_not_null()).then(del_lead)
               .when(is_ins).then(ins_annovar)
               .otherwise(pl.lit(None, dtype=pl.String)))

    new_cols = [raw_key.alias("_raw"), ann_key.alias("_ann")]
    if compat_anchor_del:
        new_cols.append(pl.when(is_del).then(del_anchor)
                        .otherwise(pl.lit(None, dtype=pl.String)).alias("_ann2"))
    # allele_type 与序列形态交叉校验(单次表达式, 用 sum() 聚合, 不额外过滤)
    has_allele_type = "allele_type" in df.columns
    if has_allele_type:
        expect = (pl.when(shape == "sub").then(pl.lit("snv"))
                  .when(shape == "del").then(pl.lit("del"))
                  .when(shape == "ins").then(pl.lit("ins"))
                  .otherwise(pl.col("allele_type")))
        new_cols.append((pl.col("allele_type").is_in(list(KNOWN_ALLELE_TYPES))
                         & (expect != pl.col("allele_type"))).alias("_mismatch"))
    if not keep_raw_indel_keys:
        # 只要等长行的 raw key(indel 只保留 ANNOVAR 风格 key)
        new_cols[0] = pl.when(eq_len).then(raw_key).otherwise(
            pl.lit(None, dtype=pl.String)).alias("_raw")

    df = df.with_columns(new_cols)

    blocks = []
    keys_out = 0
    for col in ("_ann2", "_ann", "_raw"):      # 低优先级 -> 高优先级
        if col not in df.columns:
            continue
        frame = _non_null_frame(df, col)
        if frame.height == 0:
            continue
        keys_out += frame.height
        blocks.append((frame, col))

    stats = {
        "rows_in": df.height,
        "keys_out": keys_out,
    }
    # 分类计数: 一次 select 里做多个聚合(只扫一遍)
    aggs = [is_del.sum().alias("del_rows"), is_ins.sum().alias("ins_rows"),
            (~(eq_len | is_del | is_ins)).sum().alias("unclassified")]
    if has_allele_type:
        aggs.append(pl.col("_mismatch").sum().alias("allele_type_mismatch"))
    row = df.select(aggs).row(0, named=True)
    stats.update({k: int(v or 0) for k, v in row.items()})
    return blocks, stats


def _value_lists(blocks, use_int):
    """把 blocks 转成 [(key_list, value_list), ...] 并统计 key 总数。"""
    expr = (pl.col("nhomalt").cast(pl.Int64, strict=False) if use_int
            else pl.col("nhomalt"))
    out = []
    for frame, col in blocks:
        out.append((frame[col].to_list(),
                    frame.select(expr).to_series().to_list()))
    return out


def int_values_ok(long_frames):
    """判断所有 nhomalt 是否都能无损转 int('007'/'2.0'/'NA' 之类会返回 False)。"""
    for frame in long_frames:
        nh_str = pl.col("nhomalt").cast(pl.String)
        nh_int = nh_str.cast(pl.Int64, strict=False)
        check = frame.select((nh_int.is_not_null()
                              & (nh_int.cast(pl.String) == nh_str)).alias("ok"))
        if not bool(check["ok"].all()):
            return False
    return True


def merge_blocks(blocks, value_type="auto", list_dups=0):
    """按优先级合并各 key 块 -> dict(不含 key 的块已剔除)。

    * 常规路径: ``dict.update`` 顺序覆盖, 后者(更高优先级)胜出; 纯 C 层操作;
    * 出现重复 key 时: 告警, 并改用“高优先级 + 同块内先出现优先”的慢路径,
      使结果与旧版 ``if key not in dic`` 完全一致。
    """
    frames = [frame for frame, _col in blocks]
    ok_int = int_values_ok(frames)
    if value_type == "int" and not ok_int:
        log.warning("nhomalt 存在无法无损转 int 的取值, --value-type int 可能写出 "
                    "null; 建议改用默认的 auto")
    use_int = ok_int if value_type == "auto" else (value_type == "int")
    key_lists = _value_lists(blocks, use_int)
    keys_out = sum(len(k) for k, _v in key_lists)

    dic = {}
    for keys, values in key_lists:
        dic.update(zip(keys, values))
    dups = keys_out - len(dic)
    stats = {"keys_out": keys_out, "intra_file_dups": dups,
             "value_type": "int" if use_int else "str"}

    if dups:
        log.warning("发现 %d 条重复 key(keys=%d, 唯一=%d), 改用『先出现优先』"
                    "(与旧版一致); 建议检查上游是否混用了 VCF 风格与 ANNOVAR 风格",
                    dups, keys_out, len(dic))
        dic = {}
        for idx, (keys, values) in enumerate(reversed(key_lists)):  # 高 -> 低优先级
            if idx == 0:
                # 最高优先级块: 反向 zip 得到“同块内先出现优先”
                dic.update(zip(reversed(keys), reversed(values)))
            else:
                # 低优先级块: 正序 + 不覆盖 = “先出现优先”且不推翻高优先级
                for key, value in zip(keys, values):
                    if key not in dic:
                        dic[key] = value
        if list_dups:
            counter = Counter(k for keys, _v in key_lists for k in keys)
            stats["dup_examples"] = [k for k, n in counter.most_common(200)
                                     if n > 1][:list_dups]
            del counter
        del key_lists
    return dic, stats


# --------------------------------------------------------------------------- #
# 主流程
# --------------------------------------------------------------------------- #
def process_one_file(path, keep_raw_indel_keys=True, compat_anchor_del=False,
                     value_type="auto", list_dups=0):
    """读取单个转换表 -> (dict, stats)。"""
    header = peek_header(path)
    if not header:
        raise ValueError("空文件或无法读取表头: {}".format(path))
    missing = [c for c in REQUIRED_COLUMNS if c not in header]
    if missing:
        raise ValueError(
            "{} 缺少必需列 {}; 实际表头 = {}".format(path, missing, header))
    columns = [c for c in header if c in REQUIRED_COLUMNS + OPTIONAL_COLUMNS]
    df = read_table(path, columns)

    blocks, stats = build_key_frame(
        df, keep_raw_indel_keys=keep_raw_indel_keys,
        compat_anchor_del=compat_anchor_del)
    # 染色体名(用于分片): 首尾相同则视为单染色体, 省一次全列 unique 扫描
    first = df["chrom"][0] if df.height else None
    last = df["chrom"][-1] if df.height else None
    stats["chroms"] = ([first] if first == last
                       else df["chrom"].unique().to_list())
    del df

    dic, merge_stats = merge_blocks(blocks, value_type=value_type,
                                    list_dups=list_dups)
    stats.update(merge_stats)
    stats["dict_size"] = len(dic)
    return dic, stats


def build_parser():
    parser = argparse.ArgumentParser(
        description="构建 ANNOVAR avinput 风格的 gnomAD nhomalt 查询字典(pkl.gz)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-d", "--dir", default=".",
                        help="gnomAD 转换表(*.txt.gz)所在目录")
    parser.add_argument("--pattern", default="*.txt.gz",
                        help="输入文件通配符")
    parser.add_argument("--exclude", nargs="*",
                        default=["*nhomalt_dic.pkl.gz", "*" + DEFAULT_SHARD_SUFFIX],
                        help="需要排除的文件名通配符")
    parser.add_argument("-o", "--output", default=None,
                        help="输出字典文件(默认: <dir>/%s)" % DEFAULT_OUTPUT_NAME)
    parser.add_argument("--shard-dir", default=None,
                        help="额外输出按染色体的分片字典 {chrom}%s(降低查询内存峰值)"
                             % DEFAULT_SHARD_SUFFIX)
    parser.add_argument("--no-shard", action="store_true",
                        help="--shard-dir 存在时也不写分片")
    parser.add_argument("--chrom", nargs="*", default=None,
                        help="只处理指定染色体(例如 --chrom chr1 chr2), 便于分批构建")
    parser.add_argument("--no-raw-indel-keys", action="store_true",
                        help="不写入 indel 的 VCF 风格原始 key(只写 ANNOVAR 风格 key)")
    parser.add_argument("--compat-anchor-del", action="store_true",
                        help="额外写入“缺失起点不加 1”的兼容 key(历史数据兼容)")
    parser.add_argument("--value-type", choices=["auto", "int", "str"], default="auto",
                        help="字典 value 类型: auto=可无损转 int 时用 int(省内存), "
                             "str=与旧版完全一致的字符串")
    parser.add_argument("--compress-level", type=int, default=1,
                        help="pickle.gz 的 gzip 压缩级别(1=快, 9=最小体积)")
    parser.add_argument("--list-dups", type=int, default=0,
                        help="出现重复 key 时打印前 N 条明细(0=不打印)")
    parser.add_argument("--log", default=None,
                        help="日志文件(默认: <dir>/logging.log)")
    return parser


def setup_logging(log_path):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    fh = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    fh.setFormatter(formatter)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    root.addHandler(fh)
    root.addHandler(sh)


def dump_pickle(dic, out_path, compress_level):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(out_path, mode="wb", compresslevel=compress_level) as fh:
        pickle.dump(dic, fh, protocol=pickle.HIGHEST_PROTOCOL)
    return out_path


def main(argv=None):
    args = build_parser().parse_args(argv)
    current_dir = Path(args.dir).resolve()
    output = (Path(args.output) if args.output
              else current_dir.joinpath(DEFAULT_OUTPUT_NAME))
    log_path = Path(args.log) if args.log else current_dir.joinpath("logging.log")
    setup_logging(log_path)

    log.info("参数: %s", vars(args))
    gnomad_txt_lst = GetAllFilePaths(current_dir, args.pattern, exclude=args.exclude)
    if args.chrom:
        wanted = set(args.chrom)
        gnomad_txt_lst = [p for p in gnomad_txt_lst
                          if wanted.intersection(Path(p).name.split("."))]
    if not gnomad_txt_lst:
        raise FileNotFoundError(
            "在 {} 下没有找到匹配 {} 的文件".format(current_dir, args.pattern))

    gnomad_nhomalt_dic = {}
    totals = Counter()
    seen_chroms = set()
    shard_dir = (Path(args.shard_dir).resolve() if args.shard_dir
                 and not args.no_shard else None)
    if shard_dir:
        shard_dir.mkdir(parents=True, exist_ok=True)

    for gzip_txt in gnomad_txt_lst:
        dic, stats = process_one_file(
            gzip_txt,
            keep_raw_indel_keys=not args.no_raw_indel_keys,
            compat_anchor_del=args.compat_anchor_del,
            value_type=args.value_type,
            list_dups=args.list_dups,
        )
        # 分片: 本文件(通常恰为一条染色体)的字典单独落盘, 供查询端按需加载
        if shard_dir:
            chroms = stats["chroms"]
            shard_name = (chroms[0] if len(chroms) == 1
                          else Path(gzip_txt).name.split(".")[0])
            if len(chroms) != 1:
                log.warning("%s 含多条染色体 %s, 分片按文件名命名: %s",
                            gzip_txt, chroms, shard_name)
            shard_path = shard_dir.joinpath(shard_name + DEFAULT_SHARD_SUFFIX)
            dump_pickle(dic, shard_path, args.compress_level)
            log.info("分片写入 %s (keys=%d)", shard_path, len(dic))

        # key 内含染色体: 只有染色体与已处理的重复时, 才可能存在跨文件重复
        overlap = 0
        if seen_chroms.intersection(stats["chroms"]):
            overlap = sum(1 for k in dic if k in gnomad_nhomalt_dic)
        seen_chroms.update(stats["chroms"])

        totals.update({k: v for k, v in stats.items() if isinstance(v, int)})
        totals["cross_file_dups"] += overlap
        gnomad_nhomalt_dic.update(dic)
        totals["dict_size"] = len(gnomad_nhomalt_dic)
        del dic

        log.info("处理完成 %s; 行数=%d, 本文件 key=%d, 合并后 key=%d, del=%d, ins=%d, "
                 "未分类=%d, 本文件重复=%d, 跨文件重复=%d, value=%s; %s",
                 gzip_txt, stats["rows_in"], stats["keys_out"], totals["dict_size"],
                 stats["del_rows"], stats["ins_rows"], stats["unclassified"],
                 stats["intra_file_dups"], overlap, stats["value_type"],
                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if stats.get("allele_type_mismatch"):
            log.warning("%s: allele_type 与序列形态不一致 %d 行",
                        gzip_txt, stats["allele_type_mismatch"])
        if stats.get("unclassified"):
            log.warning("%s: %d 行既非等长替换也非纯 del/ins(复杂 indel), 只写入原始 "
                        "key, 请确认上游是否已 left-normalize",
                        gzip_txt, stats["unclassified"])
        if stats.get("dup_examples"):
            log.info("重复 key 示例(前 %d 条): %s", args.list_dups,
                     stats["dup_examples"])

    log.info("序列化压缩中... 共 %d 个 key -> %s (gzip level=%d)",
             len(gnomad_nhomalt_dic), output, args.compress_level)
    dump_pickle(gnomad_nhomalt_dic, output, args.compress_level)
    log.info("字典构建完成: %s (%.1f MB)",
             output, output.stat().st_size / 1024 / 1024)
    log.info("统计汇总: %s", dict(totals))
    return 0


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
