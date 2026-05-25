from __future__ import print_function

from dew_core import write_video


def main():
    width, height, frames = 128, 128, 12
    video_frames = []
    for frame_index in range(frames):
        frame = []
        for y in range(height):
            for x in range(width):
                value = (x * 2 + y * 5 + frame_index * 9 + ((y // 16) * 13)) % 256
                if 18 <= x <= 110 and 14 <= y <= 24:
                    value = 38
                if 22 <= x <= 106 and 96 <= y <= 108:
                    value = 214
                if 56 <= x <= 72 and 40 <= y <= 88:
                    value = 180
                frame.append(value)
        video_frames.append(frame)

    write_video("cover.dwv", {"format": "DEW evidence grayscale video", "width": width, "height": height, "frames": video_frames})
    print("created cover.dwv")


if __name__ == "__main__":
    main()
