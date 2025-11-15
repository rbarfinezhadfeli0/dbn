# pyproject.toml

## File Metadata

- **Path:** `python/pyproject.toml`
- **Type:** .toml
- **Lines:** 37
- **Characters:** 914
- **Words:** 111
- **Size:** text

## Original Source

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

## Overview

This file is part of the repository at `python`.

This is a Python project configuration file defining build system requirements and project metadata.

## Detailed Analysis

## Performance & Security Notes


## Related Files

- Parent directory: `python/`

## Testing

- Test file location: Not specified

