#!/usr/bin/env bash
set -euo pipefail

LAB="${1:-}"

case "$LAB" in
    dew-video|dew-evidence|dew-audit)
        ;;
    "")
        echo "Usage: bash start-dew-lab.sh <dew-video|dew-evidence|dew-audit>" >&2
        exit 2
        ;;
    *)
        echo "Unknown DEW lab: $LAB" >&2
        echo "Use one of: dew-video, dew-evidence, dew-audit" >&2
        exit 2
        ;;
esac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d "$SCRIPT_DIR/labs/$LAB" ]; then
    echo "Could not find $SCRIPT_DIR/labs/$LAB" >&2
    echo "Run this script from the repository root that contains the labs directory." >&2
    exit 1
fi

find_student_dir() {
    if [ -n "${LABTAINER_STUDENT_DIR:-}" ] && [ -x "$LABTAINER_STUDENT_DIR/bin/labtainer" ]; then
        echo "$LABTAINER_STUDENT_DIR"
        return 0
    fi

    for candidate in \
        "$HOME/labtainer/labtainer-student" \
        "$HOME/labtainer/trunk/scripts/labtainer-student" \
        "$HOME/labtainer/scripts/labtainer-student" \
        "$SCRIPT_DIR/labtainer-student" \
        "$SCRIPT_DIR/trunk/scripts/labtainer-student" \
        "$SCRIPT_DIR/scripts/labtainer-student"; do
        if [ -x "$candidate/bin/labtainer" ]; then
            echo "$candidate"
            return 0
        fi
    done

    echo "Could not find Labtainer student directory." >&2
    echo "Set LABTAINER_STUDENT_DIR to the directory that contains bin/labtainer." >&2
    return 1
}

find_labs_dir() {
    local student_dir="$1"
    for candidate in \
        "$student_dir/../../labs" \
        "$student_dir/../labs" \
        "$HOME/labtainer/trunk/labs" \
        "$HOME/labtainer/labs" \
        "$SCRIPT_DIR/labs"; do
        if [ -d "$candidate" ]; then
            (cd "$candidate" && pwd)
            return 0
        fi
    done

    echo "Could not find Labtainer labs directory." >&2
    return 1
}

STUDENT_DIR="$(find_student_dir)"
LABS_DIR="$(find_labs_dir "$STUDENT_DIR")"
LABTAINER_DIR="$(cd "$LABS_DIR/.." && pwd)"
export LABTAINER_DIR

echo "[1/5] Syncing $LAB into $LABS_DIR"
SOURCE_LAB_DIR="$(cd "$SCRIPT_DIR/labs/$LAB" && pwd)"
TARGET_LAB_DIR="$LABS_DIR/$LAB"
mkdir -p "$TARGET_LAB_DIR"
TARGET_LAB_DIR="$(cd "$TARGET_LAB_DIR" && pwd)"
if [ "$SOURCE_LAB_DIR" != "$TARGET_LAB_DIR" ]; then
    cp -a "$SOURCE_LAB_DIR/." "$TARGET_LAB_DIR/"
else
    echo "      Source lab directory is already the Labtainer lab directory"
fi
chmod +x "$LABS_DIR/$LAB/bin/postzip" 2>/dev/null || true
find "$LABS_DIR/$LAB" -name "run_tests.sh" -exec chmod +x {} \; 2>/dev/null || true

case "$LAB" in
    dew-video)
        IMAGES=("dew-video.dew-video.student" "dew-video.tester.student")
        CONTAINERS=("dew-video.dew-video.student" "dew-video.tester.student" "dew-video-igrader")
        ;;
    dew-evidence)
        IMAGES=("dew-evidence.demo.student" "dew-evidence.tester.student")
        CONTAINERS=("dew-evidence.demo.student" "dew-evidence.tester.student" "dew-evidence-igrader")
        ;;
    dew-audit)
        IMAGES=("dew-audit.audit.student" "dew-audit.verifier.student")
        CONTAINERS=("dew-audit.audit.student" "dew-audit.verifier.student" "dew-audit-igrader")
        ;;
esac

missing_image=0
for image in "${IMAGES[@]}"; do
    if ! docker image inspect "$image" >/dev/null 2>&1; then
        missing_image=1
        break
    fi
done

cd "$STUDENT_DIR"

if [ "$missing_image" -eq 1 ]; then
    echo "[2/5] Local images are missing; building $LAB images once"
    ./bin/rebuild -L -f -b "$LAB"
else
    echo "[2/5] Local images already exist"
fi

echo "[3/5] Removing stale $LAB containers"
docker rm -f "${CONTAINERS[@]}" >/dev/null 2>&1 || true

echo "[4/5] Removing stale local-net if unused"
docker network rm local-net >/dev/null 2>&1 || true

echo "[5/5] Starting $LAB"
export DISPLAY="${DISPLAY:-:0}"
./bin/labtainer -q -r "$LAB"
