#!/usr/bin/env bash
# =====================================================================
# build_submission.sh
# ---------------------------------------------------------------------
# Convenience helper. Produces lab13_submission.txt in the exact format
# the lab requires:
#
#   #Task N
#   <the code>
#   #Ciktilar
#   <the real program output>
#
# So you can copy the whole file into the school submission terminal.
# =====================================================================

set -e
OUT="lab13_submission.txt"
: > "$OUT"   # truncate

emit_task() {
  local num="$1" file="$2" runcmd="$3"
  {
    echo "#Task $num"
    echo
    cat "$file"
    echo
    echo "#Ciktilar"
    echo
    eval "$runcmd"
    echo
    echo "======================================================================"
    echo
  } >> "$OUT"
}

emit_task 1 task1.py "python3 task1.py"
emit_task 2 task2.py "python3 task2.py"
emit_task 3 task3.py "python3 task3.py"
emit_task 4 run_experiments.sh "bash run_experiments.sh"
emit_task 5 task5.py "python3 task5.py"

echo "Wrote $OUT ($(wc -l < "$OUT") lines)."
