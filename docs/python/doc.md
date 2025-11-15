# Documentation for Folder: python

## Role in the Project

This folder contains **Python bindings** for the DBN Rust library.

Using PyO3, it exposes DBN functionality to Python developers, enabling:
- Fast decoding of DBN files in Python
- Type-safe Python classes for market data records
- Integration with the Databento Python client library


## Key Concepts

Key technical concepts in this folder:

- **Building**: Core concept used throughout this module
- **Installation**: Core concept used throughout this module
- **License**: Core concept used throughout this module
- **Usage**: Core concept used throughout this module
- **databento**: Core concept used throughout this module
- **documentation**: Core concept used throughout this module
- **main**: Core concept used throughout this module


## Important Files

### Essential Files

- **[Cargo.toml](./Cargo.toml_docs.md)**: Rust package configuration
- **[README.md](./README.md_docs.md)**: Project documentation

### Additional Files

- [build.rs](./build.rs_docs.md)
- [pyproject.toml](./pyproject.toml_docs.md)


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

- **Parent folder**: [root](../doc.md)
- **python**: [View documentation](./python/doc.md)
- **src**: [View documentation](./src/doc.md)
