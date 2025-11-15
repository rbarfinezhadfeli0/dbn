# Documentation for Folder: rust/dbn/src

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

- **Action**: Core concept used throughout this module
- **AsRef**: Core concept used throughout this module
- **AsyncSkipBytes**: Core concept used throughout this module
- **BAD_TS_RECV**: Core concept used throughout this module
- **BBO_1M**: Core concept used throughout this module
- **BBO_1S**: Core concept used throughout this module
- **BID_ASK**: Core concept used throughout this module
- **Bbo1MMsg**: Core concept used throughout this module
- **Bbo1SMsg**: Core concept used throughout this module
- **BboMsg**: Core concept used throughout this module
- **BidAskPair**: Core concept used throughout this module
- **BufferSlice**: Core concept used throughout this module
- **CBBO_1M**: Core concept used throughout this module
- **CBBO_1S**: Core concept used throughout this module
- **CMBP1**: Core concept used throughout this module


## Important Files

### Essential Files

- **[lib.rs](./lib.rs_docs.md)**: Library entry point

### Additional Files

- [decode.rs](./decode.rs_docs.md)
- [publishers.rs](./publishers.rs_docs.md)
- [error.rs](./error.rs_docs.md)
- [macros.rs](./macros.rs_docs.md)
- [v3.rs](./v3.rs_docs.md)
- [v2.rs](./v2.rs_docs.md)
- [encode.rs](./encode.rs_docs.md)
- [python.rs](./python.rs_docs.md)
- [pretty.rs](./pretty.rs_docs.md)
- [enums.rs](./enums.rs_docs.md)

*... and 10 more files (see [index](./index.md))*


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

- **Parent folder**: [dbn](../doc.md)
- **python**: [View documentation](./python/doc.md)
- **record**: [View documentation](./record/doc.md)
- **v3**: [View documentation](./v3/doc.md)
- **metadata**: [View documentation](./metadata/doc.md)
- **encode**: [View documentation](./encode/doc.md)
