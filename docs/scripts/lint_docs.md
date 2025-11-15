# lint.sh

## File Metadata

- **Path:** `scripts/lint.sh`
- **Type:** .sh
- **Lines:** 9
- **Characters:** 304
- **Words:** 34
- **Size:** text

## Original Source

```bash
#! /usr/bin/env bash
set -e

cargo --version
cargo clippy --all-features -- --deny warnings
# `cargo doc` does not have a `--deny warnings` flag like clippy, workaround from:
# https://github.com/rust-lang/cargo/issues/8424#issuecomment-1070988443
RUSTDOCFLAGS='--deny warnings' cargo doc --all-features

```

## Overview

This file is part of the repository at `scripts`.

## Detailed Analysis

## Performance & Security Notes


## Related Files

- Parent directory: `scripts/`

## Testing

- Test file location: Not specified

