# Documentation for Folder: rust/dbn-macros/src

## Role in the Project

This folder contains the **core Rust implementation** of the DBN library.

It provides fundamental functionality for:
- Encoding market data to DBN format
- Decoding DBN streams
- Type definitions for market data records
- Metadata handling
- Symbol mapping and conversion


## Key Concepts

Key technical concepts in this folder:

- **Args**: Core concept used throughout this module
- **AsRef**: Core concept used throughout this module
- **C_CHAR_ATTR**: Core concept used throughout this module
- **FIXED_PRICE_ATTR**: Core concept used throughout this module
- **FMT_BINARY**: Core concept used throughout this module
- **FMT_METHOD**: Core concept used throughout this module
- **INDEX_TS_ATTR**: Core concept used throughout this module
- **PRETTY_PX**: Core concept used throughout this module
- **PRETTY_TS**: Core concept used throughout this module
- **Parse**: Core concept used throughout this module
- **SKIP_ATTR**: Core concept used throughout this module
- **UNIX_NANOS_ATTR**: Core concept used throughout this module
- **as**: Core concept used throughout this module
- **as_ref**: Core concept used throughout this module
- **attribute_macro_impl**: Core concept used throughout this module


## Important Files

### Essential Files

- **[lib.rs](./lib.rs_docs.md)**: Library entry point

### Additional Files

- [utils.rs](./utils.rs_docs.md)
- [has_rtype.rs](./has_rtype.rs_docs.md)
- [dbn_attr.rs](./dbn_attr.rs_docs.md)
- [debug.rs](./debug.rs_docs.md)
- [py_field_desc.rs](./py_field_desc.rs_docs.md)
- [serialize.rs](./serialize.rs_docs.md)


## Data Flows & Interactions

This folder integrates with the broader project architecture through:
- Shared type definitions
- Common error handling patterns
- Standard library interfaces


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

- **Parent folder**: [dbn-macros](../doc.md)
