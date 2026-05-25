from __future__ import print_function

from dew_core import write_video


def main():
    width, height, frames = 128, 128, 12
    video_frames = []
    for frame_index in range(frames):
        frame = []
        for y in range(height):
            for x in range(width):
                value = (x * 5 + y * 3 + frame_index * 11 + ((x // 12) * 7) + ((y // 20) * 17)) % 256
                if 12 <= x <= 116 and 18 <= y <= 30:
                    value = 52
                if 12 <= x <= 116 and 76 <= y <= 88:
                    value = 206
                if 32 <= x <= 44 and 38 <= y <= 110:
                    value = 168
                if 82 <= x <= 96 and 38 <= y <= 110:
                    value = 96
                frame.append(value)
        video_frames.append(frame)

    write_video("cover.dwv", {"format": "DEW audit grayscale video", "width": width, "height": height, "frames": video_frames})
    print("created cover.dwv")


if __name__ == "__main__":
    main()
