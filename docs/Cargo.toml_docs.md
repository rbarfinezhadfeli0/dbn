# Documentation: Cargo.toml

## File Metadata

**Path:** `Cargo.toml`
**Filename:** `Cargo.toml`
**Extension:** `.toml`
**Type:** Text

## Original Source

**Location:** `../Cargo.toml`

### Source Content

```toml
[workspace]
members = [
  "c",
  "python",
  "rust/dbn-cli",
  "rust/dbn-macros",
  "rust/dbn"
]
resolver = "2"

[workspace.package]
authors = ["Databento <support@databento.com>"]
edition = "2021"
version = "0.30.0"
documentation = "https://databento.com/docs"
repository = "https://github.com/databento/dbn"
license = "Apache-2.0"

[workspace.dependencies]
anyhow = "1.0.97"
csv = "1.3"
pyo3 = "0.24.0"
pyo3-build-config = "0.24.0"
rstest = "0.25.0"
serde = { version = "1.0", features = ["derive"] }
time = ">=0.3.35"
zstd = "0.13"

```

## High-Level Overview

This file is located at `Cargo.toml` within the repository.

### File Type: Configuration

This is a configuration file that defines settings, dependencies, or build parameters.

#### Role in Project

Configuration files control various aspects of the build process, dependencies, and project metadata.

