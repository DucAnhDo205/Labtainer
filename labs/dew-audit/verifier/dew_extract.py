import argparse

from dew_core import extract_video


def main():
    parser = argparse.ArgumentParser(description="Extract a message using simplified DEW.")
    parser.add_argument("--in", dest="src", required=True)
    parser.add_argument("--length", type=int, required=True)
    parser.add_argument("--key", type=int, default=9107)
    args = parser.parse_args()
    print(extract_video(args.src, args.length, args.key))


if __name__ == "__main__":
    main()
