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


def text_to_bits(text):
    bits = []
    for ch in text:
        value = ord(ch)
        for shift in range(7, -1, -1):
            bits.append((value >> shift) & 1)
    return bits


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


def idct8(coeff):
    out = [[0.0 for _ in range(8)] for _ in range(8)]
    for y in range(8):
        for x in range(8):
            total = 0.0
            for u in range(8):
                for v in range(8):
                    total += _alpha(u) * _alpha(v) * coeff[u][v] * COS[u][x] * COS[v][y]
            out[y][x] = 0.25 * total
    return out


def _energy(coeff, coords):
    return sum(coeff[y][x] * coeff[y][x] for y, x in coords)


def _scale_group(coeff, coords, scale):
    for y, x in coords:
        coeff[y][x] *= scale


def _positions(width, height, total_bits, key):
    positions = []
    for y in range(8, height - 8, 8):
        for x in range(8, width - 8, 8):
            positions.append((x, y))
    rng = random.Random(key)
    rng.shuffle(positions)
    if total_bits > len(positions):
        raise ValueError("message too long for cover video")
    return positions[:total_bits]


def _get_block(frame, width, x0, y0):
    block = []
    for y in range(8):
        row = []
        for x in range(8):
            row.append(float(frame[(y0 + y) * width + (x0 + x)]) - 128.0)
        block.append(row)
    return block


def _put_block(frame, width, x0, y0, block):
    for y in range(8):
        for x in range(8):
            value = int(round(block[y][x] + 128.0))
            frame[(y0 + y) * width + (x0 + x)] = max(0, min(255, value))


def embed_video(src, dst, message, key=4242, strength=60.0):
    video = read_video(src)
    width = int(video["width"])
    height = int(video["height"])
    frame = video["frames"][0]
    bits = text_to_bits(message)
    positions = _positions(width, height, len(bits), key)

    for bit, (x, y) in zip(bits, positions):
        coeff = dct8(_get_block(frame, width, x, y))
        high = float(strength)
        low = high / 6.0
        for cy, cx in GROUP_A:
            sign = -1.0 if coeff[cy][cx] < 0 else 1.0
            coeff[cy][cx] = sign * (high if bit == 1 else low)
        for cy, cx in GROUP_B:
            sign = -1.0 if coeff[cy][cx] < 0 else 1.0
            coeff[cy][cx] = sign * (low if bit == 1 else high)
        _put_block(frame, width, x, y, idct8(coeff))

    write_video(dst, video)
    return len(bits)


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
    new_frames = []
    for frame in video["frames"]:
        new_frames.append([int(round(value / float(step)) * step) for value in frame])
    video["frames"] = new_frames
    write_video(dst, video)
