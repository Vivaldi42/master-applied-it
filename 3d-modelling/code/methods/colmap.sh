#!/usr/bin/env bash
# Paused method: COLMAP sparse and dense reconstruction.
#
# Usage:  code/methods/colmap.sh <run-dir>
# Input:  <run-dir>/frames/*.jpg
# Output: <run-dir>/database.db, sparse/, dense/ (dense/fused.ply), *.log
set -euo pipefail

RUN_DIR="$(realpath "$1")"
IMAGE="colmap/colmap:latest"
GPU=0

# A run never overwrites an earlier run
if [ -e "$RUN_DIR/database.db" ]; then
  echo "Error: $RUN_DIR/database.db exists. Use a new run folder." >&2
  exit 1
fi

# Record the exact image version for repeatability
docker image inspect "$IMAGE" --format '{{index .RepoDigests 0}}' > "$RUN_DIR/colmap-image.txt"

# Run one COLMAP command in Docker. The run folder is visible as /work.
colmap() {
  docker run --rm --gpus "device=$GPU" -u "$(id -u):$(id -g)" \
    -v "$RUN_DIR":/work "$IMAGE" colmap "$@"
}

# 1. Feature extraction: SIFT keypoints and descriptors per frame
colmap feature_extractor \
  --database_path /work/database.db \
  --image_path /work/frames \
  --ImageReader.single_camera 1 \
  2>&1 | tee "$RUN_DIR/feature_extraction.log"

# 2. Matching: all image pairs, then geometric verification
colmap exhaustive_matcher \
  --database_path /work/database.db \
  2>&1 | tee "$RUN_DIR/matching.log"

# 3. Mapping: camera poses and sparse 3D points (incremental)
mkdir -p "$RUN_DIR/sparse"
colmap mapper \
  --database_path /work/database.db \
  --image_path /work/frames \
  --output_path /work/sparse \
  2>&1 | tee "$RUN_DIR/mapping.log"

# 4. Undistortion: input for dense reconstruction.
# Assumes sparse/0 is the main model. Check this with model_analyzer.
colmap image_undistorter \
  --image_path /work/frames \
  --input_path /work/sparse/0 \
  --output_path /work/dense \
  --max_image_size 2000 \
  2>&1 | tee "$RUN_DIR/undistortion.log"

# 5. PatchMatch stereo: depth map per frame (slowest step)
colmap patch_match_stereo \
  --workspace_path /work/dense \
  --PatchMatchStereo.geom_consistency true \
  2>&1 | tee "$RUN_DIR/patch_match.log"

# 6. Fusion: depth maps to one dense point cloud
colmap stereo_fusion \
  --workspace_path /work/dense \
  --input_type geometric \
  --output_path /work/dense/fused.ply \
  2>&1 | tee "$RUN_DIR/fusion.log"
