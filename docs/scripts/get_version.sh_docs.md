# Documentation: scripts/get_version.sh

## File Metadata

**Path:** `scripts/get_version.sh`
**Filename:** `get_version.sh`
**Extension:** `.sh`
**Type:** Text

## Original Source

**Location:** `../../scripts/get_version.sh`

### Source Content

```sh
#! /usr/bin/env bash

source "$(dirname "$0")/config.sh"
grep -E '^version =' "${PROJECT_ROOT_DIR}/Cargo.toml" | cut -d'"' -f 2

```

## High-Level Overview

This file is located at `scripts/get_version.sh` within the repository.

### File Type: Shell Script

This is a shell script used for automation, building, testing, or deployment tasks.

#### Script Purpose

Shell scripts automate common development tasks and ensure consistent build/test procedures.

