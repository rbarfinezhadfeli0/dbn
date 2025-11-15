# get_version.sh

## File Metadata

- **Path:** `scripts/get_version.sh`
- **Type:** .sh
- **Lines:** 5
- **Characters:** 128
- **Words:** 16
- **Size:** text

## Original Source

```bash
#! /usr/bin/env bash

source "$(dirname "$0")/config.sh"
grep -E '^version =' "${PROJECT_ROOT_DIR}/Cargo.toml" | cut -d'"' -f 2

```

## Overview

This file is part of the repository at `scripts`.

## Detailed Analysis

## Performance & Security Notes


## Related Files

- Parent directory: `scripts/`

## Testing

- Test file location: Not specified

