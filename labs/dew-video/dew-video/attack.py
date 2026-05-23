from __future__ import print_function

import argparse

from dew_core import quantize_video


def main():
    parser = argparse.ArgumentParser(description="Apply a simple compression-like quantization attack.")
    parser.add_argument("--in", dest="src", required=True)
    parser.add_argument("--out", dest="dst", required=True)
    parser.add_argument("--step", type=int, default=4)
    args = parser.parse_args()
    quantize_video(args.src, args.dst, args.step)
    print("created %s" % args.dst)


if __name__ == "__main__":
    main()
