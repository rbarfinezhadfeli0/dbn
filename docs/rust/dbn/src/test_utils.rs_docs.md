# Documentation: rust/dbn/src/test_utils.rs

## File Metadata

**Path:** `rust/dbn/src/test_utils.rs`
**Filename:** `test_utils.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../../rust/dbn/src/test_utils.rs`

### Source Content

```rs
use fallible_streaming_iterator::FallibleStreamingIterator;

use crate::{
    decode::{private::BufferSlice, DecodeRecordRef},
    Error, HasRType, RecordRef,
};

/// A testing shim to get a streaming iterator from a [`Vec`].
pub struct VecStream<T> {
    vec: Vec<T>,
    idx: isize,
}

impl<T> VecStream<T> {
    pub fn new(vec: Vec<T>) -> Self {
        // initialize at -1 because `advance()` is always called before
        // `get()`.
        Self { vec, idx: -1 }
    }
}

impl<T> FallibleStreamingIterator for VecStream<T> {
    type Item = T;
    type Error = Error;

    fn advance(&mut self) -> Result<(), Error> {
        self.idx += 1;
        Ok(())
    }

    fn get(&self) -> Option<&Self::Item> {
        self.vec.get(self.idx as usize)
    }
}

impl<T> DecodeRecordRef for VecStream<T>
where
    T: HasRType,
{
    fn decode_record_ref(&mut self) -> crate::Result<Option<crate::RecordRef>> {
        self.idx += 1;
        let Some(rec) = self.vec.get(self.idx as usize) else {
            return Ok(None);
        };
        Ok(Some(RecordRef::from(rec)))
    }
}

impl<T> BufferSlice for VecStream<T>
where
    T: HasRType + AsRef<[u8]>,
{
    fn buffer_slice(&self) -> &[u8] {
        self.vec
            .get(self.idx as usize)
            .map(|r| r.as_ref())
            .unwrap_or_default()
    }

    fn compat_buffer_slice(&self) -> &[u8] {
        &[]
    }

    fn record_ref(&self) -> RecordRef {
        RecordRef::from(self.vec.get(self.idx as usize).unwrap())
    }
}

```

## High-Level Overview

This file is located at `rust/dbn/src/test_utils.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** advance, buffer_slice, compat_buffer_slice, decode_record_ref, get, new, record_ref

**Structs defined:** VecStream

**Dependencies:** This file imports from 3 modules


#### Detailed Walkthrough


##### Function: `new`

```rust
pub fn new(vec: Vec<T>) -> Self {
```


##### Function: `advance`

```rust
fn advance(&mut self) -> Result<(), Error> {
```


##### Function: `get`

```rust
fn get(&self) -> Option<&Self::Item> {
```


##### Function: `decode_record_ref`

```rust
fn decode_record_ref(&mut self) -> crate::Result<Option<crate::RecordRef>> {
```


##### Function: `buffer_slice`

```rust
fn buffer_slice(&self) -> &[u8] {
```


##### Function: `compat_buffer_slice`

```rust
fn compat_buffer_slice(&self) -> &[u8] {
```


##### Function: `record_ref`

```rust
fn record_ref(&self) -> RecordRef {
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

