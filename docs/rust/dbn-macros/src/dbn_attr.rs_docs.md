# Documentation: rust/dbn-macros/src/dbn_attr.rs

## File Metadata

**Path:** `rust/dbn-macros/src/dbn_attr.rs`
**Filename:** `dbn_attr.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../../rust/dbn-macros/src/dbn_attr.rs`

### Source Content

```rs
//! Common functionality for working with the `#[dbn(...)]` attribute
//! macros.

use std::collections::{HashSet, VecDeque};

use proc_macro2::Ident;
use syn::{parenthesized, spanned::Spanned, token, Field, FieldsNamed, Meta};

pub const C_CHAR_ATTR: &str = "c_char";
pub const FIXED_PRICE_ATTR: &str = "fixed_price";
pub const FMT_BINARY: &str = "fmt_binary";
pub const FMT_METHOD: &str = "fmt_method";
pub const INDEX_TS_ATTR: &str = "index_ts";
pub const SKIP_ATTR: &str = "skip";
pub const UNIX_NANOS_ATTR: &str = "unix_nanos";

/// Parses and sorts the fields of a DBN record according to the order specified with `dbn`
/// attributes.
pub fn get_sorted_fields(fields: FieldsNamed) -> syn::Result<VecDeque<Field>> {
    let mut fields: VecDeque<_> = fields.named.into_iter().collect();
    let mut encode_orders = HashSet::new();
    let mut encode_order_fields = Vec::new();
    for field in fields.iter() {
        if let Some(encode_order) = find_encode_order_attr(field)? {
            if !encode_orders.insert(encode_order) {
                // Already existed
                return Err(syn::Error::new_spanned(
                    field,
                    format!("Specified duplicate encode order `{encode_order}` for field"),
                ));
            }
            encode_order_fields.push((encode_order, field.clone()));
        }
    }
    encode_order_fields.sort_by_key(|field| field.0);
    for (encode_order, prioritized_field) in encode_order_fields {
        let idx = fields
            .iter()
            .position(|f| f.ident == prioritized_field.ident)
            .expect("to find field");
        fields.remove(idx).expect("to find field");
        if encode_order >= fields.len() {
            fields.push_back(prioritized_field);
        } else {
            fields.insert(encode_order, prioritized_field);
        }
    }
    Ok(fields)
}

/// Note this ignores encode_order, which can be extracted through [`find_encode_order_attr`].
pub fn find_dbn_attr_args(field: &Field) -> syn::Result<Vec<Ident>> {
    for attr in field.attrs.iter() {
        if let Meta::List(ref meta_list) = attr.meta {
            if meta_list.path.is_ident("dbn") {
                let mut args = Vec::new();
                // parse contents, e.g `unix_nanos` from `#[dbn(unix_nanos)]` or `#[dbn(unix_nanos, encode_order)]`
                meta_list.parse_nested_meta(|meta| {
                    // Ignore encode_order here
                    if meta.path.is_ident("encode_order") {
                        // Still need to parse (N) here to consume it
                        if meta.input.peek(token::Paren) {
                            let content;
                            parenthesized!(content in meta.input);
                            let _lit: syn::LitInt = content.parse()?;
                        }
                        Ok(())
                    } else if let Some(i) = meta.path.get_ident() {
                        if i == C_CHAR_ATTR
                            || i == FIXED_PRICE_ATTR
                            || i == FMT_BINARY
                            || i == FMT_METHOD
                            || i == INDEX_TS_ATTR
                            || i == SKIP_ATTR
                            || i == UNIX_NANOS_ATTR
                        {
                            args.push(i.clone());
                            Ok(())
                        } else {
                            Err(meta.error(format!("unrecognized dbn attr argument {i}")))
                        }
                    } else {
                        Err(meta.error("unrecognized dbn attr"))
                    }
                })?;
                return Ok(args);
            }
        }
    }
    Ok(vec![])
}

fn find_encode_order_attr(field: &Field) -> syn::Result<Option<usize>> {
    for attr in field.attrs.iter() {
        if let Meta::List(ref meta_list) = attr.meta {
            if meta_list.path.is_ident("dbn") {
                let mut encode_order = None;
                meta_list.parse_nested_meta(|meta| {
                    // #[dbn(encode_order)] or #[dbn(encode_order(1))]
                    if meta.path.is_ident("encode_order") {
                        if meta.input.peek(token::Paren) {
                            let content;
                            parenthesized!(content in meta.input);
                            let lit: syn::LitInt = content.parse()?;
                            let n: usize = lit.base10_parse()?;
                            encode_order = Some(n);
                        } else {
                            // defaults to 0
                            encode_order = Some(0)
                        }
                    }
                    Ok(())
                })?;
                return Ok(encode_order);
            }
        }
    }
    Ok(None)
}

pub fn is_hidden(field: &Field) -> bool {
    let ident = field.ident.as_ref().unwrap();
    ident.to_string().starts_with('_')
        || find_dbn_attr_args(field)
            .unwrap_or_default()
            .iter()
            .any(|id| id == SKIP_ATTR)
}

pub fn find_dbn_debug_attr(field: &Field) -> syn::Result<Option<Ident>> {
    let mut args: Vec<_> = find_dbn_attr_args(field)?
        .into_iter()
        .filter(|id| {
            id == C_CHAR_ATTR || id == FIXED_PRICE_ATTR || id == FMT_BINARY || id == FMT_METHOD
        })
        .collect();
    match args.len() {
        0 => Ok(None),
        1 => Ok(Some(args.pop().unwrap())),
        _ => Err(syn::Error::new(
            field.span(),
            "Passed incompatible format arguments to dbn attr",
        )),
    }
}

