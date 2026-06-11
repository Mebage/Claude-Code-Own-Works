# Operating Systems — Laboratory Exercises 13

Virtual Memory and Memory Compression. All scripts use **only the Python 3
standard library** (no external packages) and run on a clean Ubuntu install.

## Files

| File | Task | What it does |
|------|------|--------------|
| `task1.py` | 1 | Compression algorithm comparison (zlib / bz2 / lzma): avg ratio + time. |
| `task2.py` | 2 | Compression threshold: skip pages with ratio > 0.9, count skipped, memory saved. |
| `task3.py` | 3 | Memory pressure: 512 MB capacity tracking, LRU eviction, compression vs no-compression. |
| `memory_compression_sim.py` | 4 | Parametrizable simulator (`--pages`, `--page-size`, `--algo`). |
| `run_experiments.sh` | 4 | Bash automation: sweeps parameters, writes per-run logs to `logs/`. |
| `task5.py` | 5 | When compression is beneficial vs not (demo + reflection comment). |
| `OBSERVATIONS.md` | 6 | Short summary of observations and conclusions. |
| `build_submission.sh` | — | Helper: produces `lab13_submission.txt` (`#Task N / code / #Ciktilar / output`). |

## How to run

```bash
python3 task1.py
python3 task2.py
python3 task3.py
python3 memory_compression_sim.py --pages 200 --page-size 4096 --algo zlib
bash run_experiments.sh        # writes logs/*.log
python3 task5.py

# Build the ready-to-submit text file:
bash build_submission.sh       # -> lab13_submission.txt
```
