# Cargo.toml

## File Metadata

- **Path:** `c/Cargo.toml`
- **Type:** .toml
- **Lines:** 23
- **Characters:** 522
- **Words:** 79
- **Size:** text

## Original Source

```toml
[package]
name = "dbn-c"
description = "C bindings for working with Databento Binary Encoding (DBN)"
# This crate should not be published
publish = false
authors.workspace = true
version.workspace = true
edition.workspace = true
license.workspace = true
repository.workspace = true

[lib]
name = "dbn_c"
crate-type = ["staticlib"]

[dependencies]
anyhow = { workspace = true }
dbn = { path = "../rust/dbn", features = [] }
libc = "0.2.171"

[build-dependencies]
cbindgen = { version = "0.28.0", default-features = false }

```

## Overview

This file is part of the repository at `c`.

This is a Rust package manifest file (Cargo.toml) that defines dependencies, metadata, and build configuration.

## Detailed Analysis

## Performance & Security Notes


## Related Files

- Parent directory: `c/`

## Testing

- Test file location: Not specified

