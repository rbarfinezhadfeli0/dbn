# Documentation: rust/dbn-macros/Cargo.toml

## File Metadata

**Path:** `rust/dbn-macros/Cargo.toml`
**Filename:** `Cargo.toml`
**Extension:** `.toml`
**Type:** Text

## Original Source

**Location:** `../../../rust/dbn-macros/Cargo.toml`

### Source Content

```toml
[package]
name = "dbn-macros"
description = "Proc macros for dbn crate"
authors.workspace = true
version.workspace = true
edition.workspace = true
license.workspace = true
repository.workspace = true

[lib]
proc-macro = true

[dependencies]
proc-macro-crate = "3.3.0"
proc-macro2 = "1.0.94"
quote = "1.0.40"
syn = { version = "2.0", features = ["full"] }

[dev-dependencies]
csv = { workspace = true }
dbn = { path = "../dbn" }
trybuild = "1.0.104"

```

## High-Level Overview

This file is located at `rust/dbn-macros/Cargo.toml` within the repository.

### File Type: Configuration

This is a configuration file that defines settings, dependencies, or build parameters.

#### Role in Project

Configuration files control various aspects of the build process, dependencies, and project metadata.