pub fn find_dbn_serialize_attr(field: &Field) -> syn::Result<Option<Ident>> {
    let mut args: Vec<_> = find_dbn_attr_args(field)?
        .into_iter()
        .filter(|id| id == C_CHAR_ATTR || id == FIXED_PRICE_ATTR || id == UNIX_NANOS_ATTR)
        .collect();
    match args.len() {
        0 => Ok(None),
        1 => Ok(Some(args.pop().unwrap())),
        _ => Err(syn::Error::new(
            field.span(),
            "Passed incompatible serialization arguments to dbn attr",
        )),
    }
}

#[cfg(test)]
mod tests {
    use quote::quote;
    use syn::FieldsNamed;

    use super::*;

    #[test]
    fn find_encode_order_attr_blank() {
        let input = quote!({
            pub b: bool,
        });
        let fields = syn::parse2::<FieldsNamed>(input).unwrap();
        assert_eq!(fields.named.len(), 1);
        assert!(find_encode_order_attr(fields.named.first().unwrap())
            .unwrap()
            .is_none());
    }

    #[test]
    fn find_encode_order_attr_none() {
        let input = quote!({
            #[dbn(c_char)]
            pub f: c_char,
        });
        let fields = syn::parse2::<FieldsNamed>(input).unwrap();
        assert_eq!(fields.named.len(), 1);
        assert!(find_encode_order_attr(fields.named.first().unwrap())
            .unwrap()
            .is_none());
    }

    #[test]
    fn find_encode_order_attr_only() {
        let input = quote!({
            #[dbn(encode_order(3))]
            pub b: bool,
        });
        let fields = syn::parse2::<FieldsNamed>(input).unwrap();
        assert_eq!(fields.named.len(), 1);
        assert_eq!(
            find_encode_order_attr(fields.named.first().unwrap())
                .unwrap()
                .unwrap(),
            3
        );
    }

    #[test]
    fn find_encode_order_attr_first() {
        let input = quote!({
            #[dbn(encode_order(2), unix_nanos)]
            pub ts: u64,
        });
        let fields = syn::parse2::<FieldsNamed>(input).unwrap();
        assert_eq!(fields.named.len(), 1);
        assert_eq!(
            find_encode_order_attr(fields.named.first().unwrap())
                .unwrap()
                .unwrap(),
            2
        );
    }

    #[test]
    fn find_encode_order_attr_last() {
        let input = quote!({
            #[dbn(unix_nanos, encode_order(4))]
            pub ts: u64,
        });
        let fields = syn::parse2::<FieldsNamed>(input).unwrap();
        assert_eq!(fields.named.len(), 1);
        assert_eq!(
            find_encode_order_attr(fields.named.first().unwrap())
                .unwrap()
                .unwrap(),
            4
        );
    }

    #[test]
    fn find_encode_order_attr_default() {
        let input = quote!({
            #[dbn(unix_nanos, encode_order)]
            pub ts: u64,
        });
        let fields = syn::parse2::<FieldsNamed>(input).unwrap();
        assert_eq!(fields.named.len(), 1);
        assert_eq!(
            find_encode_order_attr(fields.named.first().unwrap())
                .unwrap()
                .unwrap(),
            0
        );
    }
}

```

## High-Level Overview

This file is located at `rust/dbn-macros/src/dbn_attr.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** find_dbn_attr_args, find_dbn_debug_attr, find_dbn_serialize_attr, find_encode_order_attr, find_encode_order_attr_blank, find_encode_order_attr_default, find_encode_order_attr_first, find_encode_order_attr_last, find_encode_order_attr_none, find_encode_order_attr_only, get_sorted_fields, is_hidden

**Dependencies:** This file imports from 6 modules


#### Detailed Walkthrough


##### Function: `get_sorted_fields`

```rust
pub fn get_sorted_fields(fields: FieldsNamed) -> syn::Result<VecDeque<Field>> {
```


##### Function: `find_dbn_attr_args`

```rust
pub fn find_dbn_attr_args(field: &Field) -> syn::Result<Vec<Ident>> {
```


##### Function: `find_encode_order_attr`

```rust
fn find_encode_order_attr(field: &Field) -> syn::Result<Option<usize>> {
```


##### Function: `is_hidden`

```rust
pub fn is_hidden(field: &Field) -> bool {
```


##### Function: `find_dbn_debug_attr`

```rust
pub fn find_dbn_debug_attr(field: &Field) -> syn::Result<Option<Ident>> {
```


##### Function: `find_dbn_serialize_attr`

```rust
pub fn find_dbn_serialize_attr(field: &Field) -> syn::Result<Option<Ident>> {
```


##### Function: `find_encode_order_attr_blank`

```rust
fn find_encode_order_attr_blank() {
```


##### Function: `find_encode_order_attr_none`

```rust
fn find_encode_order_attr_none() {
```


##### Function: `find_encode_order_attr_only`

```rust
fn find_encode_order_attr_only() {
```


##### Function: `find_encode_order_attr_first`

```rust
fn find_encode_order_attr_first() {
```


*... and more functions (see source code)*


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

