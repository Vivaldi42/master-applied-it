# Asset reconstruction pipeline

Experiment code for SQ3 and SQ4 of the background research document. The pipeline converts a video of a room into a 3D model and a list of detected assets with 3D positions.

## Folder layout

| Path | Content | In git |
|---|---|---|
| `code/` | Pipeline and evaluation code | Yes |
| `data/<room>/video.mp4` | Input video | No |
| `data/<room>/ground-truth.csv` | Hand count and tape measurements | Yes |
| `runs/<run-id>/` | All outputs of one pipeline run | No |

A run never overwrites an earlier run. Each run folder stores its settings, stage outputs, logs and metrics.

## Pipeline stages

Each stage runs as a separate process in its own environment. Stages exchange data only through files in the run folder.

| Stage | Input | Output | Method (experiment 1) | Environment |
|---|---|---|---|---|
| 1. Frames | `video.mp4` | `frames/*.jpg` | FFmpeg | System |
| 2. Reconstruct | `frames/` | `sparse/`, `dense/` (COLMAP format) | COLMAP | Docker `colmap/colmap` |
| 3. Scale | Model, one measured distance | Model in metres | Own script | TBD |
| 4. Detect | `frames/` | `masks/` (PNG per frame) | SAM 3 | TBD |
| 5. Localise | Model, `masks/` | `assets.csv` (position, count) | Own script | TBD |
| 6. Evaluate | `assets.csv`, `ground-truth.csv` | `metrics.json` | Own script | TBD |

## Run naming

Format: `exp<NNN>-<room>-<reconstruction method>-<detection method>`

Example: `exp001-room001-colmap-sam3`

Rules:
1. `<NNN>` is a three-digit counter that increases by one for every new run, also when a run repeats earlier settings. The counter alone identifies a run.
2. The other parts describe the input and methods. They do not identify the run.
3. Method names use lowercase letters and digits only, for example `colmap`, `mapanything`, `sam3`, `gdinosam2`.
4. A failed or aborted run keeps its number. The number is not reused.

## How to run

TBD
