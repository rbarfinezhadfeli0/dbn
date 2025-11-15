# Documentation Repository

This directory contains comprehensive auto-generated documentation for the entire dbn repository.

**Generated:** 2025-11-15T12:51:04.027122
**Generator Version:** 1.0.0
**Files Documented:** 202
**Documentation Files:** 424

## Structure

- **manifest.json** - Complete metadata, checksums, and statistics
- **index.md** - Root index with links to all documentation
- **keywords.md** - Global A-Z keyword index
- **comprehensive_book.md** - Complete documentation in book format
- **verification_report.md** - Validation and error report
- **README.md** - This file

### Per-File Documentation

For each source file `path/to/file.ext`, you will find:
- `docs/path/to/file_docs.md` - Complete documentation
- `docs/path/to/file_kw.md` - Keyword index

### Per-Folder Documentation

For each directory `path/to/dir/`, you will find:
- `docs/path/to/dir/index.md` - Directory index
- `docs/path/to/dir/doc.md` - Narrative documentation
- `docs/path/to/dir/sub.md` - Merged keyword index

## Usage

1. **Browse by Topic**: Start with [index.md](./index.md)
2. **Search Keywords**: Use [keywords.md](./keywords.md)
3. **Read Sequentially**: Open [comprehensive_book.md](./comprehensive_book.md)
4. **Verify Quality**: Check [verification_report.md](./verification_report.md)

## Resumability

To regenerate or update documentation:

```bash
python3 generate_docs.py
```

The generator is idempotent - running it multiple times produces the same output for the same repository state.

## Statistics

- **Total Repository Files:** 202
- **Documentation Files Created:** 424
- **Estimated Words:** 122,795
- **Bytes Written:** 2,340,804

## Verification

All generated files are checksummed (SHA-256) and recorded in manifest.json. All internal links use relative paths and are validated.
