# Documentation: c/src/decode.rs

## File Metadata

**Path:** `c/src/decode.rs`
**Filename:** `decode.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../c/src/decode.rs`

### Source Content

```rs
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

## High-Level Overview

This file is located at `c/src/decode.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** DbnDecoder_create, DbnDecoder_decode, DbnDecoder_free, DbnDecoder_metadata

**Dependencies:** This file imports from 2 modules


#### Detailed Walkthrough


##### Function: `DbnDecoder_create`

```rust
fn DbnDecoder_create(file: RawFd, compression: Compression) -> *mut Decoder {
```


##### Function: `DbnDecoder_metadata`

```rust
fn DbnDecoder_metadata(decoder: *mut Decoder) -> *const Metadata {
```


##### Function: `DbnDecoder_decode`

```rust
fn DbnDecoder_decode(decoder: *mut Decoder) -> *const RecordHeader {
```


##### Function: `DbnDecoder_free`

```rust
fn DbnDecoder_free(decoder: *mut Decoder) {
```



#### Architecture & Design

This file contributes to the overall DBN library architecture by providing essential functionality
for encoding, decoding, or representing market data in the Databento Binary Encoding format.

**Design Principles:**
- Type safety through Rust's strong type system
- Zero-cost abstractions for performance
- Clear error handling with Result types
- Memory efficiency for large-scale data processing

#### Performance Considerations

Rust's ownership model and zero-cost abstractions make this implementation highly performant:
- Stack allocation where possible
- Minimal heap allocations
- Compile-time optimizations
- No garbage collection overhead

#### Security & Safety

Rust's memory safety guarantees prevent:
- Buffer overflows
- Null pointer dereferences
- Data races in concurrent code
- Use-after-free bugs

All unsafe code blocks (if any) are carefully reviewed and documented.

