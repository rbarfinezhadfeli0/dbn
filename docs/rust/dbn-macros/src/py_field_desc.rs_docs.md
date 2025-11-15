# Documentation: rust/dbn-macros/src/py_field_desc.rs

## File Metadata

**Path:** `rust/dbn-macros/src/py_field_desc.rs`
**Filename:** `py_field_desc.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../../rust/dbn-macros/src/py_field_desc.rs`

### Source Content

```rs
use std::collections::VecDeque;

use proc_macro2::TokenStream;
use quote::quote;
use syn::{parse_macro_input, Data, DeriveInput, Field};

use crate::dbn_attr::{
    find_dbn_serialize_attr, get_sorted_fields, is_hidden, C_CHAR_ATTR, FIXED_PRICE_ATTR,
    UNIX_NANOS_ATTR,
};

pub fn derive_impl(input: proc_macro::TokenStream) -> proc_macro::TokenStream {
    let DeriveInput { ident, data, .. } = parse_macro_input!(input as DeriveInput);
    let Data::Struct(data_struct) = data else {
        return syn::Error::new(ident.span(), "Can only derive PyFieldDesc for structs")
            .into_compile_error()
            .into();
    };
    let syn::Fields::Named(fields) = data_struct.fields else {
        return syn::Error::new(ident.span(), "Cannot derive PyFieldDesc for tuple struct")
            .into_compile_error()
            .into();
    };
    let sorted_fields = match get_sorted_fields(fields.clone()) {
        Ok(fields) => fields,
        Err(ts) => {
            return ts.into_compile_error().into();
        }
    };
    let raw_fields: VecDeque<_> = fields.named.into_iter().collect();
    let dtype_iter = raw_fields.iter().map(|f| {
        let ident = f.ident.as_ref().unwrap();
        let f_type = &f.ty;

        match find_dbn_serialize_attr(f) {
            Ok(attr) => {
                if matches!(attr, Some(id) if id == C_CHAR_ATTR) {
                    quote! {
                        res.push((
                            stringify!(#ident).to_owned(),
                            "S1".to_owned(),
                        ));
                    }
                } else {
                    quote! { res.extend(<#f_type>::field_dtypes(stringify!(#ident))); }
                }
            }
            Err(e) => e.into_compile_error(),
        }
    });
    let price_fields = fields_with_attr(&raw_fields, FIXED_PRICE_ATTR, quote!(price_fields));
    let hidden_fields = hidden_fields(&raw_fields);
    let timestamp_fields = fields_with_attr(&raw_fields, UNIX_NANOS_ATTR, quote!(timestamp_fields));
    let ordered_fields = sorted_fields.iter().filter(|f| !is_hidden(f)).map(|f| {
        let ident = f.ident.as_ref().unwrap();
        let f_type = &f.ty;
        quote! {
            res.extend(<#f_type>::ordered_fields(stringify!(#ident)));
        }
    });

    quote! {
        impl crate::python::PyFieldDesc for #ident {
            fn field_dtypes(_field_name: &str) -> Vec<(String, String)> {
                let mut res =  Vec::new();
                #(#dtype_iter)*
                res
            }
            fn price_fields(_field_name: &str) -> Vec<String> {
                let mut res =  Vec::new();
                #price_fields
                res
            }
            fn hidden_fields(_field_name: &str) -> Vec<String> {
                let mut res =  Vec::new();
                #hidden_fields
                res
            }
            fn timestamp_fields(_field_name: &str) -> Vec<String> {
                let mut res =  Vec::new();
                #timestamp_fields
                res
            }
            fn ordered_fields(_field_name: &str) -> Vec<String> {
                let mut res =  Vec::new();
                #(#ordered_fields)*
                res
            }
        }
    }
    .into()
}

fn fields_with_attr(fields: &VecDeque<Field>, attr: &str, method: TokenStream) -> TokenStream {
    let fields_iter = fields.iter().map(|f| {
        let ident = f.ident.as_ref().unwrap();
        if matches!(find_dbn_serialize_attr(f).unwrap_or(None), Some(id) if id == attr) {
            quote! { res.push(stringify!(#ident).to_owned()); }
        } else {
            let f_type = &f.ty;
            quote! { res.extend(<#f_type>::#method(stringify!(#ident))); }
        }
    });
    quote! {
        #(#fields_iter)*
    }
}

fn hidden_fields(fields: &VecDeque<Field>) -> TokenStream {
    let fields_iter = fields.iter().map(|f| {
        let ident = f.ident.as_ref().unwrap();
        if is_hidden(f) {
            quote! { res.push(stringify!(#ident).to_owned()); }
        } else {
            let f_type = &f.ty;
            quote! { res.extend(<#f_type>::hidden_fields(stringify!(#ident))); }
        }
    });
    quote! {
        #(#fields_iter)*
    }
}

```

## High-Level Overview

This file is located at `rust/dbn-macros/src/py_field_desc.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** derive_impl, field_dtypes, fields_with_attr, hidden_fields, ordered_fields, price_fields, timestamp_fields

**Dependencies:** This file imports from 5 modules


#### Detailed Walkthrough


##### Function: `derive_impl`

```rust
pub fn derive_impl(input: proc_macro::TokenStream) -> proc_macro::TokenStream {
```


##### Function: `field_dtypes`

```rust
fn field_dtypes(_field_name: &str) -> Vec<(String, String)> {
```


##### Function: `price_fields`

```rust
fn price_fields(_field_name: &str) -> Vec<String> {
```


##### Function: `hidden_fields`

```rust
fn hidden_fields(_field_name: &str) -> Vec<String> {
```


##### Function: `timestamp_fields`

```rust
fn timestamp_fields(_field_name: &str) -> Vec<String> {
```


##### Function: `ordered_fields`

```rust
fn ordered_fields(_field_name: &str) -> Vec<String> {
```


##### Function: `fields_with_attr`

```rust
fn fields_with_attr(fields: &VecDeque<Field>, attr: &str, method: TokenStream) -> TokenStream {
```


##### Function: `hidden_fields`

```rust
fn hidden_fields(fields: &VecDeque<Field>) -> TokenStream {
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

