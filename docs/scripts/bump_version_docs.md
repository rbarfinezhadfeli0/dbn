# bump_version.sh

## File Metadata

- **Path:** `scripts/bump_version.sh`
- **Type:** .sh
- **Lines:** 35
- **Characters:** 850
- **Words:** 102
- **Size:** text

## Original Source

```bash
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

## Overview

This file is part of the repository at `scripts`.

## Detailed Analysis

## Performance & Security Notes


## Related Files

- Parent directory: `scripts/`

## Testing

- Test file location: Not specified

