# dbn.rs

## File Metadata

- **Path:** `rust/dbn/src/decode/dbn.rs`
- **Type:** .rs
- **Lines:** 21
- **Characters:** 607
- **Words:** 71
- **Size:** text

## Original Source

```rust
//! Decoding of DBN files.
const DBN_PREFIX: &[u8] = b"DBN";
const DBN_PREFIX_LEN: usize = DBN_PREFIX.len();

/// Returns `true` if `bytes` starts with valid uncompressed DBN.
pub fn starts_with_prefix(bytes: &[u8]) -> bool {
    bytes.len() > DBN_PREFIX_LEN && &bytes[..DBN_PREFIX_LEN] == DBN_PREFIX
}

mod sync;
pub(crate) use sync::decode_iso8601;
pub use sync::{Decoder, MetadataDecoder, RecordDecoder};

#[cfg(feature = "async")]
mod r#async;
#[cfg(feature = "async")]
pub use r#async::{
    Decoder as AsyncDecoder, MetadataDecoder as AsyncMetadataDecoder,
    RecordDecoder as AsyncRecordDecoder,
};

```

## Overview

This file is part of the repository at `rust/dbn/src/decode`.

This is a Rust source file.

## Detailed Analysis

### Functions (1)

- `starts_with_prefix()`

### Dependencies/Imports (3)

- `r#async::{`
- `sync::decode_iso8601`
- `sync::{Decoder,`

## Performance & Security Notes


## Related Files

- Parent directory: `rust/dbn/src/decode/`
- See imported modules in Dependencies section above

## Testing

- Test file location: Not specified

