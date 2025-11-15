# Documentation for Folder: rust/dbn/src/record

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

- **BboMsg**: Core concept used throughout this module
- **BidAskPair**: Core concept used throughout this module
- **CbboMsg**: Core concept used throughout this module
- **Cmbp1Msg**: Core concept used throughout this module
- **ConsolidatedBidAskPair**: Core concept used throughout this module
- **Debug**: Core concept used throughout this module
- **Default**: Core concept used throughout this module
- **ErrorMsg**: Core concept used throughout this module
- **HEARTBEAT**: Core concept used throughout this module
- **ImbalanceMsg**: Core concept used throughout this module
- **InstrumentDefMsg**: Core concept used throughout this module
- **LENGTH_MULTIPLIER**: Core concept used throughout this module
- **MboMsg**: Core concept used throughout this module
- **Mbp10Msg**: Core concept used throughout this module
- **Mbp1Msg**: Core concept used throughout this module


## Important Files

### Additional Files

- [impl_default.rs](./impl_default.rs_docs.md)
- [conv.rs](./conv.rs_docs.md)
- [methods.rs](./methods.rs_docs.md)


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

- **Parent folder**: [src](../doc.md)
