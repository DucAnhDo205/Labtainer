# DEW Video Steganography Lab

## Objectives

1. Explain the Differential Energy Watermarking idea.
2. Embed a short text message into a video using DCT-block energy differences.
3. Extract the message without the original video.
4. Measure visual distortion with PSNR.
5. Test robustness after mild video re-encoding.

## Background

DEW hides a bit by changing the relative energy of two coefficient groups. In this lab, each selected 8x8 luminance block is transformed with DCT. Two mid-frequency groups are measured. A bit value is represented by which group has higher energy.

This lab is intentionally simplified. Real DEW for compressed JPEG/MPEG streams works closer to the codec coefficient domain. The simplified version is easier to inspect and suitable for a Labtainer exercise.

## Before starting the lab

Import the IModule, then start the lab:

```bash
imodule https://raw.githubusercontent.com/DucAnhDo205/Labtainer/main/dew-video-labtainer.tar.gz
labtainer -r dew-video
```

The lab uses its own DEW Labtainer images and does not depend on unrelated lab images.

## Tasks

### Task 1: Create the cover video

On the `dew-video` machine:

```bash
python make_cover.py
```

Confirm that `cover.dwv` exists.

### Task 2: Embed a hidden message

```bash
python dew_embed.py --in cover.dwv --out watermarked.dwv --message "LABTAINERS-DEW-2026" --key 4242
```

### Task 3: Extract the message

```bash
python dew_extract.py --in watermarked.dwv --length 19 --key 4242
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
./run_tests.sh watermarked.dwv 19 4242
```

Record whether the original and re-encoded videos can still be decoded.

### Task 6: Prepare checkwork artifacts

On `dew-video`, run:

```bash
python submit_dew.py
```

The output must include:

```text
COVER_OK=Y
EMBED_BITS=152
EXTRACT_OK=Y
PSNR_OK=Y
```

On `tester`, `run_tests.sh` must include:

```text
VERIFY_ORIGINAL=Y
VERIFY_ATTACKED=Y
```

Then run:

```bash
checkwork dew-video
```

## Questions

1. Which DCT coefficient region is used in this lab, and why not the DC coefficient?
2. What is the tradeoff between watermark strength and PSNR?
3. Why can compression damage the hidden message?
4. How is DEW different from simple LSB steganography?
