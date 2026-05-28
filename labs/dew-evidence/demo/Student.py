#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import zipfile


DEFAULT_LAB_NAME = "dew-evidence"


def skip_path(path):
    return ".cache" in path or "__pycache__" in path or path.startswith(".local/zip")


def read_first_existing(paths, default):
    for path in paths:
        if os.path.isfile(path):
            with open(path) as fh:
                value = fh.read().strip()
            if value:
                return value
    return default


def main():
    user_name = sys.argv[1] if len(sys.argv) > 1 else "ubuntu"
    home = os.path.join("/home", user_name)
    local = os.path.join(home, ".local")
    zip_dir = os.path.join(local, "zip")

    student_id = read_first_existing(
        [os.path.join(local, ".email"), os.path.join("/root", ".local", ".email")],
        "student",
    )
    lab_name = read_first_existing(
        [os.path.join(local, ".labname"), os.path.join("/root", ".local", ".labname")],
        DEFAULT_LAB_NAME,
    )

    if not os.path.isdir(zip_dir):
        os.makedirs(zip_dir)

    zip_name = "%s.%s.zip" % (student_id.replace("@", "_at_"), lab_name)
    final_path = os.path.join(zip_dir, zip_name)
    tmp_path = os.path.join("/tmp", zip_name)
    for path in (final_path, tmp_path):
        if os.path.exists(path):
            os.remove(path)

    with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(home):
            rel_root = os.path.relpath(root, home)
            if rel_root == ".":
                rel_root = ""
            dirs[:] = [d for d in dirs if not skip_path(os.path.join(rel_root, d))]
            for fname in files:
                full = os.path.join(root, fname)
                rel = os.path.relpath(full, home)
                if skip_path(rel):
                    continue
                try:
                    zf.write(full, rel)
                except OSError:
                    pass

    os.rename(tmp_path, final_path)
    os.chmod(final_path, 0o666)
    print("Created %s" % final_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
