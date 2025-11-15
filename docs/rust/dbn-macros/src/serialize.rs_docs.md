# Documentation: rust/dbn-macros/src/serialize.rs

## File Metadata

**Path:** `rust/dbn-macros/src/serialize.rs`
**Filename:** `serialize.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../../rust/dbn-macros/src/serialize.rs`

### Source Content

```rs
use proc_macro2::TokenStream;
use quote::quote;
use syn::{parse_macro_input, Data, DeriveInput, Field};

use crate::{
    dbn_attr::{
        find_dbn_serialize_attr, get_sorted_fields, is_hidden, C_CHAR_ATTR, FIXED_PRICE_ATTR,
        UNIX_NANOS_ATTR,
    },
    utils::crate_name,
};

pub fn derive_csv_macro_impl(input: proc_macro::TokenStream) -> proc_macro::TokenStream {
    let DeriveInput { ident, data, .. } = parse_macro_input!(input as DeriveInput);

    if let Data::Struct(data_struct) = data {
        if let syn::Fields::Named(fields) = data_struct.fields {
            let crate_name = crate_name();
            let fields = match get_sorted_fields(fields) {
                Ok(fields) => fields,
                Err(ts) => {
                    return ts.into_compile_error().into();
                }
            };
            let serialize_header_iter = fields.iter().map(write_csv_header_token_stream);
            let serialize_fields = fields
                .iter()
                .map(write_csv_field_token_stream)
                .collect::<syn::Result<Vec<_>>>()
                .unwrap_or_else(|e| vec![syn::Error::to_compile_error(&e)]);
            return quote! {
                impl #crate_name::encode::csv::serialize::CsvSerialize for #ident {
                    fn serialize_header<W: ::std::io::Write>(writer: &mut ::csv::Writer<W>) -> ::csv::Result<()> {
                        use #crate_name::encode::csv::serialize::WriteField;

                        #(#serialize_header_iter)*
                        Ok(())
                    }

                    fn serialize_to<W: ::std::io::Write, const PRETTY_PX: bool, const PRETTY_TS: bool>(
                        &self,
                        writer: &mut ::csv::Writer<W>
                    ) -> ::csv::Result<()> {
                        use #crate_name::encode::csv::serialize::WriteField;

                        #(#serialize_fields)*
                        Ok(())
                    }
                }
            }
            .into();
        }
    }
    syn::Error::new(ident.span(), "Can only derive CsvSerialize for structs")
        .into_compile_error()
        .into()
}

pub fn derive_json_macro_impl(input: proc_macro::TokenStream) -> proc_macro::TokenStream {
    let DeriveInput { ident, data, .. } = parse_macro_input!(input as DeriveInput);

    if let Data::Struct(data_struct) = data {
        if let syn::Fields::Named(fields) = data_struct.fields {
            let crate_name = crate_name();
            let fields = match get_sorted_fields(fields) {
                Ok(fields) => fields,
                Err(ts) => {
                    return ts.into_compile_error().into();
                }
            };
            let serialize_fields = fields
                .iter()
                .map(write_json_field_token_stream)
                .collect::<syn::Result<Vec<_>>>()
                .unwrap_or_else(|e| vec![syn::Error::to_compile_error(&e)]);
            return quote! {
                impl crate::encode::json::serialize::JsonSerialize for #ident {
                    fn to_json<J: #crate_name::json_writer::JsonWriter, const PRETTY_PX: bool, const PRETTY_TS: bool>(
                        &self,
                        writer: &mut #crate_name::json_writer::JsonObjectWriter<J>,
                    ) {
                        use #crate_name::encode::json::serialize::WriteField;

                        #(#serialize_fields)*
                    }
                }
            }
            .into();
        }
    }
    syn::Error::new(ident.span(), "Can only derive JsonSerialize for structs")
        .into_compile_error()
        .into()
}

fn write_csv_header_token_stream(field: &Field) -> TokenStream {
    let ident = field.ident.as_ref().unwrap();
    let field_type = &field.ty;
    // ignore dummy and skipped fields
    if is_hidden(field) {
        return TokenStream::new();
    }
    quote! {
        <#field_type>::write_header(writer, stringify!(#ident))?;
    }
}

fn write_csv_field_token_stream(field: &Field) -> syn::Result<TokenStream> {
    let ident = field.ident.as_ref().unwrap();
    // ignore dummy fields
    if is_hidden(field) {
        return Ok(quote! {});
    }
    if let Some(dbn_attr_id) = find_dbn_serialize_attr(field)? {
        if dbn_attr_id == UNIX_NANOS_ATTR {
            Ok(quote! {
                crate::encode::csv::serialize::write_ts_field::<_, PRETTY_TS>(writer, self.#ident)?;
            })
        } else if dbn_attr_id == FIXED_PRICE_ATTR {
            Ok(quote! {
                crate::encode::csv::serialize::write_px_field::<_, PRETTY_PX>(writer, self.#ident)?;
            })
        } else if dbn_attr_id == C_CHAR_ATTR {
            Ok(quote! {
                crate::encode::csv::serialize::write_c_char_field(writer, self.#ident)?;
            })
        } else {
            Err(syn::Error::new(
                dbn_attr_id.span(),
                format!("Invalid attr `{dbn_attr_id}` passed to `#[dbn]`"),
            ))
        }
    } else {
        Ok(quote! {
            self.#ident.write_field::<_, PRETTY_PX, PRETTY_TS>(writer)?;
        })
    }
}

