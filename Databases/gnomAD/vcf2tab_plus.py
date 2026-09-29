#!/usr/bin/env python3
"""
将 .vcf.bgz 转换为 .txt.gz，支持多进程 + 多线程并行压缩。

输出为 gzip multi-member 格式，必须使用 gzip.open / zcat / gunzip -c 读取，
不能使用 gzip.decompress()（它只解压第一个成员）。

坐标采用 1-based inclusive（与 VCF POS/END 一致）：
  start = POS  (1-based)
  stop  = END  (1-based inclusive)
"""

from cyvcf2 import VCF
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from collections import deque
from functools import partial
import gzip
import logging
import multiprocessing as mp
import os
import stat as stat_mod
import sys
import time

# ---------- 日志 ----------

logger = logging.getLogger("vcf2txt")


def _setup_logging():
    """
    配置 root logger。幂等：重复调用不会添加重复 handler。
    spawn 模式下子进程会重新导入模块，convert_one 顶部也会调用一次。
    """
    root = logging.getLogger()
    if root.handlers:
        return
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stderr,
    )


# 表头：列名保持与原脚本一致（start/stop），坐标为 1-based inclusive
HEADER = (
    "chrom\tstart\tstop\tref\talt\tallele_type\tAF\tAF_eas\tnhomalt\n"
).encode("utf-8")

# ---------- 可调参数 ----------

LINES_PER_CHUNK   = 20000   # 每个 gzip 成员的文本行数（约几 MB）
COMPRESS_LEVEL    = 1       # 1 最快，压缩率略降；下游按行读无影响
VCF_THREADS       = 1       # 外层已多进程，这里给 1；单文件场景可调大

MAX_WORKERS       = 8       # 多文件时进程数上限，避免同时打开过多大 VCF 导致 OOM
SINGLE_FILE_MAX_THREADS = 8 # 单文件时压缩线程数上限

# 是否覆盖已存在的输出文件（可通过环境变量 OVERWRITE=1 强制覆盖）
OVERWRITE = os.environ.get("OVERWRITE", "").lower() in ("1", "true", "yes")

# gzip.compress 的 mtime 在 Python 3.11+ 是 keyword-only，
# 用 partial 固定 compresslevel 与 mtime，使 submit 只传 data。
_compress = partial(gzip.compress, compresslevel=COMPRESS_LEVEL, mtime=0)


# ---------- 工具 ----------

def GetAllFilePaths(pwd, wildcard="*.vcf.bgz"):
    """
    递归查找指定模式的文件，排除符号链接和空文件。

    用 lstat + stat.S_ISREG，单次 syscall 完成类型与大小判定：
    - lstat 不跟随符号链接，与“排除 symlink”语义一致；
    - S_ISREG 同时排除目录、FIFO、socket 等；
    - 避免 is_file()/is_symlink()/stat() 之间的 TOCTOU 竞态。
    """
    target = Path(pwd)
    result = []
    for p in target.rglob(wildcard):
        try:
            st = p.lstat()
        except OSError:
            continue
        if stat_mod.S_ISREG(st.st_mode) and st.st_size > 0:
            result.append(p)
    return result


def _is_valid_gz(path):
    """
    快速验证文件是否能作为 gzip 打开并读到至少 1 字节。
    避免静默跳过被截断/损坏的历史输出文件。
    """
    try:
        with gzip.open(path, "rb") as f:
            return bool(f.read(1))
    except (OSError, EOFError):
        return False


# ---------- 单文件转换 ----------

def _iter_text_chunks(vcf_path, chunk_lines):
    """生成器：流式产出 UTF-8 bytes 文本块。"""
    vcf = VCF(vcf_path, threads=VCF_THREADS)
    try:
        buf = []
        append = buf.append
        n = 0

        for v in vcf:
            alt = v.ALT
            if len(alt) == 1:
                alt = alt[0]
            else:
                alt = ",".join(alt)

            info = v.INFO
            append(
                f"{v.CHROM}\t{v.start + 1}\t{v.end}\t{v.REF}\t{alt}\t"
                f"{info.get('allele_type')}\t"
                f"{info.get('AF')}\t"
                f"{info.get('AF_eas')}\t"
                f"{info.get('nhomalt')}\n"
            )
            n += 1
            if n >= chunk_lines:
                yield "".join(buf).encode("utf-8")
                buf.clear()
                n = 0

        if buf:
            yield "".join(buf).encode("utf-8")
    finally:
        vcf.close()


def _write_gz_parallel(fout, chunks, workers, max_pending):
    """
    并行压缩 + 顺序写出。
    利用 gzip multi-member 特性：每个 chunk 独立压缩成一个 gzip 成员，
    按序追加后仍是合法的 gz 文件。

    注意：下游读取时必须使用 gzip.open / zcat / gunzip -c，
    不能使用 gzip.decompress()（它只解压第一个成员）。
    """
    ex = ThreadPoolExecutor(max_workers=workers)
    pending = deque()
    try:
        for chunk in chunks:
            pending.append(ex.submit(_compress, chunk))
            if len(pending) >= max_pending:
                fout.write(pending.popleft().result())
        while pending:
            fout.write(pending.popleft().result())
    finally:
        # 取消尚未开始的任务；已启动的任务无法中断，shutdown(wait=True)
        # 会等它们结束。被成功取消的 future 其结果不会写出——异常路径下
        # 整个输出文件将被丢弃，这是期望行为。
        for fut in pending:
            fut.cancel()
        ex.shutdown(wait=True)


