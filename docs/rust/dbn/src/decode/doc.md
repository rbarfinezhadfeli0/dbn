# Documentation for Folder: rust/dbn/src/decode

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

- **AsRef**: Core concept used throughout this module
- **BYTES**: Core concept used throughout this module
- **DBN_PREFIX**: Core concept used throughout this module
- **DBN_PREFIX_LEN**: Core concept used throughout this module
- **DBZ_PREFIX**: Core concept used throughout this module
- **Decoder**: Core concept used throughout this module
- **Error**: Core concept used throughout this module
- **FIXED_METADATA_LEN**: Core concept used throughout this module
- **Item**: Core concept used throughout this module
- **MAPPING_INTERVAL_ENCODED_SIZE**: Core concept used throughout this module
- **MIN_SYMBOL_MAPPING_ENCODED_SIZE**: Core concept used throughout this module
- **MetadataDecoder**: Core concept used throughout this module
- **RESERVED_LEN**: Core concept used throughout this module
- **RecordDecoder**: Core concept used throughout this module
- **SCHEMA_VERSION**: Core concept used throughout this module


## Important Files

### Additional Files

- [zstd.rs](./zstd.rs_docs.md)
- [stream.rs](./stream.rs_docs.md)
- [dbz.rs](./dbz.rs_docs.md)
- [merge.rs](./merge.rs_docs.md)
- [dbn.rs](./dbn.rs_docs.md)


## Data Flows & Interactions

This folder handles **decoding** operations:
- Reads DBN/DBZ format files
- Parses compressed (Zstandard) streams
- Validates metadata and record structures
- Provides streaming iterators for efficient processing


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

- **Parent folder**: [src](../doc.md)
- **dbn**: [View documentation](./dbn/doc.md)
