# Documentation for Folder: rust/dbn/src/metadata

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

- **IntervalOrdering**: Core concept used throughout this module
- **MappingInterval**: Core concept used throughout this module
- **MetadataMerger**: Core concept used throughout this module
- **finalize**: Core concept used throughout this module
- **mapping_interval**: Core concept used throughout this module
- **mapping_interval_ordering**: Core concept used throughout this module
- **mapping_interval_ordering_diff_symbol**: Core concept used throughout this module
- **merge**: Core concept used throughout this module
- **merge_intervals**: Core concept used throughout this module
- **new**: Core concept used throughout this module
- **ordering**: Core concept used throughout this module
- **test_merge**: Core concept used throughout this module


## Important Files

### Additional Files

- [merge.rs](./merge.rs_docs.md)


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
