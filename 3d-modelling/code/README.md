# Code

Design: `architecture/pipeline-design.md`. Method 1: `architecture/method-1-sam3.md`.

## Layout

| Path | Content |
|---|---|
| `run_pipeline.py` | Evaluation pipeline: frames, method, evaluation |
| `methods/sam3_video.py` | Method 1: SAM 3 detection and tracking |
| `methods/colmap.sh`, `colmap.md` | Paused method: 3D reconstruction with COLMAP |

## Run

Each room folder contains `video.mp4`, `asset-types.csv` and `ground-truth.csv`.

```
conda activate sam3
cd /mnt/ssd/vladi/master-applied-it/3d-modelling
python code/run_pipeline.py sam3 room002
```

The run folder `runs/exp<NNN>-<room>-<method>/` receives the next free number. It contains `inputs/` (copies of the asset types and the ground truth), `counts.csv`, `evaluation.csv`, `timing.csv` (time per step) and `run.log`. To test other asset types, add `--assets <file>`.

## Add a method

1. Write a program that is called as `<program> <frames-dir> <asset-types.csv> <run-dir>` and writes `<run-dir>/counts.csv` with the columns `asset,count`.
2. Add its command to `METHODS` in `run_pipeline.py`.
