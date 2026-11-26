# COLMAP reconstruction (stage 2)

This document describes the COLMAP reconstruction stage, the settings used in run `exp001-room001-colmap-sam3` and the results of that run. The commands are in `colmap.sh` in this folder.

## 1. Purpose

The stage computes the position and orientation (pose) of the camera for each video frame and a 3D point cloud of the room. Later stages use the poses to project 2D detection masks into 3D and use the point cloud to compute asset positions.

COLMAP is an external tool. The repository contains only the commands and settings that call it. The tool runs in Docker so that its dependencies stay separate from other methods.

## 2. Environment

| Item | Value |
|---|---|
| COLMAP version | 4.3.0.dev0 with CUDA |
| Docker image | `colmap/colmap@sha256:b8498ebecab11c3f9b9a25370e3fcfb6de9b6bcd4f3c85d5dc39a40229f40954` |
| GPU | NVIDIA RTX 4090 (GPU 0). GPU 1 was in use by other users. |

## 3. Input

| Item | Value |
|---|---|
| Room | `room001`, two computer monitors as target assets |
| Device | Samsung Galaxy S25, video stabilisation off |
| Video | 172.5 s, 3840 x 2160, 30 fps, HEVC, 716 MB, no rotation flag |
| Camera motion | Slow walk along the walls with a closing loop, close passes of each monitor |

## 4. Procedure

### 4.1 Frame extraction (FFmpeg)

```
ffmpeg -i data/room001/video.mp4 -vf fps=2 -q:v 2 runs/<run>/frames/frame_%06d.jpg
```

- 2 frames per second gives 345 frames. At slow walking speed, consecutive frames are approximately 25 cm apart. This distance gives enough baseline for depth estimation and enough overlap for matching.
- All 5173 frames were not used. Consecutive frames at 30 fps are almost identical, which adds computation without new information. The number of image pairs for exhaustive matching grows with the square of the number of frames.
- JPEG quality 2 is the highest quality setting of FFmpeg. Full resolution was kept.
- No blur filter was applied. The number of registered frames after mapping was used to decide whether blur is a problem.

### 4.2 Feature extraction

COLMAP detects keypoints (distinctive image locations such as corners and texture) with SIFT and computes a 128-value descriptor for each keypoint. The results are stored in `database.db`.

- `--ImageReader.single_camera 1`: all frames share one set of camera parameters (focal length and lens distortion) because one camera with fixed zoom was used.
- Other settings use the defaults: camera model `SIMPLE_RADIAL`, at most 8192 features per image.
- The frames with the fewest keypoints showed blank walls or motion blur.

### 4.3 Feature matching

COLMAP compares descriptors between images and keeps image pairs whose matches agree with one camera motion (geometric verification).

- The exhaustive matcher compares all image pairs. It was selected over the sequential matcher because it also detects the overlap between the end and the start of the closing loop without an extra vocabulary tree file.

### 4.4 Mapping (sparse reconstruction)

The incremental mapper starts from the image pair with the strongest matches, adds one frame at a time, triangulates new 3D points and refines all poses and points with bundle adjustment.

- The incremental mapper was selected as the reference method. The global mapper (GLOMAP) is planned as a separate run for comparison.

### 4.5 Undistortion

The frames are corrected for the estimated lens distortion and resized to the input format of dense reconstruction.

- `--max_image_size 2000`: frames are reduced from 3840 x 2160 to 2000 x 1125 pixels to limit processing time and GPU memory.
- Only the main model `sparse/0` is used.

### 4.6 PatchMatch stereo

For every pixel of every frame, PatchMatch estimates a depth value by comparing image patches with neighbouring frames. This step took more than 154 min.

- `--PatchMatchStereo.geom_consistency true`: a second pass keeps only depth values that agree between neighbouring frames.

### 4.7 Fusion

The depth maps are combined into one point cloud. A point is kept only if several frames agree on its position.

- `--input_type geometric`: uses the filtered depth maps from the second pass.

## 5. Results of exp001

### 5.1 Processing time

| Step | Time (min) |
|---|---|
| Feature extraction | 0.24 |
| Matching | 4.58 |
| Mapping | 7.20 |
| Undistortion | 0.04 |
| PatchMatch stereo | 154.52 |
| Fusion | 1.60 |
| Total | 168.17 |

PatchMatch stereo takes 92 % of the total time. Peak GPU memory was not recorded.

### 5.2 Matching and mapping

| Measure | Value |
|---|---|
| Image pairs compared | 59,340 |
| Verified image pairs | 4,958 (8 %) |
| Models produced | 2 |
| Model 0: registered frames | 326 of 345 |
| Model 0: 3D points | 60,726 |
| Model 0: mean reprojection error | 1.28 px |
| Model 0: mean track length | 3.90 frames per point |
| Model 1: registered frames | 10 (frames 84 and 102 to 110) |
| Model 1: 3D points | 968 |
| Frames in neither model | 101, 111, 124 to 130, 242 |

Model 1 has its own coordinate system and scale. It cannot be combined with model 0 without additional processing, so its frames are lost for this run. The unregistered frames lie at approximately 50 to 55 s and 62 to 65 s of the video. Their cause has not been checked.

### 5.3 Dense reconstruction

| Measure | Value |
|---|---|
| Undistorted frames | 326, 2000 x 1125 px |
| Depth maps | 652 (photometric and geometric per frame) |
| Fused points | 1,994,709 |
| Size of `dense/` | 23 GB (normal maps 17 GB, depth maps 5.5 GB) |
| Size of `fused.ply` | 51 MB |

### 5.4 Visual inspection

- The sparse model resembles the shape of the room, but most objects cannot be identified.
- The dense model is upside down. COLMAP does not know the direction of gravity and uses a camera convention in which the y-axis points down.
- Walls and desks contain holes. Smooth surfaces without texture give no reliable patch matches.
- The two monitors can be identified only with prior knowledge of the room.

## 6. Assessment

The model is accepted as the baseline for the first experiment. Visual quality is not the criterion. The criterion is whether the localisation stage can compute monitor positions with an error of a few centimetres. This error can be measured only after the scale, detection and localisation stages are complete.

## 7. Open issues

1. The cause of the 19 frames outside model 0 is unknown. Inspect frames 101 to 111 and 124 to 130.
2. `colmap.sh` assumes that `sparse/0` is the main model. COLMAP does not guarantee this order.
3. Peak GPU memory per step (criterion C5) was not measured.
4. The `dense/` folder uses 23 GB per run. A cleanup rule for intermediate outputs is needed.
5. The model has no real-world scale and no defined up direction. Both are handled in the scale stage.
6. Section 5.1 of the background research document names COLMAP with GLOMAP as rank 1. Section 5.2 names COLMAP only. The two sections should be made consistent.

## 8. Possible improvements for later runs

Each change is a separate run that is compared with exp001.

- Global mapper (GLOMAP) instead of the incremental mapper: processing time and accuracy.
- Higher frame rate or a sharpness-based frame selection: number of registered frames.
- Larger `max_image_size`: completeness of the dense model.
