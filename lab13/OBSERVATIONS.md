# Lab 13 — Memory Compression: Observations & Conclusions (Task 6)

This lab simulated virtual-memory compression in Python (standard library
only) and explored five experiments. Summary of what each task showed:

**Task 1 — Algorithm comparison (zlib / bz2 / lzma).**
On the mixed test data, `zlib` gave both the best average ratio (~0.47) and
by far the fastest time (~0.02 s), while `lzma` was ~15x slower for no ratio
gain. There is a clear speed-vs-ratio trade-off: fast algorithms (zlib/LZ4/
LZO class) suit live, real-time memory compression; heavy algorithms (lzma)
suit offline/archival use.

**Task 2 — Compression threshold (skip if ratio > 0.9).**
With incompressible pages added to the mix, 61 of 200 pages were skipped.
Memory savings stayed the same as "compress everything" (~46%), because the
skipped pages would not have shrunk anyway — so the rule saves CPU at no cost
to memory. Real systems (zswap) reject incompressible pages the same way.

**Task 3 — Memory pressure & eviction.**
At a 512 KB budget, without compression only 128 pages fit and 416 LRU
evictions occurred; with compression 343 pages stayed resident and evictions
dropped to 0. The 512 MB projection showed ~3.97x more pages fit in the same
RAM. Compression increases effective capacity, so it delays — and here fully
avoids — page eviction and the slow disk swapping it would cause.

**Task 4 — Bash automation.**
`run_experiments.sh` swept algorithm × page-count × page-size (27 runs) and
stored each result in `logs/`. Larger pages compressed slightly better
(more redundancy per page); zlib stayed competitive across the board.

**Task 5 — When compression helps vs not.**
Repetitive/text pages compressed to ~1.5% of their size (huge win); random/
binary pages grew slightly (ratio 1.003 — a loss). Compression is a
CPU-for-memory trade: it wins when data is compressible, RAM is scarce, and
CPU is relatively cheap (the mobile case); it loses on already-compressed or
encrypted data, or when CPU is the bottleneck.

**Overall conclusion.**
Memory compression is an effective middle layer between pure RAM access and
disk swapping. Applied *selectively* — a fast algorithm plus a skip
threshold — it raises effective memory capacity and reduces costly evictions,
which is exactly why modern OSes (Linux zram/zswap, iOS/macOS compressor)
use it under memory pressure on RAM-constrained devices.
