#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

find "$ROOT" -maxdepth 1 -type d -name "jj_*" | while read -r dir; do
    echo "=============================="
    echo "Processing $dir"
    echo "=============================="

    dockerfile="$dir/environment/Dockerfile"
    testfile="$dir/bootstrap/test_initial_state.py"

    if [[ ! -f "$dockerfile" ]]; then
        echo "Skip: no Dockerfile"
        continue
    fi

    if [[ ! -f "$testfile" ]]; then
        echo "Skip: no test_initial_state.py"
        continue
    fi

    image_name="jj-test-$(basename "$dir")"

    echo "Building image $image_name"
    docker build -t "$image_name" -f "$dockerfile" "$dir"

    echo "Running bootstrap test"
    docker run --rm \
        -v "$dir:/workspace" \
        -w /workspace \
        "$image_name" \
        python3 bootstrap/test_initial_state.py

    echo "✅ $dir passed"
done

