# DBN Repository Documentation Index

## Repository: databento/dbn

**Databento Binary Encoding (DBN)** - Fast message encoding and storage format for normalized market data.

## Overview

This documentation system provides comprehensive coverage of every file and folder in the repository.

### Quick Navigation

- **[Comprehensive Book](./comprehensive_book.md)** - Read the entire repository as a book
- **[Global Keywords](./keywords.md)** - Find any concept quickly
- **[Root Documentation](./doc.md)** - High-level repository documentation
- **[Root Subtree Keywords](./sub.md)** - All keywords in the repository

## Repository Structure

**[./](./index.md)**
  ├── CONTRIBUTING.md
  ├── Cargo.toml
  ├── CODE_OF_CONDUCT.md
  └── ... 5 more files
  ├── **[c/](./c/index.md)**
    ├── cbindgen.toml
    ├── Cargo.toml
    ├── build.rs
    └── ... 1 more files
    ├── **[src/](./c/src/index.md)**
      ├── lib.rs
      ├── decode.rs
      ├── text_serialization.rs
      └── ... 3 more files
  ├── **[indexes/](./indexes/index.md)**
    ├── books_index.md
    ├── keywords.md
  ├── **[python/](./python/index.md)**
    ├── Cargo.toml
    ├── build.rs
    ├── README.md
    └── ... 1 more files
    ├── **[python/](./python/python/index.md)**
    ├── **[src/](./python/src/index.md)**
      ├── lib.rs
      ├── transcoder.rs
      ├── encode.rs
      └── ... 1 more files
  ├── **[rust/](./rust/index.md)**
    ├── **[dbn/](./rust/dbn/index.md)**
      ├── Cargo.toml
      ├── README.md
    ├── **[dbn-cli/](./rust/dbn-cli/index.md)**
      ├── Cargo.toml
      ├── README.md
    ├── **[dbn-macros/](./rust/dbn-macros/index.md)**
      ├── Cargo.toml
  ├── **[scripts/](./scripts/index.md)**
    ├── lint.sh
    ├── get_version.sh
    ├── config.sh
    └── ... 5 more files
  ├── **[tests/](./tests/index.md)**
    ├── **[data/](./tests/data/index.md)**
      ├── test_data.ohlcv-1d.dbn
      ├── test_data.bbo-1s.dbn.zst
      ├── test_data.ohlcv-1m.dbz
      └── ... 70 more files


## Main Components

### Rust Core Library
- **[rust/dbn/](./rust/dbn/index.md)** - Core DBN implementation
  - [Encoding](./rust/dbn/src/encode/index.md) - Format encoders
  - [Decoding](./rust/dbn/src/decode/index.md) - Format decoders
  - [Records](./rust/dbn/src/record/index.md) - Data type definitions

### Language Bindings
- **[python/](./python/index.md)** - Python bindings via PyO3
- **[c/](./c/index.md)** - C FFI bindings

### Tools
- **[rust/dbn-cli/](./rust/dbn-cli/index.md)** - Command-line tool
- **[scripts/](./scripts/index.md)** - Build and automation scripts

### Testing
- **[tests/](./tests/index.md)** - Test data and integration tests
- **[rust/dbn-macros/tests/](./rust/dbn-macros/tests/index.md)** - Macro tests

## Documentation System

### Per-File Documentation
Every file has:
- `<filename>_docs.md` - Comprehensive documentation
- `<filename>_kw.md` - Keyword index

### Per-Folder Documentation
Every folder has:
- `index.md` - File and subfolder listing
- `doc.md` - Narrative documentation
- `sub.md` - Subtree keyword index

### Global Documentation
- `comprehensive_book.md` - Complete repository book
- `keywords.md` - All keywords across repository
- `index.md` - This file

## Statistics

- **Total Files Documented:** 123
- **Total Folders:** 32
- **Total Keywords:** 1154
- **Documentation Files Generated:** 493

## How to Use This Documentation

1. **Start with the [Comprehensive Book](./comprehensive_book.md)** for a complete overview
2. **Use [Keywords](./keywords.md)** to find specific concepts
3. **Navigate by folder** using index.md files
4. **Deep dive into files** using _docs.md files

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md_docs.md) for contribution guidelines.

## License

See [LICENSE](./LICENSE_docs.md) for license information.

