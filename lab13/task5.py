#!/usr/bin/env python3
# =====================================================================
# Task 5: When is compression beneficial, and when is it not?
# ---------------------------------------------------------------------
# This task asks for a reflective comment. To back the reflection with
# evidence, the script below measures two extreme page types and prints
# whether compressing each one actually pays off.
# =====================================================================

import os
import string
import time
import zlib


def evaluate(name, data):
    start = time.perf_counter()
    comp = zlib.compress(data)
    elapsed = time.perf_counter() - start
    ratio = len(comp) / len(data)
    verdict = "BENEFICIAL" if ratio < 0.9 else "NOT worth it"
    print("{:<22} ratio={:.3f}  time={:.5f}s  -> {}".format(name, ratio, elapsed, verdict))


def main():
    size = 4096
    print("=" * 64)
    print("Task 5: When does compression help?")
    print("=" * 64)

    # 1) Highly repetitive page -> compresses extremely well.
    repetitive = (("the_same_block_" * 8)[:64] * (size // 64 + 1))[:size].encode()
    evaluate("Repetitive page", repetitive)

    # 2) Natural-text-like page -> compresses moderately.
    textish = (string.ascii_lowercase * (size // 26 + 1))[:size].encode()
    evaluate("Text-like page", textish)

    # 3) Already-compressed / encrypted / random page -> does NOT shrink.
    incompressible = os.urandom(size)
    evaluate("Random/binary page", incompressible)

    print("=" * 64)


if __name__ == "__main__":
    main()

# =====================================================================
# REFLECTION (Task 5): when is compression beneficial vs not?
# ---------------------------------------------------------------------
# Compression is BENEFICIAL when:
#   - Pages contain redundant / structured data (text, code, zero-filled
#     or repetitive buffers). They shrink a lot, so RAM holds more pages,
#     eviction and disk swapping are delayed or avoided (see Task 3).
#   - The system is under memory pressure but has spare CPU cycles. This
#     is the typical case on mobile devices: limited RAM, capable CPU.
#     Trading CPU for memory is a clear win -> Linux zram/zswap, iOS/macOS
#     compressor all rely on this.
#   - A fast algorithm (zlib/LZ4/LZO class) is used, keeping the CPU cost
#     of (de)compression small compared to the cost of a disk swap.
#
# Compression is NOT beneficial when:
#   - Pages are already compressed, encrypted, or random (the os.urandom
#     case above): the ratio stays ~1.0, so we burn CPU for no memory gain
#     and may even grow the data. The Task 2 threshold rule (skip if
#     ratio > 0.9) exists exactly to avoid this.
#   - The CPU is the bottleneck and RAM is plentiful: spending cycles on
#     compression then slows the workload with no benefit.
#   - A heavy algorithm (lzma/bz2) is used for live memory: the extra CPU
#     latency can cost more than the disk I/O it was meant to save.
#
# Bottom line:
#   Compression is a CPU-for-memory trade. It wins when data is
#   compressible, RAM is scarce, and CPU is relatively cheap; it loses
#   when data is incompressible or CPU is the scarce resource. A good
#   policy compresses selectively (threshold + fast algorithm) rather
#   than unconditionally.
# =====================================================================
