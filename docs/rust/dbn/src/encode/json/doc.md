# Documentation for Folder: rust/dbn/src/encode/json

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

- **BAR**: Core concept used throughout this module
- **BID_ASK_JSON**: Core concept used throughout this module
- **Encoder**: Core concept used throughout this module
- **EncoderBuilder**: Core concept used throughout this module
- **HEADER_JSON**: Core concept used throughout this module
- **JsonSerialize**: Core concept used throughout this module
- **N**: Core concept used throughout this module
- **PRETTY_PX**: Core concept used throughout this module
- **PRETTY_TS**: Core concept used throughout this module
- **WriteField**: Core concept used throughout this module
- **_PRETTY_PX**: Core concept used throughout this module
- **_PRETTY_TS**: Core concept used throughout this module
- **build**: Core concept used throughout this module
- **builder**: Core concept used throughout this module
- **encode_metadata**: Core concept used throughout this module


## Important Files

### Additional Files

- [async.rs](./async.rs_docs.md)
- [sync.rs](./sync.rs_docs.md)
- [serialize.rs](./serialize.rs_docs.md)


## Data Flows & Interactions

This folder handles **encoding** operations:
- Converts market data records to various output formats
- Supports DBN, CSV, JSON encodings
- Provides both sync and async APIs
- Interacts with record types defined in parent modules


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

- **Parent folder**: [encode](../doc.md)
