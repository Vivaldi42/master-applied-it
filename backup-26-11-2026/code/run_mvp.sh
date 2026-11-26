#!/usr/bin/env bash
# MVP pipeline: room video and asset list in, asset counts and count errors out.
#
# Usage:  code/run_mvp.sh <video> <asset-list.csv> <ground-truth.csv> <run-dir>
#         Run inside the conda env "sam3".
# Output: <run-dir>/frames/, detect/, counts.csv, review/, evaluation.csv
set -euo pipefail

VIDEO="$1"
ASSETS="$2"
TRUTH="$3"
RUN_DIR="$4"
STAGES="$(dirname "$0")/stages"

# A run never overwrites an earlier run
mkdir "$RUN_DIR"

echo "=== 1. Frames"
mkdir "$RUN_DIR/frames"
ffmpeg -loglevel error -i "$VIDEO" -vf "fps=10,scale=1920:-2" -q:v 2 \
  -start_number 0 "$RUN_DIR/frames/%05d.jpg"

echo "=== 4. Detect"
"$STAGES/detect/run_sam3.sh" "$RUN_DIR/frames" "$ASSETS" "$RUN_DIR/detect"

echo "=== Count"
python "$STAGES/count/count.py" "$RUN_DIR/detect" "$ASSETS" "$RUN_DIR/counts.csv"

echo "=== Review"
python "$STAGES/review/review.py" "$RUN_DIR/frames" "$RUN_DIR/detect" "$ASSETS" "$RUN_DIR/review"

echo "=== 6. Evaluate"
python "$STAGES/evaluate/evaluate.py" "$RUN_DIR/counts.csv" "$TRUTH" "$RUN_DIR/evaluation.csv"
cat "$RUN_DIR/evaluation.csv"
