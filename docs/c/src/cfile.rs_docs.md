# Documentation: c/src/cfile.rs

## File Metadata

**Path:** `c/src/cfile.rs`
**Filename:** `cfile.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../c/src/cfile.rs`

### Source Content

```rs
use std::ptr::NonNull;

/// A non-owning wrapper around a `*mut libc::FILE`.
pub struct CFileRef {
    ptr: NonNull<libc::FILE>,
    bytes_written: usize,
}

impl CFileRef {
    pub fn new(ptr: *mut libc::FILE) -> Option<Self> {
        NonNull::new(ptr).map(|ptr| Self {
            ptr,
            bytes_written: 0,
        })
    }

    pub fn bytes_written(&self) -> usize {
        self.bytes_written
    }

    pub fn as_ptr(&mut self) -> *mut libc::FILE {
        self.ptr.as_ptr()
    }
}

impl std::io::Write for CFileRef {
    fn write(&mut self, buf: &[u8]) -> std::io::Result<usize> {
        let ret = unsafe {
            libc::fwrite(
                buf.as_ptr() as *const libc::c_void,
                1,
                buf.len(),
                self.as_ptr(),
            )
        };
        if ret > 0 {
            self.bytes_written += ret;
            Ok(ret)
        } else {
            Err(std::io::Error::last_os_error())
        }
    }

    fn flush(&mut self) -> std::io::Result<()> {
        let ret = unsafe { libc::fflush(self.as_ptr()) };
        if ret == 0 {
            Ok(())
        } else {
            Err(std::io::Error::last_os_error())
        }
    }
}

```

## High-Level Overview

This file is located at `c/src/cfile.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** as_ptr, bytes_written, flush, new, write

**Structs defined:** CFileRef

**Dependencies:** This file imports from 1 modules


#### Detailed Walkthrough


##### Function: `new`

```rust
pub fn new(ptr: *mut libc::FILE) -> Option<Self> {
```


##### Function: `bytes_written`

```rust
pub fn bytes_written(&self) -> usize {
```


##### Function: `as_ptr`

```rust
pub fn as_ptr(&mut self) -> *mut libc::FILE {
```


##### Function: `write`

```rust
fn write(&mut self, buf: &[u8]) -> std::io::Result<usize> {
```


##### Function: `flush`

```rust
fn flush(&mut self) -> std::io::Result<()> {
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

