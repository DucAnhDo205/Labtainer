from __future__ import print_function

import os

from dew_core import embed_video, extract_video, read_video


MESSAGE = "DEW-AUDIT-TRACE26"
KEY = 9107
LENGTH = len(MESSAGE)


def psnr(ref_path, test_path):
    import math

    ref = read_video(ref_path)
    test = read_video(test_path)
    pixels = 0
    squared_error = 0.0
    for ref_frame, test_frame in zip(ref["frames"], test["frames"]):
        for a, b in zip(ref_frame, test_frame):
            squared_error += (a - b) ** 2
            pixels += 1
    if pixels == 0:
        return 0.0
    mse = squared_error / float(pixels)
    return 99.0 if mse == 0 else 20.0 * math.log10(255.0 / math.sqrt(mse))


def main():
    if not os.path.exists("cover.dwv"):
        print("COVER_OK=N")
        print("ERROR=cover.dwv missing; run python make_cover.py")
        return

    print("COVER_OK=Y")
    bits = embed_video("cover.dwv", "watermarked.dwv", MESSAGE, KEY)
    print("EMBED_BITS=%d" % bits)

    extracted = extract_video("watermarked.dwv", LENGTH, KEY)
    print("EXTRACTED=%s" % extracted)
    print("EXTRACT_OK=%s" % ("Y" if extracted == MESSAGE else "N"))

    score = psnr("cover.dwv", "watermarked.dwv")
    print("PSNR_DB=%.2f" % score)
    print("PSNR_OK=%s" % ("Y" if score >= 30.0 else "N"))
    print("OUTPUT_FILE=watermarked.dwv")


if __name__ == "__main__":
    main()
