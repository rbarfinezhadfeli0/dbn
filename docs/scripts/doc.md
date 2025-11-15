# Documentation for Folder: scripts

## Role in the Project

This folder contains **automation scripts** for:
- Building the project
- Running tests
- Formatting code
- Version management
- CI/CD integration


## Key Concepts

This folder contains supporting files and infrastructure.


## Important Files

### Additional Files

- [lint.sh](./lint.sh_docs.md)
- [get_version.sh](./get_version.sh_docs.md)
- [config.sh](./config.sh_docs.md)
- [format.sh](./format.sh_docs.md)
- [bump_version.sh](./bump_version.sh_docs.md)
- [regenerate_test_data.sh](./regenerate_test_data.sh_docs.md)
- [test.sh](./test.sh_docs.md)
- [build.sh](./build.sh_docs.md)


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
