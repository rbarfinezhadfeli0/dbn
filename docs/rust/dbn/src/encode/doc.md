# Documentation for Folder: rust/dbn/src/encode

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

- **DynBufWriter**: Core concept used throughout this module
- **DynBufWriterImpl**: Core concept used throughout this module
- **DynEncoder**: Core concept used throughout this module
- **DynEncoderBuilder**: Core concept used throughout this module
- **DynEncoderImpl**: Core concept used throughout this module
- **DynWriter**: Core concept used throughout this module
- **DynWriterImpl**: Core concept used throughout this module
- **FallibleStreamingIterator**: Core concept used throughout this module
- **all_pretty**: Core concept used throughout this module
- **build**: Core concept used throughout this module
- **builder**: Core concept used throughout this module
- **delimiter**: Core concept used throughout this module
- **encode_decoded**: Core concept used throughout this module
- **encode_header**: Core concept used throughout this module
- **encode_header_for_schema**: Core concept used throughout this module


## Important Files

### Additional Files

- [dyn_encoder.rs](./dyn_encoder.rs_docs.md)
- [csv.rs](./csv.rs_docs.md)
- [json.rs](./json.rs_docs.md)
- [dbn.rs](./dbn.rs_docs.md)
- [dyn_writer.rs](./dyn_writer.rs_docs.md)


## Data Flows & Interactions

This folder handles **encoding** operations:
- Converts market data records to various output formats
- Supports DBN, CSV, JSON encodings
- Provides both sync and async APIs
- Interacts with record types defined in parent modules


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
- **dbn**: [View documentation](./dbn/doc.md)
- **json**: [View documentation](./json/doc.md)
- **csv**: [View documentation](./csv/doc.md)
