#!/usr/bin/env bash
# =====================================================================
# Task 4: Bash Script Automation (Optional)
# ---------------------------------------------------------------------
# Runs memory_compression_sim.py with different parameters (page sizes,
# number of pages, algorithms) and stores every run's output into a
# separate log file under ./logs/.
#
# Usage:
#   bash run_experiments.sh
# =====================================================================

set -e

SCRIPT="memory_compression_sim.py"
LOG_DIR="logs"
mkdir -p "$LOG_DIR"

# Parameter grids to sweep.
PAGE_COUNTS=(100 200 500)
PAGE_SIZES=(1024 4096 8192)
ALGOS=(zlib bz2 lzma)

echo "Starting memory-compression experiments..."
echo "Logs will be written to ./$LOG_DIR/"
echo

for algo in "${ALGOS[@]}"; do
  for pages in "${PAGE_COUNTS[@]}"; do
    for size in "${PAGE_SIZES[@]}"; do
      logfile="$LOG_DIR/run_${algo}_p${pages}_s${size}.log"
      echo "-> algo=$algo pages=$pages page_size=$size  =>  $logfile"
      python3 "$SCRIPT" --pages "$pages" --page-size "$size" --algo "$algo" > "$logfile" 2>&1
    done
  done
done

echo
echo "All experiments finished. Summary of average compression ratios:"
echo "----------------------------------------------------------------"
# Pull the ratio line from each log so we get a quick overview.
for logfile in "$LOG_DIR"/*.log; do
  ratio=$(grep "Average compression ratio" "$logfile" | awk '{print $NF}')
  printf "%-40s ratio=%s\n" "$(basename "$logfile")" "$ratio"
done
echo "----------------------------------------------------------------"
echo "Done. ($(ls "$LOG_DIR"/*.log | wc -l) log files written.)"
