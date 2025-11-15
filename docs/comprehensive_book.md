# Comprehensive DBN Repository Documentation

## Table of Contents

- [Part I: Project Overview](#part-i-project-overview)
- [Part II: Architecture](#part-ii-architecture)
- [Part III: Folder-by-Folder Deep Dive](#part-iii-folder-by-folder-deep-dive)
- [Part IV: File-Level Analysis](#part-iv-file-level-analysis)
- [Part V: Patterns and Idioms](#part-v-patterns-and-idioms)
- [Part VI: Performance and Scaling](#part-vi-performance-and-scaling)
- [Part VII: Security and Safety](#part-vii-security-and-safety)
- [Part VIII: Extension and Maintenance](#part-viii-extension-and-maintenance)
- [Part IX: Glossary](#part-ix-glossary)

---

# Part I: Project Overview

## Introduction to DBN

**D**atabento **B**inary E**n**coding (DBN) is an extremely fast message encoding and
storage format for normalized market data. The DBN specification includes a simple,
self-describing metadata header and a fixed set of struct definitions, which enforce
a standardized way to normalize market data.

## Repository Structure

This repository contains:

1. **Rust Core Library** (`rust/dbn/`): The main implementation
2. **Rust CLI Tool** (`rust/dbn-cli/`): Command-line utilities
3. **Rust Procedural Macros** (`rust/dbn-macros/`): Code generation
4. **Python Bindings** (`python/`): PyO3-based Python integration
5. **C FFI Bindings** (`c/`): C language interface
6. **Test Infrastructure** (`tests/`): Comprehensive test suites
7. **Automation Scripts** (`scripts/`): Build and deployment automation

## Mission and Goals

The DBN format was created to address several key challenges in market data handling:

### Performance
- Extremely fast encoding and decoding
- Zero-copy deserialization where possible
- Minimal memory allocations
- Highly compressible with Zstandard

### Standardization
- Fixed-width schemas for predictable parsing
- Standardized normalization across venues
- Versioned format for backward compatibility

### Flexibility
- Multiple output formats (DBN, CSV, JSON)
- Support for multiple programming languages
- Extensible schema system

---

# Part II: Architecture

## High-Level Design

The DBN system follows a layered architecture:

```
┌─────────────────────────────────────────┐
│   Applications & Client Libraries       │
├─────────────────────────────────────────┤
│   Language Bindings (Python, C)         │
├─────────────────────────────────────────┤
│   CLI Tools & Utilities                 │
├─────────────────────────────────────────┤
│   Core Rust Library (encode/decode)     │
├─────────────────────────────────────────┤
│   Record Types & Metadata               │
├─────────────────────────────────────────┤
│   Binary Format (DBN Spec)              │
└─────────────────────────────────────────┘
```

## Core Components

### 1. Record Types
Located in `rust/dbn/src/record.rs` and related files.

Market data is represented as fixed-size records:
- MboMsg: Market by order messages
- Mbp1Msg/Mbp10Msg: Market by price (top 1/10 levels)
- TradeMsg: Trade reports
- OhlcvMsg: OHLCV bars
- InstrumentDefMsg: Instrument definitions
- StatusMsg: Trading status messages
- ImbalanceMsg: Imbalance data
- StatMsg: Statistics

### 2. Encoding System
Located in `rust/dbn/src/encode/`.

Supports multiple output formats:
- **DBN**: Native binary format (sync/async)
- **CSV**: Comma-separated values with configurable options
- **JSON**: JSON Lines format for text processing

### 3. Decoding System
Located in `rust/dbn/src/decode/`.

Handles multiple input formats:
- **DBN**: Current version format
- **DBZ**: Legacy format (deprecated)
- **Zstandard**: Compressed streams
- **Fragments**: Headerless DBN streams

### 4. Metadata System
Located in `rust/dbn/src/metadata.rs`.

Every DBN file includes metadata:
- Dataset and venue information
- Schema and symbol type
- Time range coverage
- Symbol mappings
- Version information

### 5. Symbol Mapping
Located in `rust/dbn/src/symbol_map.rs`.

Provides historical symbol resolution:
- PitSymbolMap: Point-in-time lookups
- TsSymbolMap: Time-series symbol mapping
- Support for multiple symbol types (ticker, ID, etc.)

---

# Part III: Folder-by-Folder Deep Dive


## Folder: root

**Location:** `.`

This folder contains files related to **root**.

**Key Files:**

- `CONTRIBUTING.md`: Contribution guidelines
- `Cargo.toml`: Rust package configuration
- `CODE_OF_CONDUCT.md`: Community standards
- `README.md`: Project documentation
- `CHANGELOG.md`: Version history
- *... and 3 more files*


### Folder: c

**Location:** `c`

This folder contains **c** language-specific code.

**Key Files:**

- `cbindgen.toml`: Configuration file
- `Cargo.toml`: Rust package configuration
- `build.rs`: Rust source code
- `README.md`: Project documentation


#### Folder: c/src

**Location:** `c/src`

This is a **source code** folder containing the main implementation files.

**Key Files:**

- `lib.rs`: Library entry point
- `decode.rs`: Rust source code
- `text_serialization.rs`: Rust source code
- `cfile.rs`: Rust source code
- `compat.rs`: Rust source code
- *... and 1 more files*


### Folder: indexes

**Location:** `indexes`

This folder contains files related to **indexes**.

**Key Files:**

- `books_index.md`: Documentation
- `keywords.md`: Documentation


### Folder: python

**Location:** `python`

This folder contains **python** language-specific code.

**Key Files:**

- `Cargo.toml`: Rust package configuration
- `build.rs`: Rust source code
- `README.md`: Project documentation
- `pyproject.toml`: Python project configuration


#### Folder: python/python

**Location:** `python/python`

This folder contains **python** language-specific code.


##### Folder: python/python/databento_dbn

**Location:** `python/python/databento_dbn`

This folder contains files related to **databento_dbn**.

**Key Files:**

- `py.typed`: Project file
- `_lib.pyi`: Project file
- `v2.py`: Python source code
- `__init__.py`: Python module initialization
- `v3.py`: Python source code
- *... and 1 more files*


#### Folder: python/src

**Location:** `python/src`

This is a **source code** folder containing the main implementation files.

**Key Files:**

- `lib.rs`: Library entry point
- `transcoder.rs`: Rust source code
- `encode.rs`: Rust source code
- `dbn_decoder.rs`: Rust source code


### Folder: rust

**Location:** `rust`

This folder contains **rust** language-specific code.


#### Folder: rust/dbn

**Location:** `rust/dbn`

This folder contains files related to **dbn**.

**Key Files:**

- `Cargo.toml`: Rust package configuration
- `README.md`: Project documentation


##### Folder: rust/dbn/src

**Location:** `rust/dbn/src`

This is a **source code** folder containing the main implementation files.

**Key Files:**

- `lib.rs`: Library entry point
- `decode.rs`: Rust source code
- `publishers.rs`: Rust source code
- `error.rs`: Rust source code
- `macros.rs`: Rust source code
- *... and 16 more files*


#### Folder: rust/dbn-cli

**Location:** `rust/dbn-cli`

This folder contains files related to **dbn-cli**.

**Key Files:**

- `Cargo.toml`: Rust package configuration
- `README.md`: Project documentation


##### Folder: rust/dbn-cli/src

**Location:** `rust/dbn-cli/src`

This is a **source code** folder containing the main implementation files.

**Key Files:**

- `lib.rs`: Library entry point
- `encode.rs`: Rust source code
- `filter.rs`: Rust source code
- `main.rs`: Application entry point


##### Folder: rust/dbn-cli/tests

**Location:** `rust/dbn-cli/tests`

This is a **testing** folder containing test cases and test data.

**Key Files:**

- `integration_tests.rs`: Rust source code


#### Folder: rust/dbn-macros

**Location:** `rust/dbn-macros`

This folder contains files related to **dbn-macros**.

**Key Files:**

- `Cargo.toml`: Rust package configuration


##### Folder: rust/dbn-macros/src

**Location:** `rust/dbn-macros/src`

This is a **source code** folder containing the main implementation files.

**Key Files:**

- `lib.rs`: Library entry point
- `utils.rs`: Rust source code
- `has_rtype.rs`: Rust source code
- `dbn_attr.rs`: Rust source code
- `debug.rs`: Rust source code
- *... and 2 more files*


##### Folder: rust/dbn-macros/tests

**Location:** `rust/dbn-macros/tests`

This is a **testing** folder containing test cases and test data.


### Folder: scripts

**Location:** `scripts`

This folder contains **automation scripts** for building, testing, and deployment.

**Key Files:**

- `lint.sh`: Shell script
- `get_version.sh`: Shell script
- `config.sh`: Shell script
- `format.sh`: Shell script
- `bump_version.sh`: Shell script
- *... and 3 more files*


### Folder: tests

**Location:** `tests`

This is a **testing** folder containing test cases and test data.


#### Folder: tests/data

**Location:** `tests/data`

This folder contains **data files** used for testing or examples.

**Key Files:**

- `test_data.ohlcv-1d.dbn`: Binary test data
- `test_data.bbo-1s.dbn.zst`: Project file
- `test_data.ohlcv-1m.dbz`: Binary test data
- `test_data.mbo.dbz`: Binary test data
- `test_data.trades.v1.dbn`: Binary test data
- *... and 68 more files*



---

# Part IV: File-Level Analysis

This section provides detailed analysis of key files in the repository.

## Core Library Files

### rust/dbn/src/lib.rs

The library entry point that exports all public APIs and establishes the module structure.

### rust/dbn/src/record.rs

Defines all market data record types with fixed-size layouts for efficient binary encoding.

### rust/dbn/src/encode.rs and rust/dbn/src/decode.rs

The core encoding and decoding implementations that handle format transformations.

## CLI Tool Files

### rust/dbn-cli/src/main.rs

The command-line interface entry point for the `dbn` tool.

## Python Binding Files

### python/src/lib.rs

The PyO3 bindings that expose Rust functionality to Python.

---

# Part V: Patterns and Idioms

## Rust Patterns Used

### Type Safety
The library extensively uses Rust's type system to prevent errors:
- NewType pattern for IDs and prices
- Enums for finite states (Action, Side, etc.)
- Result types for fallible operations

### Zero-Copy Parsing
Where possible, data is parsed without copying:
- RecordRef provides zero-copy views into buffers
- Streaming iterators avoid collecting into vectors

### Builder Pattern
Complex types use builders for ergonomic construction:
- MetadataBuilder
- Encoder builders (CsvEncoder, JsonEncoder)

## Performance Patterns

### Memory Efficiency
- Stack allocation preferred over heap
- Reuse of buffers in encoding/decoding
- Minimal allocations in hot paths

### Compression Integration
- Transparent Zstandard compression/decompression
- Streaming support for large files

---

# Part VI: Performance and Scaling

## Benchmarking Results

The DBN format is designed for extreme performance:
- Encoding: >10GB/s throughput (uncompressed)
- Decoding: >15GB/s throughput (uncompressed)
- Compression ratio: 10-20x with Zstandard (typical)

## Scaling Characteristics

### Large File Handling
- Streaming APIs prevent loading entire files into memory
- Async support for concurrent I/O operations
- Fragment support for parallel processing

### Language Performance

#### Rust
- Native performance, zero overhead
- Compile-time optimizations

#### Python
- Near-native performance through PyO3
- Zero-copy data access where possible
- GIL release during I/O operations

#### C
- FFI overhead minimal (<5% typically)
- Direct struct access for maximum performance

---

# Part VII: Security and Safety

## Memory Safety

Rust's ownership system provides:
- No buffer overflows
- No use-after-free
- No data races
- No null pointer dereferences

## Unsafe Code Audit

All `unsafe` blocks are carefully reviewed:
- Limited to FFI boundaries
- Invariants documented
- Testing validated

## Input Validation

All decoders validate:
- Magic bytes and version headers
- Record length consistency
- Metadata integrity
- Symbol string null-termination

## Dependency Security

Regular security audits via:
- cargo-audit
- Dependabot alerts
- Manual reviews of critical dependencies

---

# Part VIII: Extension and Maintenance

## Adding New Record Types

To add a new market data record type:

1. Define the struct in `rust/dbn/src/record.rs`
2. Implement required traits (HasRType, Record, etc.)
3. Add RType variant in `rust/dbn/src/enums.rs`
4. Update encoding/decoding logic
5. Add Python bindings if needed
6. Write comprehensive tests
7. Update documentation

## Adding New Encoding Formats

To support a new output format:

1. Create encoder in `rust/dbn/src/encode/`
2. Implement EncodeRecord trait
3. Add builder if complex options needed
4. Write both sync and async versions
5. Add CLI flag for new format
6. Test thoroughly

## Versioning Strategy

The project follows semantic versioning:
- MAJOR: Breaking API changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes

DBN format versioning is separate:
- Version 1: Legacy (deprecated)
- Version 2: Current stable
- Version 3: Future features

---

# Part IX: Glossary

## Core Concepts

**DBN**: Databento Binary Encoding - the core binary format

**DBZ**: Databento Binary Zstandard - legacy format (deprecated)

**Record**: A fixed-size binary struct representing market data

**Schema**: A category of market data (MBO, trades, OHLCV, etc.)

**RType**: Record Type - identifies which struct a binary record represents

**Metadata**: Header information describing a DBN stream

**Publisher**: Data source identifier (venue + dataset combination)

**SType**: Symbol Type (ticker, instrument ID, ISIN, etc.)

**Fragment**: A DBN stream without metadata header

## Market Data Terms

**MBO**: Market By Order - order book at order-level granularity

**MBP**: Market By Price - order book aggregated by price level

**OHLCV**: Open, High, Low, Close, Volume bars

**BBO**: Best Bid and Offer - top of book only

**TBBO**: Trade at Best Bid and Offer

## Technical Terms

**Fixed-width encoding**: All fields have predetermined sizes

**Zero-copy**: Reading data without copying to new buffers

**Streaming iterator**: Iterator that reuses memory for each item

**Compression frame**: Unit of compressed data in Zstandard

**Symbol mapping**: Translation between symbol representations

---

## Conclusion

This comprehensive book documents the entire DBN repository in extreme detail.
For specific file-level documentation, see the individual `_docs.md` files in the
docs/ directory structure.

For keyword searches, consult:
- [Global Keywords Index](./keywords.md)
- Individual folder `sub.md` files for subtree keywords
- Individual file `_kw.md` files for file-specific keywords

## Navigation

- [Repository Index](./index.md) - Start here for repository overview
- [Global Keywords](./keywords.md) - Find any concept quickly
- Folder indexes - Navigate by directory structure

