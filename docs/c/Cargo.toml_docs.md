# Documentation: c/Cargo.toml

## File Metadata

**Path:** `c/Cargo.toml`
**Filename:** `Cargo.toml`
**Extension:** `.toml`
**Type:** Text

## Original Source

**Location:** `../../c/Cargo.toml`

### Source Content

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

## High-Level Overview

This file is located at `c/Cargo.toml` within the repository.

### File Type: Configuration

This is a configuration file that defines settings, dependencies, or build parameters.

#### Role in Project

Configuration files control various aspects of the build process, dependencies, and project metadata.

