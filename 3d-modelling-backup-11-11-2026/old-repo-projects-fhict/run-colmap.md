# Run COLMAP over SSH: video to 3D model

Run the numbered steps in order. Commands run on the **remote Ubuntu PC** unless explicitly marked **local computer**. No monitor is required on the remote PC.

The PC already has Docker, the COLMAP image and tmux. The first experiment failed during GPU matching; this guide limits matching memory and uses medium reconstruction quality. It does not stop other GPU workloads.

## 1. Connect and create a new experiment

On your **local computer**, connect using your usual SSH address (replace `PC_ADDRESS`):

```bash
ssh vladi@PC_ADDRESS
```

On the **remote PC**, start or rejoin tmux:

```bash
tmux new-session -A -s colmap
```

tmux keeps jobs running if SSH disconnects. If a previous job is still running in this session, let it finish first.

Choose a new folder name for each video or changed frame extraction. Run the following **inside tmux**; replace `my-room-2` as needed:

```bash
export COLMAP_RUN="/home/vladi/Desktop/colmap-experiments/my-room-2"
mkdir -p "$COLMAP_RUN/images"
```

Keep this terminal open. Later commands use `COLMAP_RUN`. In a new shell, set it again to the same folder.

## 2. Upload the video

In a separate terminal on your **local computer**:

```bash
scp "/path/to/your/video.mp4" \
  vladi@PC_ADDRESS:/home/vladi/Desktop/colmap-experiments/my-room-2/video.mp4
```

Replace the local video path, SSH address and experiment name. The destination must match step 1. You can also upload with an SFTP client.

## 3. Check tools and GPU access

Back inside **remote tmux**:

```bash
ffmpeg -version
docker run --rm --gpus 'device=0' colmap/colmap:latest nvidia-smi
df -h "$COLMAP_RUN"
```

If FFmpeg is missing:

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

The Docker check should show GPU 0. If it fails, fix Docker GPU access before continuing. The disk previously had about 42 GB free; dense outputs can be large.

Record the installed image for repeatability; there is no need to pull a new image for every run:

```bash
docker image inspect colmap/colmap:latest \
  --format '{{index .RepoDigests 0}}' > "$COLMAP_RUN/container-image.txt"
```

## 4. Extract images from the video

```bash
ffmpeg -n -i "$COLMAP_RUN/video.mp4" \
  -vf "fps=2,scale=1920:1920:force_original_aspect_ratio=decrease:force_divisible_by=2" \
  -q:v 2 "$COLMAP_RUN/images/frame_%06d.jpg"
```

This saves two JPEGs per second, fitting each within 1920 × 1920 pixels while preserving its proportions. It works for portrait and landscape video. `-n` prevents overwriting existing frames.

For a slow walkthrough, `fps=1` is another starting point. Use a new experiment folder when changing extraction settings so old frames and database entries cannot get mixed in.

Count the images:

```bash
find "$COLMAP_RUN/images" -maxdepth 1 -name '*.jpg' | wc -l
```

Preview several JPEGs using VS Code Remote SSH. Check that they are sharp and consecutive frames overlap. Start with a short room recording; exhaustive matching below is intended for small experiments.

## 5. Define a short Docker command

Run this function definition inside the same tmux shell:

```bash
colmap_run() {
  docker run --rm --gpus 'device=0' \
    --user "$(id -u):$(id -g)" \
    -v "$COLMAP_RUN:/working" \
    -w /working \
    colmap/colmap:latest colmap "$@"
}
```

It runs COLMAP on GPU 0 and saves results in your experiment folder. `/working` inside Docker refers to that folder on the PC. The function lasts for this shell; redefine it if you open a new shell.

## 6. Extract visual features

```bash
colmap_run feature_extractor \
  --database_path /working/database.db \
  --image_path /working/images \
  --FeatureExtraction.gpu_index 0 \
  --FeatureExtraction.max_image_size 1920 \
  --SiftExtraction.max_num_features 4096 \
  > "$COLMAP_RUN/extraction.log" 2>&1
```

This finds visual details that can be matched between frames. When the prompt returns, immediately run:

```bash
echo $?
tail -n 30 "$COLMAP_RUN/extraction.log"
```

`0` means the process exited successfully. Also check the log for errors before continuing. The feature target does not guarantee an exact upper bound, so the matching limit in the next step is still useful.

## 7. Match images with limited GPU memory use

