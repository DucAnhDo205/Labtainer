# DEW Audit Video Trace Lab

## Objectives

1. Explain how Differential Energy Watermarking represents a bit with DCT coefficient energy.
2. Embed an audit trace into a video using two mid-frequency DCT coefficient groups.
3. Extract the trace without the original cover video.
4. Measure distortion with PSNR.
5. Test whether the trace survives a mild compression-like attack.

## Scenario

An internal audit team needs to mark a short grayscale monitoring clip before handing it to another group. The trace must be hidden in the video and recoverable later without the original cover file.

Your trace message is:

```text
DEW-AUDIT-TRACE26
```

Use key:

```text
9107
```

## Background

DEW hides a bit by changing the relative energy of two coefficient groups. In this lab, each selected 8x8 block from the first frame is transformed with DCT. If group A has more energy than group B, the extracted bit is `1`. If group B has more energy than group A, the extracted bit is `0`.

The lab uses a simple `.dwv` educational video format so it can run on the Labtainer base image without OpenCV, FFmpeg, NumPy, or apt package installation.

## Before starting the lab

If this lab is being copied to a new Labtainer VM, use the repository start script. It syncs the lab files, builds missing local Docker images, removes stale DEW containers/networks, and starts the lab. You do not need to run `rebuild` manually.

From the repository root, run only these two commands:

```bash
git pull
bash start-dew-lab.sh dew-audit
```

If your Labtainer installation is not under `~/labtainer/labtainer-student` or `~/labtainer/trunk/scripts/labtainer-student`, set `LABTAINER_STUDENT_DIR` once in the same shell:

```bash
export LABTAINER_STUDENT_DIR=/path/to/labtainer-student
bash start-dew-lab.sh dew-audit
```

The script prevents the common `Unable to reach Dockerhub` / `Could not find image info` error by building the required local images before `labtainer -r` is called.

## Tasks

### Task 1: Create the cover video

On the `audit` machine:

```bash
python make_cover.py
```

Confirm that `cover.dwv` exists.

### Task 2: Embed the audit trace

```bash
python dew_embed.py --in cover.dwv --out watermarked.dwv --message "DEW-AUDIT-TRACE26" --key 9107
```

### Task 3: Extract the trace

```bash
python dew_extract.py --in watermarked.dwv --length 17 --key 9107
```

Record the extracted text.

### Task 4: Measure quality

```bash
python quality.py --ref cover.dwv --test watermarked.dwv
```

The PSNR must be at least 30 dB.

### Task 5: Run the independent verifier

Copy the watermarked video:

```bash
scp watermarked.dwv ubuntu@verifier:/home/ubuntu/
```

On `verifier`:

```bash
./run_tests.sh watermarked.dwv 17 9107
```

The verifier checks both the original watermarked file and an attacked copy.

### Task 6: Prepare checkwork artifacts

On `audit`, run:

```bash
python submit_dew.py
```

The output must include:

```text
COVER_OK=Y
EMBED_BITS=136
EXTRACT_OK=Y
PSNR_OK=Y
```

On `verifier`, `run_tests.sh` must include:

```text
VERIFY_ORIGINAL=Y
VERIFY_ATTACKED=Y
```

Then run:

```bash
checkwork dew-audit
```

## Questions

1. Why does this lab use mid-frequency DCT coefficients instead of the DC coefficient?
2. What happens to PSNR if watermark strength is increased?
3. Why can a compression-like attack damage hidden data?
4. How is blind DEW extraction different from comparing against the original cover video?
