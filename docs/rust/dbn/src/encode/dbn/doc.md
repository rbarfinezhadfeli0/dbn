# Documentation for Folder: rust/dbn/src/encode/dbn

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

- **Encoder**: Core concept used throughout this module
- **MIN_ENCODED_SIZE**: Core concept used throughout this module
- **MetadataEncoder**: Core concept used throughout this module
- **RecordEncoder**: Core concept used throughout this module
- **START_OFFSET**: Core concept used throughout this module
- **START_SEEK_FROM**: Core concept used throughout this module
- **calc_length**: Core concept used throughout this module
- **encode**: Core concept used throughout this module
- **encode_date**: Core concept used throughout this module
- **encode_fixed_len_cstr**: Core concept used throughout this module
- **encode_range_and_counts**: Core concept used throughout this module
- **encode_record**: Core concept used throughout this module
- **encode_record_ref**: Core concept used throughout this module
- **encode_record_ref_ts_out**: Core concept used throughout this module
- **encode_ref**: Core concept used throughout this module


## Important Files

### Additional Files

- [async.rs](./async.rs_docs.md)
- [sync.rs](./sync.rs_docs.md)


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
