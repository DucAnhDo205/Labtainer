# DEW Evidence Video Sealing Lab

## Objectives

1. Explain the Differential Energy Watermarking idea.
2. Embed an evidence seal into a video using DCT-block energy differences.
3. Extract the message without the original video.
4. Measure visual distortion with PSNR.
5. Test robustness after a mild compression-like attack.

## Background

DEW hides a bit by changing the relative energy of two coefficient groups. In this lab, each selected 8x8 luminance block is transformed with DCT. Two mid-frequency groups are measured. A bit value is represented by which group has higher energy.

This lab is intentionally simplified. Real DEW for compressed JPEG/MPEG streams works closer to the codec coefficient domain. The simplified version is easier to inspect and suitable for a Labtainer exercise.

Scenario: a field analyst has a short grayscale evidence clip. The analyst must embed the seal `DEW-EVIDENCE-2026` with key `7301`, verify that it can be extracted blindly, and prove that the visible distortion stays below the PSNR limit.

## Before starting the lab

If this lab is being copied to a new Labtainer VM, build the local Docker images before starting the lab. This avoids a Docker Hub lookup when the VM is offline or cannot reach Docker Hub.

From the Labtainer student directory, run:

```bash
cd ~/labtainer/labtainer-student
rebuild -L -f -b dew-evidence
labtainer -r dew-evidence
```

If your Labtainer install uses the trunk path, use:

```bash
cd ~/labtainer/trunk/scripts/labtainer-student
./bin/rebuild -L -f -b dew-evidence
./bin/labtainer -r dew-evidence
```

If `labtainer -r dew-evidence` reports `Unable to reach Dockerhub` or `Could not find image info`, the DEW evidence images have not been built locally yet. Run the `rebuild -L -f -b dew-evidence` command above, then start the lab again.

If Docker reports that `local-net` already exists with the wrong subnet, stop old DEW containers and remove the stale network:

```bash
docker rm -f dew-evidence.demo.student dew-evidence.tester.student dew-evidence-igrader 2>/dev/null || true
docker network rm local-net 2>/dev/null || true
labtainer -r dew-evidence
```

## Tasks

### Task 1: Create the cover video

On the `demo` machine:

```bash
python make_cover.py
```

Confirm that `cover.dwv` exists.

### Task 2: Embed a hidden message

```bash
python dew_embed.py --in cover.dwv --out watermarked.dwv --message "DEW-EVIDENCE-2026" --key 7301
```

### Task 3: Extract the message

```bash
python dew_extract.py --in watermarked.dwv --length 17 --key 7301
```

Record the extracted message.

### Task 4: Measure quality

```bash
python quality.py --ref cover.dwv --test watermarked.dwv
```

Record the PSNR value. Explain whether the change is visually noticeable.

### Task 5: Test on the tester machine

Copy the watermarked video:

```bash
scp watermarked.dwv ubuntu@tester:/home/ubuntu/
```

On `tester`:

```bash
./run_tests.sh watermarked.dwv 17 7301
```

Record whether the original and re-encoded videos can still be decoded.

### Task 6: Prepare checkwork artifacts

On `demo`, run:

```bash
python submit_dew.py
```

The output must include:

```text
COVER_OK=Y
EXTRACT_OK=Y
PSNR_OK=Y
```

On `tester`, `run_tests.sh` must include:

```text
VERIFY_ORIGINAL=Y
VERIFY_ATTACKED=Y
```

Then run `checkwork dew-evidence` from the host terminal used to start the lab.

## Questions

1. Which DCT coefficient region is used in this lab, and why not the DC coefficient?
2. What is the tradeoff between watermark strength and PSNR?
3. Why can compression damage the hidden message?
4. How is DEW different from simple LSB steganography?
