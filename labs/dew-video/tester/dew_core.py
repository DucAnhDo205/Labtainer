from __future__ import print_function

import json
import math
import random


GROUP_A = [(2, 3), (3, 2), (3, 3), (2, 4)]
GROUP_B = [(4, 1), (1, 4), (4, 2), (2, 5)]
COS = [[math.cos(((2 * x + 1) * u * math.pi) / 16.0) for x in range(8)] for u in range(8)]


def _alpha(i):
    return 1.0 / math.sqrt(2.0) if i == 0 else 1.0


def read_video(path):
    with open(path, "r") as handle:
        return json.load(handle)


def write_video(path, video):
    with open(path, "w") as handle:
        json.dump(video, handle, separators=(",", ":"))


def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        value = 0
        for bit in bits[i:i + 8]:
            value = (value << 1) | int(bit)
        chars.append(chr(value))
    return "".join(chars)


def dct8(block):
    out = [[0.0 for _ in range(8)] for _ in range(8)]
    for u in range(8):
        for v in range(8):
            total = 0.0
            for y in range(8):
                for x in range(8):
                    total += block[y][x] * COS[u][x] * COS[v][y]
            out[u][v] = 0.25 * _alpha(u) * _alpha(v) * total
    return out


def _energy(coeff, coords):
    return sum(coeff[y][x] * coeff[y][x] for y, x in coords)


def _positions(width, height, total_bits, key):
    positions = []
    for y in range(8, height - 8, 8):
        for x in range(8, width - 8, 8):
            positions.append((x, y))
    rng = random.Random(key)
    rng.shuffle(positions)
    return positions[:total_bits]


def _get_block(frame, width, x0, y0):
    block = []
    for y in range(8):
        row = []
        for x in range(8):
            row.append(float(frame[(y0 + y) * width + (x0 + x)]) - 128.0)
        block.append(row)
    return block


def extract_video(src, msg_len, key=4242):
    video = read_video(src)
    width = int(video["width"])
    height = int(video["height"])
    frame = video["frames"][0]
    positions = _positions(width, height, msg_len * 8, key)
    bits = []
    for x, y in positions:
        coeff = dct8(_get_block(frame, width, x, y))
        bits.append(1 if _energy(coeff, GROUP_A) > _energy(coeff, GROUP_B) else 0)
    return bits_to_text(bits)


def quantize_video(src, dst, step):
    video = read_video(src)
    video["frames"] = [[int(round(value / float(step)) * step) for value in frame] for frame in video["frames"]]
    write_video(dst, video)
