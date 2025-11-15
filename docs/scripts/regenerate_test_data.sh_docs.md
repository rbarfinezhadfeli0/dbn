# Documentation: scripts/regenerate_test_data.sh

## File Metadata

**Path:** `scripts/regenerate_test_data.sh`
**Filename:** `regenerate_test_data.sh`
**Extension:** `.sh`
**Type:** Text

## Original Source

**Location:** `../../scripts/regenerate_test_data.sh`

### Source Content

```sh
#! /usr/bin/env bash

source "$(dirname "$0")/config.sh"
cd "${PROJECT_ROOT_DIR}/tests/data"
find . -name '*.dbn*' -exec cargo run -- {} --output {} --force \;

```

## High-Level Overview

This file is located at `scripts/regenerate_test_data.sh` within the repository.

### File Type: Shell Script

This is a shell script used for automation, building, testing, or deployment tasks.

#### Script Purpose

Shell scripts automate common development tasks and ensure consistent build/test procedures.