fn write_json_field_token_stream(field: &Field) -> syn::Result<TokenStream> {
    let ident = field.ident.as_ref().unwrap();
    // ignore dummy fields
    if is_hidden(field) {
        return Ok(quote! {});
    }
    if let Some(dbn_attr_id) = find_dbn_serialize_attr(field)? {
        if dbn_attr_id == UNIX_NANOS_ATTR {
            Ok(quote! {
                crate::encode::json::serialize::write_ts_field::<_, PRETTY_TS>(writer, stringify!(#ident), self.#ident);
            })
        } else if dbn_attr_id == FIXED_PRICE_ATTR {
            Ok(quote! {
                crate::encode::json::serialize::write_px_field::<_, PRETTY_PX>(writer, stringify!(#ident), self.#ident);
            })
        } else if dbn_attr_id == C_CHAR_ATTR {
            Ok(quote! {
                crate::encode::json::serialize::write_c_char_field(writer, stringify!(#ident), self.#ident);
            })
        } else {
            Err(syn::Error::new(
                dbn_attr_id.span(),
                format!("Invalid attr `{dbn_attr_id}` passed to `#[dbn]`"),
            ))
        }
    } else {
        Ok(quote! {
            self.#ident.write_field::<_, PRETTY_PX, PRETTY_TS>(writer, stringify!(#ident));
        })
    }
}

#[cfg(test)]
mod tests {
    use syn::FieldsNamed;

    use super::*;

    #[test]
    fn skip_field() {
        let input = quote!({
                #[dbn(skip)]
                pub b: bool,
        });
        let fields = syn::parse2::<FieldsNamed>(input).unwrap();
        assert_eq!(fields.named.len(), 1);
        let csv_generated = write_csv_field_token_stream(fields.named.first().unwrap()).unwrap();
        let json_generated = write_json_field_token_stream(fields.named.first().unwrap()).unwrap();
        assert!(csv_generated.is_empty());
        assert!(json_generated.is_empty());
    }

    #[test]
    fn skip_underscore_field() {
        let input = quote!({
                pub _a: bool,
        });
        let fields = syn::parse2::<FieldsNamed>(input).unwrap();
        assert_eq!(fields.named.len(), 1);
        let csv_generated = write_csv_field_token_stream(fields.named.first().unwrap()).unwrap();
        let json_generated = write_json_field_token_stream(fields.named.first().unwrap()).unwrap();
        assert!(csv_generated.is_empty());
        assert!(json_generated.is_empty());
    }
}

```

## High-Level Overview

This file is located at `rust/dbn-macros/src/serialize.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** derive_csv_macro_impl, derive_json_macro_impl, serialize_header, serialize_to, skip_field, skip_underscore_field, to_json, write_csv_field_token_stream, write_csv_header_token_stream, write_json_field_token_stream

**Dependencies:** This file imports from 8 modules


#### Detailed Walkthrough


##### Function: `derive_csv_macro_impl`

```rust
pub fn derive_csv_macro_impl(input: proc_macro::TokenStream) -> proc_macro::TokenStream {
```


##### Function: `serialize_header`

```rust
fn serialize_header<W: ::std::io::Write>(writer: &mut ::csv::Writer<W>) -> ::csv::Result<()> {
```


##### Function: `serialize_to`

```rust
fn serialize_to<W: ::std::io::Write, const PRETTY_PX: bool, const PRETTY_TS: bool>(
                        &self,
                        writer: &mut ::csv::Writer<W>
                    ) -> ::csv::Result<()> {
```


##### Function: `derive_json_macro_impl`

```rust
pub fn derive_json_macro_impl(input: proc_macro::TokenStream) -> proc_macro::TokenStream {
```


##### Function: `to_json`

```rust
fn to_json<J: #crate_name::json_writer::JsonWriter, const PRETTY_PX: bool, const PRETTY_TS: bool>(
                        &self,
                        writer: &mut #crate_name::json_writer::JsonObjectWriter<J>,
                    ) {
```


##### Function: `write_csv_header_token_stream`

```rust
fn write_csv_header_token_stream(field: &Field) -> TokenStream {
```


##### Function: `write_csv_field_token_stream`

```rust
fn write_csv_field_token_stream(field: &Field) -> syn::Result<TokenStream> {
```


##### Function: `write_json_field_token_stream`

```rust
fn write_json_field_token_stream(field: &Field) -> syn::Result<TokenStream> {
```


##### Function: `skip_field`

```rust
fn skip_field() {
```


##### Function: `skip_underscore_field`

```rust
fn skip_underscore_field() {
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

