# Documentation: rust/dbn/src/decode/stream.rs

## File Metadata

**Path:** `rust/dbn/src/decode/stream.rs`
**Filename:** `stream.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../../../rust/dbn/src/decode/stream.rs`

### Source Content

```rs
use std::marker::PhantomData;

use fallible_streaming_iterator::FallibleStreamingIterator;

use super::{DbnMetadata, DecodeStream};
use crate::{Error, HasRType, Result};

/// A consuming iterator wrapping a [`DecodeRecord`](super::DecodeRecord). Lazily
/// decodes the contents of the file or other input stream.
///
/// Implements [`FallibleStreamingIterator`].
pub struct StreamIterDecoder<D, T> {
    /// The underlying decoder implementation.
    decoder: D,
    /// Number of element sthat have been decoded. Used for [`Iterator::size_hint()`].
    /// `None` indicates the end of the stream has been reached.
    i: Option<usize>,
    /// Required to associate this type with a specific record type `T`.
    _marker: PhantomData<T>,
}

impl<D, T> StreamIterDecoder<D, T>
where
    T: HasRType,
{
    /// Creates a new streaming decoder using the given `decoder`.
    pub fn new(decoder: D) -> Self {
        Self {
            decoder,
            i: Some(0),
            _marker: PhantomData,
        }
    }

    /// Returns an immutable reference to the inner decoder.
    pub fn get_ref(&self) -> &D {
        &self.decoder
    }
}

impl<D, T> FallibleStreamingIterator for StreamIterDecoder<D, T>
where
    D: DecodeStream,
    T: HasRType,
{
    type Error = Error;
    type Item = T;

    fn advance(&mut self) -> Result<()> {
        if let Some(i) = self.i.as_mut() {
            match self.decoder.decode_record::<T>() {
                Ok(Some(_)) => {
                    *i += 1;
                    Ok(())
                }
                Ok(None) => {
                    // set error state sentinel
                    self.i = None;
                    Ok(())
                }
                Err(err) => {
                    // set error state sentinel
                    self.i = None;
                    Err(err)
                }
            }
        } else {
            Ok(())
        }
    }

    fn get(&self) -> Option<&Self::Item> {
        if self.i.is_some() {
            // SAFETY: Validated record type in `advance` with call to `decode_record`.
            Some(unsafe { self.decoder.record_ref().get_unchecked() })
        } else {
            None
        }
    }
}

impl<D, T> DbnMetadata for StreamIterDecoder<D, T>
where
    D: DbnMetadata,
{
    fn metadata(&self) -> &crate::Metadata {
        self.decoder.metadata()
    }

    fn metadata_mut(&mut self) -> &mut crate::Metadata {
        self.decoder.metadata_mut()
    }
}

```

## High-Level Overview

This file is located at `rust/dbn/src/decode/stream.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** advance, get, get_ref, metadata, metadata_mut, new

**Structs defined:** StreamIterDecoder

**Dependencies:** This file imports from 4 modules


#### Detailed Walkthrough


##### Function: `new`

```rust
pub fn new(decoder: D) -> Self {
```


##### Function: `get_ref`

```rust
pub fn get_ref(&self) -> &D {
```


##### Function: `advance`

```rust
fn advance(&mut self) -> Result<()> {
```


##### Function: `get`

```rust
fn get(&self) -> Option<&Self::Item> {
```


##### Function: `metadata`

```rust
fn metadata(&self) -> &crate::Metadata {
```


##### Function: `metadata_mut`

```rust
fn metadata_mut(&mut self) -> &mut crate::Metadata {
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

