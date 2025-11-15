# decode.rs

## File Metadata

- **Path:** `c/src/decode.rs`
- **Type:** .rs
- **Lines:** 73
- **Characters:** 1,876
- **Words:** 230
- **Size:** text

## Original Source

```rust
// RawFd isn't defined for windows
#![cfg(not(target_os = "windows"))]

use std::{
    fs::File,
    io::BufReader,
    os::fd::{FromRawFd, RawFd},
    ptr::{null, null_mut},
};

use dbn::{
    decode::{DbnMetadata, DecodeRecordRef, DynDecoder},
    Compression, Metadata, Record, RecordHeader, VersionUpgradePolicy,
};

pub type Decoder = DynDecoder<'static, BufReader<File>>;

/// Creates a DBN decoder. Returns null in case of error.
///
/// # Safety
/// `file` must be a valid file descriptor. This function assumes ownership of `file`.
#[no_mangle]
pub unsafe extern "C" fn DbnDecoder_create(file: RawFd, compression: Compression) -> *mut Decoder {
    let decoder = match DynDecoder::new(
        File::from_raw_fd(file),
        compression,
        VersionUpgradePolicy::AsIs,
    ) {
        Ok(d) => d,
        Err(_) => {
            return null_mut();
        }
    };
    Box::into_raw(Box::new(decoder))
}

/// Returns a pointer to the decoded DBN metadata.
///
/// # Safety
/// Verifies `decoder` is not null.
#[no_mangle]
pub unsafe extern "C" fn DbnDecoder_metadata(decoder: *mut Decoder) -> *const Metadata {
    if let Some(metadata) = decoder.as_mut().map(|d| d.metadata()) {
        metadata
    } else {
        null()
    }
}

/// Decodes and returns a pointer to the next record.
///
/// # Safety
/// Verifies `decoder` is not null.
#[no_mangle]
pub unsafe extern "C" fn DbnDecoder_decode(decoder: *mut Decoder) -> *const RecordHeader {
    if let Some(Ok(Some(rec))) = decoder.as_mut().map(|d| d.decode_record_ref()) {
        rec.header()
    } else {
        null()
    }
}

/// Frees memory associated with the DBN decoder.
///
/// # Safety
/// Verifies `decoder` is not null.
#[no_mangle]
pub unsafe extern "C" fn DbnDecoder_free(decoder: *mut Decoder) {
    if let Some(decoder) = decoder.as_mut() {
        drop(Box::from_raw(decoder));
    }
}

```

## Overview

This file is part of the repository at `c/src`.

This is a Rust source file.

## Detailed Analysis

### Functions (4)

- `DbnDecoder_create()`
- `DbnDecoder_metadata()`
- `DbnDecoder_decode()`
- `DbnDecoder_free()`

### Dependencies/Imports (2)

- `dbn::{`
- `std::{`

## Performance & Security Notes

- ⚠️ Contains `unsafe` code blocks - requires careful review

## Related Files

- Parent directory: `c/src/`
- See imported modules in Dependencies section above

## Testing

- Test file location: Not specified

