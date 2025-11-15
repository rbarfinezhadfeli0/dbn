# Documentation: python/pyproject.toml

## File Metadata

**Path:** `python/pyproject.toml`
**Filename:** `pyproject.toml`
**Extension:** `.toml`
**Type:** Text

## Original Source

**Location:** `../../python/pyproject.toml`

### Source Content

```toml
[tool.poetry]
name = "databento-dbn"
version = "0.30.0"
description = "Python bindings for encoding and decoding Databento Binary Encoding (DBN)"
authors = ["Databento <support@databento.com>"]
license = "Apache-2.0"

[tool.poetry.dependencies]
python = ">=3.9"

[tool.poetry.dev-dependencies]
maturin = ">=1.0"

[build-system]
requires = ["maturin>=1.0"]
build-backend = "maturin"

[project]
name = "databento-dbn"
version = "0.30.0"
authors = [
    { name = "Databento", email = "support@databento.com" }
]
description = "Python bindings for encoding and decoding Databento Binary Encoding (DBN)"
readme = "README.md"
license = { file = "../LICENSE" }
requires-python = ">=3.9"
classifiers = [
    "Programming Language :: Rust",
    "Programming Language :: Python :: Implementation :: CPython",
]

[tool.maturin]
features = ["pyo3/extension-module"]
python-source = "python"
module-name = "databento_dbn._lib"

```

## High-Level Overview

This file is located at `python/pyproject.toml` within the repository.

### File Type: Configuration

This is a configuration file that defines settings, dependencies, or build parameters.

#### Role in Project

Configuration files control various aspects of the build process, dependencies, and project metadata.

