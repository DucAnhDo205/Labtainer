import argparse

from dew_core import embed_video


def main():
    parser = argparse.ArgumentParser(description="Embed a message using simplified DEW.")
    parser.add_argument("--in", dest="src", required=True)
    parser.add_argument("--out", dest="dst", required=True)
    parser.add_argument("--message", required=True)
    parser.add_argument("--key", type=int, default=7301)
    parser.add_argument("--strength", type=float, default=60.0)
    args = parser.parse_args()

    bits = embed_video(args.src, args.dst, args.message, args.key, args.strength)
    print("embedded_bits=%d" % bits)
    print("output=%s" % args.dst)


if __name__ == "__main__":
    main()
