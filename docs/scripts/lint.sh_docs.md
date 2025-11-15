# Documentation: scripts/lint.sh

## File Metadata

**Path:** `scripts/lint.sh`
**Filename:** `lint.sh`
**Extension:** `.sh`
**Type:** Text

## Original Source

**Location:** `../../scripts/lint.sh`

### Source Content

```sh
#! /usr/bin/env bash
set -e

cargo --version
cargo clippy --all-features -- --deny warnings
# `cargo doc` does not have a `--deny warnings` flag like clippy, workaround from:
# https://github.com/rust-lang/cargo/issues/8424#issuecomment-1070988443
RUSTDOCFLAGS='--deny warnings' cargo doc --all-features

```

## High-Level Overview

This file is located at `scripts/lint.sh` within the repository.

### File Type: Shell Script

This is a shell script used for automation, building, testing, or deployment tasks.

#### Script Purpose

Shell scripts automate common development tasks and ensure consistent build/test procedures.

