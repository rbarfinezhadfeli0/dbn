# Cargo.toml

## File Metadata

- **Path:** `rust/dbn-cli/Cargo.toml`
- **Type:** .toml
- **Lines:** 31
- **Characters:** 858
- **Words:** 123
- **Size:** text

## Original Source

```toml
[package]
name = "dbn-cli"
description = "Command-line utility for converting Databento Binary Encoding (DBN) files to text-based formats"
default-run = "dbn"
keywords = ["market-data", "json", "csv", "conversion", "encoding"]
# see https://crates.io/category_slugs
categories = ["command-line-utilities", "encoding"]
authors.workspace = true
version.workspace = true
edition.workspace = true
license.workspace = true
repository.workspace = true

[[bin]]
name = "dbn"
path = "src/main.rs"

[dependencies]
dbn = { path = "../dbn", version = "=0.30.0", default-features = false }

anyhow = { workspace = true }
clap = { version = "4.5", features = ["derive", "wrap_help"] }
serde = { workspace = true, features = ["derive"] }
zstd = { workspace = true }

[dev-dependencies]
assert_cmd = "2.0"
predicates = "3.1"
rstest = { workspace = true }
tempfile = "3.19"

```

## Overview

This file is part of the repository at `rust/dbn-cli`.

This is a Rust package manifest file (Cargo.toml) that defines dependencies, metadata, and build configuration.

## Detailed Analysis

## Performance & Security Notes

- 🔐 May contain security-sensitive code (passwords/keys/tokens)

## Related Files

- Parent directory: `rust/dbn-cli/`

## Testing

- Test file location: Not specified

