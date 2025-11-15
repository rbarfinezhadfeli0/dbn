# Documentation: rust/dbn-cli/Cargo.toml

## File Metadata

**Path:** `rust/dbn-cli/Cargo.toml`
**Filename:** `Cargo.toml`
**Extension:** `.toml`
**Type:** Text

## Original Source

**Location:** `../../../rust/dbn-cli/Cargo.toml`

### Source Content

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

## High-Level Overview

This file is located at `rust/dbn-cli/Cargo.toml` within the repository.

### File Type: Configuration

This is a configuration file that defines settings, dependencies, or build parameters.

#### Role in Project

Configuration files control various aspects of the build process, dependencies, and project metadata.

