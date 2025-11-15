# Documentation: python/Cargo.toml

## File Metadata

**Path:** `python/Cargo.toml`
**Filename:** `Cargo.toml`
**Extension:** `.toml`
**Type:** Text

## Original Source

**Location:** `../../python/Cargo.toml`

### Source Content

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

## High-Level Overview

This file is located at `python/Cargo.toml` within the repository.

### File Type: Configuration

This is a configuration file that defines settings, dependencies, or build parameters.

#### Role in Project

Configuration files control various aspects of the build process, dependencies, and project metadata.

