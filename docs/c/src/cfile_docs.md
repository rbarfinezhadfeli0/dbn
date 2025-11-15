# cfile.rs

## File Metadata

- **Path:** `c/src/cfile.rs`
- **Type:** .rs
- **Lines:** 53
- **Characters:** 1,201
- **Words:** 126
- **Size:** text

## Original Source

```rust
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

## Overview

This file is part of the repository at `c/src`.

This is a Rust source file.

## Detailed Analysis

### Structs (1)

- `CFileRef`

### Functions (5)

- `new()`
- `bytes_written()`
- `as_ptr()`
- `write()`
- `flush()`

### Dependencies/Imports (1)

- `std::ptr::NonNull`

## Performance & Security Notes

- ⚠️ Contains `unsafe` code blocks - requires careful review

## Related Files

- Parent directory: `c/src/`
- See imported modules in Dependencies section above

## Testing

- Test file location: Not specified

