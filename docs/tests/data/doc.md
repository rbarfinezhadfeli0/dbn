# Documentation for Folder: tests/data

## Role in the Project

This folder contains **test infrastructure** including:
- Integration tests
- Test data files
- Test utilities
- Validation suites

These tests ensure correctness and compatibility across different DBN versions and schemas.


## Key Concepts

This folder contains supporting files and infrastructure.


## Important Files

### Additional Files

- [test_data.ohlcv-1d.dbn](./test_data.ohlcv-1d.dbn_docs.md)
- [test_data.bbo-1s.dbn.zst](./test_data.bbo-1s.dbn.zst_docs.md)
- [test_data.ohlcv-1m.dbz](./test_data.ohlcv-1m.dbz_docs.md)
- [test_data.mbo.dbz](./test_data.mbo.dbz_docs.md)
- [test_data.trades.v1.dbn](./test_data.trades.v1.dbn_docs.md)
- [test_data.cbbo-1s.dbn.zst](./test_data.cbbo-1s.dbn.zst_docs.md)
- [test_data.ohlcv-1d.v1.dbn](./test_data.ohlcv-1d.v1.dbn_docs.md)
- [test_data.ohlcv-1d.dbz](./test_data.ohlcv-1d.dbz_docs.md)
- [test_data.mbp-10.dbn](./test_data.mbp-10.dbn_docs.md)
- [test_data.mbp-1.dbn.zst](./test_data.mbp-1.dbn.zst_docs.md)

*... and 63 more files (see [index](./index.md))*


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

- **Parent folder**: [tests](../doc.md)
