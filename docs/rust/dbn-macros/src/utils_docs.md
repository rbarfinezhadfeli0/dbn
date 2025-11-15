# utils.rs

## File Metadata

- **Path:** `rust/dbn-macros/src/utils.rs`
- **Type:** .rs
- **Lines:** 14
- **Characters:** 409
- **Words:** 37
- **Size:** text

## Original Source

```rust
use proc_macro2::{Ident, Span, TokenStream};
use proc_macro_crate::FoundCrate;
use quote::quote;

pub fn crate_name() -> TokenStream {
    match proc_macro_crate::crate_name("dbn").expect("dbn crate in Cargo.toml") {
        FoundCrate::Itself => quote!(crate),
        FoundCrate::Name(name) => {
            let ident = Ident::new(&name, Span::call_site());
            quote!( ::#ident )
        }
    }
}

```

## Overview

This file is part of the repository at `rust/dbn-macros/src`.

This is a Rust source file.

## Detailed Analysis

### Functions (1)

- `crate_name()`

### Dependencies/Imports (3)

- `proc_macro2::{Ident,`
- `proc_macro_crate::FoundCrate`
- `quote::quote`

## Performance & Security Notes

- 🔐 May contain security-sensitive code (passwords/keys/tokens)

## Related Files

- Parent directory: `rust/dbn-macros/src/`
- See imported modules in Dependencies section above

## Testing

- Test file location: Not specified

