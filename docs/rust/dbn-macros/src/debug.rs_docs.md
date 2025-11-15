# Documentation: rust/dbn-macros/src/debug.rs

## File Metadata

**Path:** `rust/dbn-macros/src/debug.rs`
**Filename:** `debug.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../../rust/dbn-macros/src/debug.rs`

### Source Content

```rs
use proc_macro2::TokenStream;
use quote::quote;
use syn::{parse_macro_input, Field, ItemStruct};

use crate::{
    dbn_attr::{
        find_dbn_debug_attr, is_hidden, C_CHAR_ATTR, FIXED_PRICE_ATTR, FMT_BINARY, FMT_METHOD,
    },
    utils::crate_name,
};

pub fn record_debug_impl(input_struct: &ItemStruct) -> TokenStream {
    let record_type = &input_struct.ident;
    let field_iter = input_struct
        .fields
        .iter()
        .map(|f| format_field(f).unwrap_or_else(|e| e.into_compile_error()));
    quote! {
        impl ::std::fmt::Debug for #record_type {
            fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                let mut debug_struct = f.debug_struct(stringify!(#record_type));
                #(#field_iter)*
                debug_struct.finish()
            }
        }
    }
}

pub fn derive_impl(input: proc_macro::TokenStream) -> proc_macro::TokenStream {
    // let DeriveInput { ident, data, .. } = parse_macro_input!(input as DeriveInput);
    let input_struct = parse_macro_input!(input as ItemStruct);
    let record_type = &input_struct.ident;
    let field_iter = input_struct
        .fields
        .iter()
        .map(|f| format_field(f).unwrap_or_else(|e| e.into_compile_error()));
    quote! {
        impl ::std::fmt::Debug for #record_type {
            fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                let mut debug_struct = f.debug_struct(stringify!(#record_type));
                #(#field_iter)*
                debug_struct.finish()
            }
        }
    }
    .into()
}

fn format_field(field: &Field) -> syn::Result<TokenStream> {
    let ident = field.ident.as_ref().unwrap();
    if is_hidden(field) {
        return Ok(quote!());
    }
    Ok(match find_dbn_debug_attr(field)? {
        Some(id) if id == C_CHAR_ATTR => {
            quote! { debug_struct.field(stringify!(#ident), &(self.#ident as u8 as char)); }
        }
        Some(id) if id == FIXED_PRICE_ATTR => {
            let crate_name = crate_name();
            quote! { debug_struct.field(stringify!(#ident), &#crate_name::pretty::Px(self.#ident)); }
        }
        Some(id) if id == FMT_BINARY => {
            // format as `0b00101010`
            quote! { debug_struct.field(stringify!(#ident), &format_args!("{:#010b}", &self.#ident)); }
        }
        Some(id) if id == FMT_METHOD => {
            // Try to use method to format, otherwise fallback on raw value
            return Ok(quote! {
                match self.#ident() {
                    Ok(s) => debug_struct.field(stringify!(#ident), &s),
                    Err(_) => debug_struct.field(stringify!(#ident), &self.#ident),
                };
            });
        }
        _ => quote! { debug_struct.field(stringify!(#ident), &self.#ident); },
    })
}

```

## High-Level Overview

This file is located at `rust/dbn-macros/src/debug.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** derive_impl, fmt, format_field, record_debug_impl

**Dependencies:** This file imports from 5 modules


#### Detailed Walkthrough


##### Function: `record_debug_impl`

```rust
pub fn record_debug_impl(input_struct: &ItemStruct) -> TokenStream {
```


##### Function: `fmt`

```rust
fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
```


##### Function: `derive_impl`

```rust
pub fn derive_impl(input: proc_macro::TokenStream) -> proc_macro::TokenStream {
```


##### Function: `fmt`

```rust
fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
```


##### Function: `format_field`

```rust
fn format_field(field: &Field) -> syn::Result<TokenStream> {
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

