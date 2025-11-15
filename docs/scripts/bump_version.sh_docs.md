# Documentation: scripts/bump_version.sh

## File Metadata

**Path:** `scripts/bump_version.sh`
**Filename:** `bump_version.sh`
**Extension:** `.sh`
**Type:** Text

## Original Source

**Location:** `../../scripts/bump_version.sh`

### Source Content

```sh
#! /usr/bin/env bash
#
# Updates the version to ${1}.
#

source "$(dirname "$0")/config.sh"

if [ -z "$1" ]; then
    echo "Usage: $0 <new-version>" >&2
    echo "Example: $0 0.1.2" >&2
    exit 1
fi

OLD_VERSION="$("${SCRIPTS_DIR}/get_version.sh")"
NEW_VERSION="$1"

# Replace package versions
find \
    "${PROJECT_ROOT_DIR}" \
    -type f \
    -name "*.toml" \
    -exec sed -Ei "s/^version\s*=\s*\"${OLD_VERSION}\"/version = \"${NEW_VERSION}\"/" {} \;
# Replace dependency versions
find \
    "${PROJECT_ROOT_DIR}" \
    -type f \
    -name "*.toml" \
    -exec sed -Ei "s/version\s*=\s*\"=${OLD_VERSION}\"/version = \"=${NEW_VERSION}\"/" {} \;
# Replace Python TOML version
find \
    "${PROJECT_ROOT_DIR}" \
    -type f \
    -name "pyproject.toml" \
    -exec sed -Ei "s/version\s*=\s*\"${OLD_VERSION}\"/version = \"=${NEW_VERSION}\"/" {} \;

```

## High-Level Overview

This file is located at `scripts/bump_version.sh` within the repository.

### File Type: Shell Script

This is a shell script used for automation, building, testing, or deployment tasks.

#### Script Purpose

Shell scripts automate common development tasks and ensure consistent build/test procedures.

