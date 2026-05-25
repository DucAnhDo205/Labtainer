#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import zipfile


def skip_path(path):
    return ".cache" in path or "__pycache__" in path or path.startswith(".local/zip")


def main():
    user_name = sys.argv[1] if len(sys.argv) > 1 else "ubuntu"
    home = os.path.join("/home", user_name)
    local = os.path.join(home, ".local")
    zip_dir = os.path.join(local, "zip")
    student_id = "student"
    lab_name = "dew-evidence"

    email_path = os.path.join(local, ".email")
    lab_path = os.path.join(local, ".labname")
    if os.path.isfile(email_path):
        student_id = open(email_path).read().strip() or student_id
    if os.path.isfile(lab_path):
        lab_name = open(lab_path).read().strip() or lab_name

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
    print("Created %s" % final_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
