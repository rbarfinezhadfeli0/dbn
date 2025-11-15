# Documentation for Folder: python/src

## Role in the Project

This folder contains **Python bindings** for the DBN Rust library.

Using PyO3, it exposes DBN functionality to Python developers, enabling:
- Fast decoding of DBN files in Python
- Type-safe Python classes for market data records
- Integration with the Databento Python client library


## Key Concepts

Key technical concepts in this folder:

- **DbnDecoder**: Core concept used throughout this module
- **Default**: Core concept used throughout this module
- **E**: Core concept used throughout this module
- **INIT**: Core concept used throughout this module
- **Inner**: Core concept used throughout this module
- **MockPyFile**: Core concept used throughout this module
- **NFLX**: Core concept used throughout this module
- **NFLX_ID**: Core concept used throughout this module
- **OUTPUT_ENC**: Core concept used throughout this module
- **PyFileLike**: Core concept used throughout this module
- **PySymbolIntervalMap**: Core concept used throughout this module
- **QQQ**: Core concept used throughout this module
- **QQQ_ID**: Core concept used throughout this module
- **SymbolIndex**: Core concept used throughout this module
- **SymbolMap**: Core concept used throughout this module


## Important Files

### Essential Files

- **[lib.rs](./lib.rs_docs.md)**: Library entry point

### Additional Files

- [transcoder.rs](./transcoder.rs_docs.md)
- [encode.rs](./encode.rs_docs.md)
- [dbn_decoder.rs](./dbn_decoder.rs_docs.md)


## Data Flows & Interactions

This folder bridges **Rust and Python**:
- Uses PyO3 for FFI bindings
- Exposes Rust types to Python
- Handles type conversion and error propagation
- Integrates with Python's memory model


## How to Work with This Folder

### Extending Functionality

When adding new features to this folder:
1. Follow existing code patterns and conventions
2. Add comprehensive tests
3. Update documentation
4. Consider backward compatibility

### Testing Changes

Run the test suite after modifications:
```bash
cargo test  # For Rust code
pytest      # For Python code
```

### Code Style

Follow the project's formatting standards:
```bash
./scripts/format.sh
./scripts/lint.sh
```


## Cross References

- **Parent folder**: [python](../doc.md)
