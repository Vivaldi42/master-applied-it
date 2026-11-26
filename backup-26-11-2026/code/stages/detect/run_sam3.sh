#!/usr/bin/env bash
# Stage 4 (detect): run SAM 3 for every prompt in a ground-truth file.
# Each prompt runs in its own process, so GPU memory is fully released in between.
#
# One prompt runs per GPU at a time.
#
# Usage:  [GPUS="0 1"] code/stages/detect/run_sam3.sh <frames-dir> <ground-truth.csv> <run-dir>
# Output: <run-dir>/<prompt>/ per prompt (see sam3_detect.py), <run-dir>/<prompt>.log
set -uo pipefail

FRAMES_DIR="$1"
GT="$2"
RUN_DIR="$3"
SCRIPT="$(dirname "$0")/sam3_detect.py"
GPUS="${GPUS:-0 1}"  # GPUs to use, for example GPUS=1

mkdir -p "$RUN_DIR"
export PYTORCH_ALLOC_CONF=expandable_segments:True
export FRAMES_DIR RUN_DIR SCRIPT GPUS

detect_one() {
  local prompt="$1" log="$RUN_DIR/${1// /_}.log"
  local gpus=($GPUS)
  export CUDA_VISIBLE_DEVICES="${gpus[$SLOT]}"
  echo "=== $prompt (GPU $CUDA_VISIBLE_DEVICES)"
  # A failed prompt does not stop the remaining prompts
  python "$SCRIPT" "$FRAMES_DIR" "$prompt" "$RUN_DIR" > "$log" 2>&1 \
    && grep -a "^=== " "$log" \
    || echo "FAILED: $prompt (see $log)"
}
export -f detect_one

# Skip the header, take the first column (prompt). xargs runs one prompt per GPU
# at a time and gives each running process a slot number (0, 1, ...).
gpu_list=($GPUS)
tail -n +2 "$GT" | cut -d, -f1 | grep -v '^$' | tr '\n' '\0' \
  | xargs -0 -n 1 -P "${#gpu_list[@]}" --process-slot-var=SLOT \
    bash -c 'detect_one "$1"' _
