"""Evaluation pipeline: frames -> method -> evaluation.

Usage:   python code/run_pipeline.py <method> <room> [--assets FILE] [--runs-dir DIR]
Example: python code/run_pipeline.py sam3 room002

Inputs:  data/<room>/video.mp4, data/<room>/asset-types.csv, data/<room>/ground-truth.csv
         --assets replaces asset-types.csv, for example to test one asset type.
Output:  <runs-dir>/exp<NNN>-<room>-<method>/ with the next free run number:
         inputs/          copies of the asset types and the ground truth
         frames/          10 frames per second, 1920 px wide
         counts.csv       asset list written by the method (asset,count)
         evaluation.csv   asset,truth,predicted,error
         timing.csv       step,seconds (wall-clock time of each step and of the whole run)
         run.log          everything printed on the terminal
"""
import argparse
import csv
import datetime
import os
import re
import shutil
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Each method runs as a separate program in its own environment. It is called as
# <command> <frames-dir> <asset-types.csv> <run-dir> and must write <run-dir>/counts.csv.
METHODS = {
    "sam3": ["conda", "run", "--no-capture-output", "-n", "sam3",
             "python", os.path.join(ROOT, "code", "methods", "sam3_video.py")],
}


def next_run_dir(runs_dir, room, method):
    """Create the run folder with the next free number. Numbers are never reused."""
    os.makedirs(runs_dir, exist_ok=True)
    numbers = [int(m.group(1)) for name in os.listdir(runs_dir)
               if (m := re.match(r"exp(\d{3})", name))]
    run_dir = os.path.join(runs_dir, f"exp{max(numbers, default=0) + 1:03d}-{room}-{method}")
    os.makedirs(run_dir)
    return run_dir


def read_counts(path):
    """Read a CSV whose first two columns are asset type and count."""
    with open(path, newline="") as f:
        return {row[0]: row[1].strip() for row in list(csv.reader(f))[1:] if row}


def evaluate(counts_path, truth_path, out_path):
    """Write asset,truth,predicted,error for every asset type in the ground truth."""
    predicted = read_counts(counts_path)
    rows = []
    for asset, truth in read_counts(truth_path).items():
        pred = predicted.get(asset, "")  # missing or failed: empty
        error = f"{int(pred) - int(truth):+d}" if pred else ""
        rows.append([asset, truth, pred, error])
    with open(out_path, "x", newline="") as f:
        csv.writer(f).writerows([["asset", "truth", "predicted", "error"]] + rows)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("method", choices=METHODS)
    parser.add_argument("room")
    parser.add_argument("--assets", help="asset types file instead of data/<room>/asset-types.csv")
    parser.add_argument("--runs-dir", default=os.path.join(ROOT, "runs"))
    args = parser.parse_args()

    room_dir = os.path.join(ROOT, "data", args.room)
    video = os.path.join(room_dir, "video.mp4")
    assets = args.assets or os.path.join(room_dir, "asset-types.csv")
    truth = os.path.join(room_dir, "ground-truth.csv")
    for path in (video, assets, truth):
        if not os.path.isfile(path):
            sys.exit(f"Error: {path} not found")

    run_dir = next_run_dir(args.runs_dir, args.room, args.method)
    log = open(os.path.join(run_dir, "run.log"), "w")

    def say(text):
        print(text, flush=True)
        log.write(text + "\n")
        log.flush()

    def run(command):
        """Run a program, show its output and copy it to run.log."""
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            say(line.rstrip("\n"))
        if proc.wait() != 0:
            say(f"Error: {command[0]} failed with exit code {proc.returncode}")
            sys.exit(1)

    commit = subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    say(f"Run:     {run_dir}")
    say(f"Command: {' '.join(sys.argv)}")
    say(f"Start:   {datetime.datetime.now():%Y-%m-%d %H:%M:%S}, git commit {commit or 'unknown'}")
    os.makedirs(os.path.join(run_dir, "inputs"))
    shutil.copy(assets, os.path.join(run_dir, "inputs", "asset-types.csv"))
    shutil.copy(truth, os.path.join(run_dir, "inputs", "ground-truth.csv"))

    timing = []
    start = time.time()

    say("\n=== 1. Frames")
    t = time.time()
    frames = os.path.join(run_dir, "frames")
    os.makedirs(frames)
    run(["ffmpeg", "-loglevel", "error", "-i", video, "-vf", "fps=10,scale=1920:-2",
         "-q:v", "2", "-start_number", "0", os.path.join(frames, "%05d.jpg")])
    say(f"{len(os.listdir(frames))} frames")
    timing.append(("frames", time.time() - t))

    say(f"\n=== 2. Method: {args.method}")
    t = time.time()
    run(METHODS[args.method] + [frames, os.path.join(run_dir, "inputs", "asset-types.csv"), run_dir])
    timing.append(("method", time.time() - t))

    say("\n=== 3. Evaluation")
    t = time.time()
    # Use the copy in inputs/, so that a change of the ground truth during the run has no effect
    rows = evaluate(os.path.join(run_dir, "counts.csv"), os.path.join(run_dir, "inputs", "ground-truth.csv"),
                    os.path.join(run_dir, "evaluation.csv"))
    say(f"{'asset':<20}{'truth':>6}{'predicted':>10}{'error':>7}")
    for asset, truth_count, predicted, error in rows:
        say(f"{asset:<20}{truth_count:>6}{predicted:>10}{error:>7}")
    timing.append(("evaluation", time.time() - t))
    timing.append(("total", time.time() - start))

    with open(os.path.join(run_dir, "timing.csv"), "x", newline="") as f:
        csv.writer(f).writerows([["step", "seconds"]] + [[n, f"{sec:.1f}"] for n, sec in timing])
    say("\n" + "  ".join(f"{n}: {sec / 60:.1f} min" for n, sec in timing))
    say(f"End:     {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")


if __name__ == "__main__":
    main()
