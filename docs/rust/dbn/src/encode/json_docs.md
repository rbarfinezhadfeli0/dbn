# json.rs

## File Metadata

- **Path:** `rust/dbn/src/encode/json.rs`
- **Type:** .rs
- **Lines:** 10
- **Characters:** 255
- **Words:** 30
- **Size:** text

## Original Source

```rust
//! Encoding of DBN records into [JSON lines](https://jsonlines.org).

pub(crate) mod serialize;
mod sync;
pub use sync::{Encoder, EncoderBuilder};
#[cfg(feature = "async")]
mod r#async;
#[cfg(feature = "async")]
pub use r#async::Encoder as AsyncEncoder;

```

## Overview

This file is part of the repository at `rust/dbn/src/encode`.

This is a Rust source file.

## Detailed Analysis

### Dependencies/Imports (2)

- `r#async::Encoder`
- `sync::{Encoder,`

## Performance & Security Notes


## Related Files

- Parent directory: `rust/dbn/src/encode/`
- See imported modules in Dependencies section above

## Testing

- Test file location: Not specified