def convert_one(vcf_path_str, workers=4, overwrite=OVERWRITE):
    """
    把一个 .vcf.bgz 转成 .txt.gz；返回状态字符串。

    该函数会被 ProcessPoolExecutor 通过 pickle 分发到子进程执行，
    因此必须是模块级函数，且只接受可 pickle 的参数。
    """
    # spawn 模式下子进程不会执行 main()，这里幂等补一次日志配置
    _setup_logging()

    vcf_path = Path(vcf_path_str)
    out_path = vcf_path.with_suffix("").with_suffix(".txt.gz")

    if out_path.exists() and not overwrite:
        if _is_valid_gz(out_path):
            return f"[skip] {out_path}"
        logger.warning("输出文件损坏，将重新生成: %s", out_path)

    # 根据 workers 调整 max_pending，避免内存过高
    max_pending = max(2, workers * 2)

    # 先写入临时文件，成功后原子替换，避免异常时留下不完整的最终文件
    tmp_path = out_path.with_name(out_path.name + ".tmp")

    t0 = time.time()
    try:
        with open(tmp_path, "wb") as fout:
            # 表头同样作为一个独立 gzip 成员写入
            fout.write(_compress(HEADER))
            _write_gz_parallel(
                fout,
                _iter_text_chunks(str(vcf_path), LINES_PER_CHUNK),
                workers=workers,
                max_pending=max_pending,
            )
        os.replace(tmp_path, out_path)
    except Exception:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
        raise

    dt = time.time() - t0
    return f"[ok]   {out_path}  ({dt:.1f}s)"


# ---------- 并发规划 ----------

def _plan_parallelism(n_files, cpu):
    """
    规划进程数与每进程线程数。

    - 单文件：线程数 = min(cpu, SINGLE_FILE_MAX_THREADS)。
    - 多文件：进程数 = min(n_files, cpu, MAX_WORKERS)，避免同时打开过多
      大 VCF 引起 I/O 争抢与内存峰值；线程数按剩余核数分配，至少 1。
    """
    if n_files <= 1:
        return 1, min(cpu, SINGLE_FILE_MAX_THREADS)
    n_workers = min(n_files, cpu, MAX_WORKERS)
    per_proc_threads = max(1, cpu // n_workers)
    # 单进程内线程数不必超过 MAX_WORKERS
    per_proc_threads = min(per_proc_threads, MAX_WORKERS)
    return n_workers, per_proc_threads


# ---------- 主流程 ----------

def main():
    _setup_logging()

    current_dir = Path.cwd()
    raw_files = GetAllFilePaths(current_dir, "*.vcf.bgz")

    if not raw_files:
        logger.error("no *.vcf.bgz found in %s", current_dir)
        return

    # 按文件大小升序：小文件先完成，能及早看到进度
    raw_files.sort(key=lambda p: p.stat().st_size)
    vcf_files = [str(p) for p in raw_files]

    logger.info("matched %d files under %s", len(vcf_files), current_dir)

    cpu = os.cpu_count() or 4
    n_workers, per_proc_threads = _plan_parallelism(len(vcf_files), cpu)

    # ---- 单文件：直接在本进程内多线程压缩 ----
    if len(vcf_files) == 1:
        try:
            logger.info(convert_one(vcf_files[0], workers=per_proc_threads))
        except Exception:
            logger.exception("failed: %s", vcf_files[0])
        return

    # ---- 多文件：多进程 + 每进程多线程 ----
    logger.info(
        "files=%d  procs=%d  threads/proc=%d  cpu=%d",
        len(vcf_files), n_workers, per_proc_threads, cpu,
    )

    # 显式使用 spawn：避免 fork 继承 cyvcf2/htslib 的线程状态导致子进程卡死
    ctx = mp.get_context("spawn")

    t_start = time.time()
    total = len(vcf_files)
    ok = skip = fail = 0

    with ProcessPoolExecutor(max_workers=n_workers, mp_context=ctx) as ex:
        futures = {
            ex.submit(convert_one, f, per_proc_threads): f
            for f in vcf_files
        }
        for done, fut in enumerate(as_completed(futures), start=1):
            src = futures[fut]
            elapsed = time.time() - t_start
            try:
                msg = fut.result()
                if msg.startswith("[skip]"):
                    skip += 1
                else:
                    ok += 1
                logger.info("[%d/%d  %6.1fs] %s",
                            done, total, elapsed, msg)
            except Exception:
                fail += 1
                logger.exception("[%d/%d  %6.1fs] worker failed: %s",
                                 done, total, elapsed, src)

    wall = time.time() - t_start
    logger.info(
        "DONE  ok=%d  skip=%d  fail=%d  total=%d  wall=%.1fs",
        ok, skip, fail, total, wall,
    )


if __name__ == "__main__":
    main()