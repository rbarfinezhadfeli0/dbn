# dbn.rs

## File Metadata

- **Path:** `rust/dbn/src/encode/dbn.rs`
- **Type:** .rs
- **Lines:** 12
- **Characters:** 330
- **Words:** 37
- **Size:** text

## Original Source

```rust
//! Encoding DBN records into DBN, Zstandard-compressed or not.
mod sync;
pub use sync::{Encoder, MetadataEncoder, RecordEncoder};

#[cfg(feature = "async")]
mod r#async;
#[cfg(feature = "async")]
pub use r#async::{
    Encoder as AsyncEncoder, MetadataEncoder as AsyncMetadataEncoder,
    RecordEncoder as AsyncRecordEncoder,
};

```

## Overview

This file is part of the repository at `rust/dbn/src/encode`.

This is a Rust source file.

## Detailed Analysis

### Dependencies/Imports (2)

- `r#async::{`
- `sync::{Encoder,`

## Performance & Security Notes


## Related Files

- Parent directory: `rust/dbn/src/encode/`
- See imported modules in Dependencies section above

## Testing

- Test file location: Not specified

