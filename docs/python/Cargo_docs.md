# Cargo.toml

## File Metadata

- **Path:** `python/Cargo.toml`
- **Type:** .toml
- **Lines:** 25
- **Characters:** 638
- **Words:** 98
- **Size:** text

## Original Source

```toml
[package]
name = "databento-dbn"
description = "Python library written in Rust for working with Databento Binary Encoding (DBN)"
# This crate should only be published as a Python package
publish = false
authors.workspace = true
version.workspace = true
edition.workspace = true
license.workspace = true
repository.workspace = true

[lib]
name = "databento_dbn" # Python modules can't contain dashes

[dependencies]
dbn = { path = "../rust/dbn", features = ["python"] }
pyo3 = { workspace = true }
time = { workspace = true }

[build-dependencies]
pyo3-build-config = { workspace = true }

[dev-dependencies]
rstest = { workspace = true }

```

## Overview

This file is part of the repository at `python`.

This is a Rust package manifest file (Cargo.toml) that defines dependencies, metadata, and build configuration.

## Detailed Analysis

## Performance & Security Notes


## Related Files

- Parent directory: `python/`

## Testing

- Test file location: Not specified

