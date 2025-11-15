# Documentation for Folder: rust/dbn-cli/tests

## Role in the Project

This folder contains **test infrastructure** including:
- Integration tests
- Test data files
- Test utilities
- Validation suites

These tests ensure correctness and compatibility across different DBN versions and schemas.


## Key Concepts

Key technical concepts in this folder:

- **PRETTY_PX_REGEX**: Core concept used throughout this module
- **PRETTY_TS_REGEX**: Core concept used throughout this module
- **TEST_DATA_PATH**: Core concept used throughout this module
- **bad_infer**: Core concept used throughout this module
- **broken_pipe_is_silent**: Core concept used throughout this module
- **cant_specify_json_and_csv**: Core concept used throughout this module
- **cmd**: Core concept used throughout this module
- **convert_dbz_to_dbn**: Core concept used throughout this module
- **empty**: Core concept used throughout this module
- **encoding_overrides_extension**: Core concept used throughout this module
- **force_overwrite**: Core concept used throughout this module
- **force_truncates_file**: Core concept used throughout this module
- **fragment_conflicts_with_dbn_output**: Core concept used throughout this module
- **fragment_conflicts_with_metadata**: Core concept used throughout this module
- **help**: Core concept used throughout this module


## Important Files

### Additional Files

- [integration_tests.rs](./integration_tests.rs_docs.md)


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

- **Parent folder**: [dbn-cli](../doc.md)
