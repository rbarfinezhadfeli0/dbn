# Documentation for Folder: rust/dbn-cli/src

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
- **BufRead**: Core concept used throughout this module
- **DecodeRecordRef**: Core concept used throughout this module
- **FRAG_TS_OUT**: Core concept used throughout this module
- **LimitFilter**: Core concept used throughout this module
- **OutputEncoding**: Core concept used throughout this module
- **STDIN_SENTINEL**: Core concept used throughout this module
- **SchemaFilter**: Core concept used throughout this module
- **as**: Core concept used throughout this module
- **decode_frag**: Core concept used throughout this module
- **decode_record_ref**: Core concept used throughout this module
- **encode_fragment**: Core concept used throughout this module
- **encode_from_dbn**: Core concept used throughout this module
- **encode_from_frag**: Core concept used throughout this module
- **infer_encoding**: Core concept used throughout this module


## Important Files

### Essential Files

- **[lib.rs](./lib.rs_docs.md)**: Library entry point
- **[main.rs](./main.rs_docs.md)**: Application entry point

### Additional Files

- [encode.rs](./encode.rs_docs.md)
- [filter.rs](./filter.rs_docs.md)


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

- **Parent folder**: [dbn-cli](../doc.md)
