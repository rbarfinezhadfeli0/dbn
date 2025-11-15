# Documentation for Folder: python/python

## Role in the Project

This folder contains **Python bindings** for the DBN Rust library.

Using PyO3, it exposes DBN functionality to Python developers, enabling:
- Fast decoding of DBN files in Python
- Type-safe Python classes for market data records
- Integration with the Databento Python client library


## Key Concepts

This folder contains supporting files and infrastructure.


## Important Files

*No files in this folder*


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

- **Parent folder**: [python](../doc.md)
- **databento_dbn**: [View documentation](./databento_dbn/doc.md)
