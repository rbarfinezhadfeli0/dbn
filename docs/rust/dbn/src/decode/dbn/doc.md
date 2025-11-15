# Documentation for Folder: rust/dbn/src/decode/dbn

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
- **Buffer**: Core concept used throughout this module
- **Decoder**: Core concept used throughout this module
- **DecoderState**: Core concept used throughout this module
- **MetadataDecoder**: Core concept used throughout this module
- **OHLCV_MSG**: Core concept used throughout this module
- **RecordDecoder**: Core concept used throughout this module
- **RecordFramer**: Core concept used throughout this module
- **U32_SIZE**: Core concept used throughout this module
- **U64_SIZE**: Core concept used throughout this module
- **advance**: Core concept used throughout this module
- **buffer_reserve**: Core concept used throughout this module
- **buffer_slice**: Core concept used throughout this module
- **clear**: Core concept used throughout this module
- **compat_buffer_slice**: Core concept used throughout this module


## Important Files

### Additional Files

- [async.rs](./async.rs_docs.md)
- [sync.rs](./sync.rs_docs.md)


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

- **Parent folder**: [decode](../doc.md)
