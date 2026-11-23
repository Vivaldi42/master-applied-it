#!/usr/bin/env bash
# Stage 4 (detect): run SAM 3 for every prompt in a ground-truth file.
# Each prompt runs in its own process, so GPU memory is fully released in between.
#
# Usage:  code/stages/detect/run_sam3.sh <frames-dir> <ground-truth.csv> <run-dir>
# Output: <run-dir>/<prompt>/ per prompt (see sam3_detect.py), <run-dir>/<prompt>.log
set -uo pipefail

FRAMES_DIR="$1"
GT="$2"
RUN_DIR="$3"
SCRIPT="$(dirname "$0")/sam3_detect.py"

mkdir -p "$RUN_DIR"
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_ALLOC_CONF=expandable_segments:True

# Skip the header, take the first column (prompt)
tail -n +2 "$GT" | cut -d, -f1 | while IFS= read -r prompt; do
  [ -z "$prompt" ] && continue
  log="$RUN_DIR/${prompt// /_}.log"
  echo "=== $prompt"
  # A failed prompt does not stop the remaining prompts
  python "$SCRIPT" "$FRAMES_DIR" "$prompt" "$RUN_DIR" > "$log" 2>&1 \
    && grep -a "^=== " "$log" \
    || echo "FAILED: $prompt (see $log)"
done
