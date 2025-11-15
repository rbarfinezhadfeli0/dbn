# Documentation for Folder: rust/dbn/src/python

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
- **BboMsg**: Core concept used throughout this module
- **BidAskPair**: Core concept used throughout this module
- **CbboMsg**: Core concept used throughout this module
- **Cmbp1Msg**: Core concept used throughout this module
- **Compression**: Core concept used throughout this module
- **ConsolidatedBidAskPair**: Core concept used throughout this module
- **Encoding**: Core concept used throughout this module
- **Error**: Core concept used throughout this module
- **ErrorMsg**: Core concept used throughout this module
- **ErrorMsgV1**: Core concept used throughout this module
- **ImbalanceMsg**: Core concept used throughout this module
- **InstrumentClass**: Core concept used throughout this module
- **InstrumentDefMsg**: Core concept used throughout this module
- **InstrumentDefMsgV1**: Core concept used throughout this module


## Important Files

### Additional Files

- [enums.rs](./enums.rs_docs.md)
- [record.rs](./record.rs_docs.md)
- [metadata.rs](./metadata.rs_docs.md)


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

- **Parent folder**: [src](../doc.md)
