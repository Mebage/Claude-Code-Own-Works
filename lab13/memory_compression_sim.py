#!/usr/bin/env python3
# =====================================================================
# memory_compression_sim.py
# ---------------------------------------------------------------------
# Parametrizable memory-compression simulator. This is the extended
# version of the base simulation from the lab handout: it accepts
# command-line parameters so it can be driven by the Bash automation
# script (Task 4) with different page sizes and page counts.
#
# Usage:
#   python3 memory_compression_sim.py --pages 200 --page-size 4096 --algo zlib
# =====================================================================

import argparse
import random
import string
import time
import zlib
import bz2
import lzma

ALGORITHMS = {
    "zlib": (zlib.compress, zlib.decompress),
    "bz2":  (bz2.compress,  bz2.decompress),
    "lzma": (lzma.compress, lzma.decompress),
}


class MemoryPage:
    def __init__(self, content: str):
        self.original = content.encode("utf-8")
        self.compressed = None

    def compress(self, algo):
        compress_fn, _ = ALGORITHMS[algo]
        self.compressed = compress_fn(self.original)

    def decompressed_size(self, algo):
        _, decompress_fn = ALGORITHMS[algo]
        return len(decompress_fn(self.compressed)) if self.compressed else len(self.original)

    def compression_ratio(self):
        if not self.compressed:
            return 1.0
        return len(self.compressed) / len(self.original)


class MemorySimulator:
    def __init__(self, num_pages=100, page_size=4096, seed=42):
        random.seed(seed)
        self.page_size = page_size
        self.pages = [self._generate_page(page_size) for _ in range(num_pages)]

    def _generate_page(self, size):
        if random.random() < 0.5:
            data = "".join(random.choices(string.ascii_lowercase, k=50)) * (size // 50)
        else:
            data = "".join(random.choices(string.printable, k=size))
        return MemoryPage(data)

    def compress_pages(self, algo):
        for page in self.pages:
            page.compress(algo)

    def report_stats(self, algo, elapsed):
        total_original = sum(len(p.original) for p in self.pages)
        total_compressed = sum(len(p.compressed) for p in self.pages if p.compressed)
        avg_ratio = sum(p.compression_ratio() for p in self.pages) / len(self.pages)

        print("Algorithm                : {}".format(algo))
        print("Pages / page size        : {} / {} bytes".format(len(self.pages), self.page_size))
        print("Original memory usage    : {} KB".format(total_original // 1024))
        print("Compressed memory usage  : {} KB".format(total_compressed // 1024))
        print("Average compression ratio: {:.2f}".format(avg_ratio))
        print("Compression time         : {:.4f} s".format(elapsed))


def main():
    parser = argparse.ArgumentParser(description="Memory compression simulator")
    parser.add_argument("--pages", type=int, default=200, help="number of memory pages")
    parser.add_argument("--page-size", type=int, default=4096, help="bytes per page")
    parser.add_argument("--algo", choices=ALGORITHMS.keys(), default="zlib",
                        help="compression algorithm")
    args = parser.parse_args()

    print("=" * 60)
    print("Memory Compression Simulation")
    print("=" * 60)
    sim = MemorySimulator(num_pages=args.pages, page_size=args.page_size)
    start = time.perf_counter()
    sim.compress_pages(args.algo)
    elapsed = time.perf_counter() - start
    sim.report_stats(args.algo, elapsed)
    print("=" * 60)


if __name__ == "__main__":
    main()
