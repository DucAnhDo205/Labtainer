from __future__ import print_function

from dew_core import write_video


def main():
    width, height, frames = 128, 128, 12
    video_frames = []
    for frame_index in range(frames):
        frame = []
        for y in range(height):
            for x in range(width):
                value = (x * 3 + y * 2 + frame_index * 7 + ((x // 16) * 11)) % 256
                if 42 <= x <= 92 and 58 <= y <= 70:
                    value = 220
                frame.append(value)
        video_frames.append(frame)

    write_video("cover.dwv", {"format": "DEW educational grayscale video", "width": width, "height": height, "frames": video_frames})
    print("created cover.dwv")


if __name__ == "__main__":
    main()
