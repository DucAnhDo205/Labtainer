from __future__ import print_function

import argparse
import math

from dew_core import read_video


def main():
    parser = argparse.ArgumentParser(description="Compute average PSNR for .dwv videos.")
    parser.add_argument("--ref", required=True)
    parser.add_argument("--test", required=True)
    args = parser.parse_args()

    ref = read_video(args.ref)
    test = read_video(args.test)
    pixels = 0
    squared_error = 0.0
    for ref_frame, test_frame in zip(ref["frames"], test["frames"]):
        for a, b in zip(ref_frame, test_frame):
            squared_error += (a - b) ** 2
            pixels += 1
    if pixels == 0:
        raise RuntimeError("no comparable frames")
    mse = squared_error / float(pixels)
    psnr = 99.0 if mse == 0 else 20.0 * math.log10(255.0 / math.sqrt(mse))
    print("pixels=%d" % pixels)
    print("avg_psnr_db=%.2f" % psnr)


if __name__ == "__main__":
    main()
