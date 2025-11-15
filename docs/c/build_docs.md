# build.rs

## File Metadata

- **Path:** `c/build.rs`
- **Type:** .rs
- **Lines:** 37
- **Characters:** 1,189
- **Words:** 102
- **Size:** text

## Original Source

```rust
//! Writes generated C header for DBN functions and symbols to
//! ${target_directory}/include/dbn/dbn.h

extern crate cbindgen;

use std::{env, ffi::OsStr, fs, path::PathBuf};

fn find_target_dir() -> PathBuf {
    if let Some(target_dir) = env::var_os("CARGO_TARGET_DIR") {
        return PathBuf::from(target_dir);
    }
    let mut dir = PathBuf::from(env::var_os("OUT_DIR").unwrap());
    loop {
        if dir.file_name() == Some(OsStr::new("target"))
            // Want to find the top directory containing a CACHEDIR.TAG file
            || (dir.join("CACHEDIR.TAG").exists()
                && !dir
                    .parent().is_none_or(|p| p.join("CACHEDIR.TAG").exists()))
        {
            return dir;
        }
        assert!(dir.pop(), "Unable to determine target dir");
    }
}

fn main() {
    let crate_dir = env::var("CARGO_MANIFEST_DIR").unwrap();
    let target_dir = find_target_dir();
    let include_dir = target_dir.join("include").join("dbn");
    fs::create_dir_all(&include_dir).unwrap();
    let out_path = include_dir.join("dbn.h");

    cbindgen::generate(crate_dir)
        .expect("Unable to generate bindings")
        .write_to_file(out_path);
}

```

## Overview

This file is part of the repository at `c`.

This is a Rust source file.

## Detailed Analysis

### Functions (2)

- `find_target_dir()`
- `main()`

### Dependencies/Imports (1)

- `std::{env,`

## Performance & Security Notes

- ⚠️ Uses `unwrap()` - may panic if expectations are not met

## Related Files

- Parent directory: `c/`
- See imported modules in Dependencies section above

## Testing

- Test file location: Not specified

