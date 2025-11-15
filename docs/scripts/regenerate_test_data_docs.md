# regenerate_test_data.sh

## File Metadata

- **Path:** `scripts/regenerate_test_data.sh`
- **Type:** .sh
- **Lines:** 6
- **Characters:** 160
- **Words:** 21
- **Size:** text

## Original Source

```bash
#! /usr/bin/env bash

source "$(dirname "$0")/config.sh"
cd "${PROJECT_ROOT_DIR}/tests/data"
find . -name '*.dbn*' -exec cargo run -- {} --output {} --force \;

```

## Overview

This file is part of the repository at `scripts`.

## Detailed Analysis

## Performance & Security Notes


## Related Files

- Parent directory: `scripts/`

## Testing

This file appears to be a test file.