```bash
colmap_run exhaustive_matcher \
  --database_path /working/database.db \
  --FeatureMatching.gpu_index 0 \
  --FeatureMatching.num_threads 1 \
  --FeatureMatching.max_num_matches 4096 \
  > "$COLMAP_RUN/matching.log" 2>&1
```

This finds corresponding details across image pairs. These limits address the GPU memory failure from the first experiment.

When the prompt returns:

```bash
echo $?
tail -n 30 "$COLMAP_RUN/matching.log"
```

Proceed only if matching completed without errors.

## 8. Reconstruct cameras, points and surfaces

```bash
colmap_run automatic_reconstructor \
  --workspace_path /working \
  --image_path /working/images \
  --extraction 0 \
  --matching 0 \
  --quality medium \
  --gpu_index 0 \
  > "$COLMAP_RUN/reconstruction.log" 2>&1
```

This reuses the previous stages, estimates camera positions, and attempts dense reconstruction and meshing. The terminal stays quiet because output is written to the log.

To leave it running: press **Ctrl+B**, release both keys, then press **D**. You can now close SSH. Return later with:

```bash
tmux attach -t colmap
```

To watch progress from a **second SSH terminal** (adjust the folder name):

```bash
tail -f /home/vladi/Desktop/colmap-experiments/my-room-2/reconstruction.log
```

**Ctrl+C** in the log-viewing terminal stops only the viewer. Ctrl+C in the terminal running COLMAP interrupts reconstruction.

## 9. Check completion

In the reconstruction terminal, the shell prompt returns when the command ends. Immediately check:

```bash
echo $?
tail -n 40 "$COLMAP_RUN/reconstruction.log"
find "$COLMAP_RUN/dense" -type f -name '*.ply'
```

Check the exit code, log and actual outputs together. A process can finish without producing a usable reconstruction.

| Output | Meaning |
|---|---|
| `database.db` | Extracted features and image matches |
| `sparse/0/` | Camera estimates and sparse 3D points |
| `dense/0/fused.ply` | Dense point cloud |
| `dense/0/meshed-poisson.ply` | Surface mesh, if meshing succeeds |
| `*.log` | Progress and error messages |

There may be additional numbered folders if COLMAP produces disconnected reconstructions. A sparse cloud alone is not the finished room surface.

## 10. Download and inspect the model

On your **local computer**:

```bash
mkdir -p colmap-results/my-room-2
scp vladi@PC_ADDRESS:/home/vladi/Desktop/colmap-experiments/my-room-2/dense/0/fused.ply \
  colmap-results/my-room-2/
scp vladi@PC_ADDRESS:/home/vladi/Desktop/colmap-experiments/my-room-2/dense/0/meshed-poisson.ply \
  colmap-results/my-room-2/
```

Adjust the address, experiment name and filenames to the outputs found in step 9. Alternatively, download through the VS Code Remote SSH file explorer.

Install [MeshLab](https://www.meshlab.net/) on your local computer. Use **File → Import Mesh** to open `fused.ply`, then the mesh. Use point rendering for the point cloud if needed. Rotate and zoom to inspect room coverage, openings and recognizable assets.

Expect holes and noise. Meshing may fill unobserved regions, so compare it with the cloud and source images. RGB reconstruction has no guaranteed metre scale: use a measured dimension to set scale and other measurements to assess accuracy. The result is geometry, not yet separately labelled walls or maintenance assets.

## If something fails

- **GPU memory error in matching:** change `--FeatureMatching.max_num_matches 4096` to `2048` and rerun step 7. Alternatively use `--FeatureMatching.use_gpu 0` for CPU matching. Do not run step 8 until matching succeeds.
- **GPU memory error during dense reconstruction:** check `nvidia-smi`. Arrange to free GPU memory or retry step 8 with `--quality low`. Do not stop unrelated processes without knowing what they are.
- **“No images with matches” or no sparse model:** inspect `matching.log` first. If matching completed, check sharpness, overlap and camera movement. More frames or a better capture may be required; use a new experiment folder for changed input images.
- **SSH disconnected:** reconnect and attach to tmux; do not start a duplicate job.
- **Resuming the original `my-room-1` failed run:** set `COLMAP_RUN` to `/home/vladi/Desktop/colmap-experiments/my-room-1`, define the function in step 5, and start at step 7. Its extracted features already exist. If you have since completed matching, check its log before rerunning it.

Reference: [COLMAP command-line workflow](https://colmap.github.io/cli.html). Commands target the installed COLMAP 4.3 development image; option names may differ in other versions.
