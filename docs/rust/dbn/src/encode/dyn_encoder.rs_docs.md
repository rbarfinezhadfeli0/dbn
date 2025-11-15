# Documentation: rust/dbn/src/encode/dyn_encoder.rs

## File Metadata

**Path:** `rust/dbn/src/encode/dyn_encoder.rs`
**Filename:** `dyn_encoder.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../../../rust/dbn/src/encode/dyn_encoder.rs`

### Source Content

```rs
use std::io;

use fallible_streaming_iterator::FallibleStreamingIterator;

use super::{
    CsvEncoder, DbnEncodable, DbnEncoder, DynWriter, EncodeDbn, EncodeRecord, EncodeRecordRef,
    EncodeRecordTextExt, JsonEncoder,
};
use crate::{
    decode::{DbnMetadata, DecodeRecordRef},
    Compression, Encoding, Error, Metadata, RecordRef, Result, Schema,
};

/// An encoder whose [`Encoding`] and [`Compression`] can be set at runtime.
pub struct DynEncoder<'a, W>(DynEncoderImpl<'a, W>)
where
    W: io::Write;

// [`DynEncoder`] isn't cloned so this isn't a concern.
#[allow(clippy::large_enum_variant)]
enum DynEncoderImpl<'a, W>
where
    W: io::Write,
{
    Dbn(DbnEncoder<DynWriter<'a, W>>),
    Csv(CsvEncoder<DynWriter<'a, W>>),
    Json(JsonEncoder<DynWriter<'a, W>>),
}

/// Helper for constructing a [`DynEncoder`].
pub struct DynEncoderBuilder<'m, W>
where
    W: io::Write,
{
    writer: W,
    encoding: Encoding,
    compression: Compression,
    metadata: &'m Metadata,
    write_header: bool,
    should_pretty_print: bool,
    use_pretty_px: bool,
    use_pretty_ts: bool,
    with_symbol: bool,
    delimiter: u8,
}

impl<'m, W> DynEncoderBuilder<'m, W>
where
    W: io::Write,
{
    /// Creates a new builder. All required fields for the builder are passed to this
    /// function.
    pub fn new(
        writer: W,
        encoding: Encoding,
        compression: Compression,
        metadata: &'m Metadata,
    ) -> Self {
        Self {
            writer,
            encoding,
            compression,
            metadata,
            write_header: true,
            should_pretty_print: false,
            use_pretty_px: false,
            use_pretty_ts: false,
            with_symbol: false,
            delimiter: b',',
        }
    }

    /// Sets whether the CSV encoder will write a header row automatically.
    /// Defaults to `true`.
    ///
    /// If `false`, a header row can still be written with
    /// [`DynEncoder::encode_header()`] or [`DynEncoder::encode_header_for_schema()`].
    pub fn write_header(mut self, write_header: bool) -> Self {
        self.write_header = write_header;
        self
    }

    /// Sets all three pretty options together: `should_pretty_print`, `use_pretty_px`,
    /// and `use_pretty_ts`. By default all are `false`.
    pub fn all_pretty(self, all_pretty: bool) -> Self {
        self.should_pretty_print(all_pretty)
            .use_pretty_px(all_pretty)
            .use_pretty_ts(all_pretty)
    }

    /// Sets whether the encoder should encode nicely-formatted JSON objects with
    /// indentation if encoding JSON. Defaults to `false` where each JSON object is
    /// compact with no spacing.
    pub fn should_pretty_print(mut self, should_pretty_print: bool) -> Self {
        self.should_pretty_print = should_pretty_print;
        self
    }

    /// Sets whether the encoder will serialize price fields as a decimal in CSV and
    /// JSON encodings. Defaults to `false`.
    pub fn use_pretty_px(mut self, use_pretty_px: bool) -> Self {
        self.use_pretty_px = use_pretty_px;
        self
    }

    /// Sets whether the encoder will serialize timestamp fields as ISO8601 datetime
    /// strings in CSV and JSON encodings. Defaults to `false`.
    pub fn use_pretty_ts(mut self, use_pretty_ts: bool) -> Self {
        self.use_pretty_ts = use_pretty_ts;
        self
    }

    /// Sets whether to add a header field "symbol" if encoding CSV. Defaults to
    /// `false`.
    pub fn with_symbol(mut self, with_symbol: bool) -> Self {
        self.with_symbol = with_symbol;
        self
    }

    /// Sets the field delimiter. Defaults to `b','` for comma-separated values (CSV).
    pub fn delimiter(mut self, delimiter: u8) -> Self {
        self.delimiter = delimiter;
        self
    }

    /// Creates the new encoder with the previously specified settings and if
    /// `write_header` is `true`, encodes the header row.
    ///
    /// # Errors
    /// This function returns an error if it fails to write the CSV header row or the
    /// DBN metadata.
    pub fn build<'a>(self) -> crate::Result<DynEncoder<'a, W>> {
        let writer = DynWriter::new(self.writer, self.compression)?;
        Ok(DynEncoder(match self.encoding {
            Encoding::Dbn => DynEncoderImpl::Dbn(DbnEncoder::new(writer, self.metadata)?),
            Encoding::Csv => DynEncoderImpl::Csv(
                CsvEncoder::builder(writer)
                    .use_pretty_px(self.use_pretty_px)
                    .use_pretty_ts(self.use_pretty_ts)
                    .delimiter(self.delimiter)
                    .write_header(self.write_header)
                    .ts_out(self.metadata.ts_out)
                    .schema(self.metadata.schema)
                    .with_symbol(self.with_symbol)
                    .build()?,
            ),
            Encoding::Json => DynEncoderImpl::Json(
                JsonEncoder::builder(writer)
                    .should_pretty_print(self.should_pretty_print)
                    .use_pretty_px(self.use_pretty_px)
                    .use_pretty_ts(self.use_pretty_ts)
                    .build(),
            ),
        }))
    }
}

impl<W> DynEncoder<'_, W>
where
    W: io::Write,
{
    /// Constructs a new instance of [`DynEncoder`].
    ///
    /// Note: `should_pretty_print`, `use_pretty_px`, and `use_pretty_ts` are ignored
    /// if `encoding` is `Dbn`.
    ///
    /// # Errors
    /// This function returns an error if it fails to encode the DBN metadata or
    /// it fails to initialize the Zstd compression.
    pub fn new(
        writer: W,
        encoding: Encoding,
        compression: Compression,
        metadata: &Metadata,
        should_pretty_print: bool,
        use_pretty_px: bool,
        use_pretty_ts: bool,
    ) -> Result<Self> {
        Self::builder(writer, encoding, compression, metadata)
            .should_pretty_print(should_pretty_print)
            .use_pretty_px(use_pretty_px)
            .use_pretty_ts(use_pretty_ts)
            .build()
    }

    /// Creates a builder for configuring a `DynEncoder` object.
    pub fn builder(
        writer: W,
        encoding: Encoding,
        compression: Compression,
        metadata: &Metadata,
    ) -> DynEncoderBuilder<'_, W> {
        DynEncoderBuilder::new(writer, encoding, compression, metadata)
    }

    /// Encodes the CSV header for the record type `R`, i.e. the names of each of the
    /// fields to the output.
    ///
    /// If `with_symbol` is `true`, will add a header field for "symbol".
    ///
    /// # Errors
    /// This function returns an error if there's an error writing to `writer`.
    pub fn encode_header<R: DbnEncodable>(&mut self, with_symbol: bool) -> Result<()> {
        match &mut self.0 {
            DynEncoderImpl::Csv(encoder) => encoder.encode_header::<R>(with_symbol),
            _ => Ok(()),
        }
    }

    /// Encodes the CSV header for `schema`, i.e. the names of each of the fields to
    /// the output.
    ///
    /// If `ts_out` is `true`, will add a header field "ts_out". If `with_symbol` is
    /// `true`, will add a header field "symbol".
    ///
    /// # Errors
    /// This function returns an error if there's an error writing to `writer`.
    pub fn encode_header_for_schema(
        &mut self,
        schema: Schema,
        ts_out: bool,
        with_symbol: bool,
    ) -> Result<()> {
        match &mut self.0 {
            DynEncoderImpl::Csv(encoder) => {
                encoder.encode_header_for_schema(schema, ts_out, with_symbol)
            }
            _ => Ok(()),
        }
    }
}

impl<W> EncodeRecord for DynEncoder<'_, W>
where
    W: io::Write,
{
    fn encode_record<R: DbnEncodable>(&mut self, record: &R) -> Result<()> {
        self.0.encode_record(record)
    }

    fn flush(&mut self) -> Result<()> {
        self.0.flush()
    }
}

impl<W> EncodeRecordRef for DynEncoder<'_, W>
where
    W: io::Write,
{
    fn encode_record_ref(&mut self, record: RecordRef) -> Result<()> {
        self.0.encode_record_ref(record)
    }

    unsafe fn encode_record_ref_ts_out(&mut self, record: RecordRef, ts_out: bool) -> Result<()> {
        self.0.encode_record_ref_ts_out(record, ts_out)
    }
}

impl<W> EncodeDbn for DynEncoder<'_, W>
where
    W: io::Write,
{
    fn encode_records<R: DbnEncodable>(&mut self, records: &[R]) -> Result<()> {
        self.0.encode_records(records)
    }

    fn encode_stream<R: DbnEncodable>(
        &mut self,
        stream: impl FallibleStreamingIterator<Item = R, Error = Error>,
    ) -> Result<()> {
        self.0.encode_stream(stream)
    }

    fn encode_decoded<D: DecodeRecordRef + DbnMetadata>(&mut self, decoder: D) -> Result<()> {
        self.0.encode_decoded(decoder)
    }
}

impl<W> EncodeRecordTextExt for DynEncoder<'_, W>
where
    W: io::Write,
{
    fn encode_record_with_sym<R: DbnEncodable>(
        &mut self,
        record: &R,
        symbol: Option<&str>,
    ) -> Result<()> {
        self.0.encode_record_with_sym(record, symbol)
    }
}

impl<W> EncodeRecord for DynEncoderImpl<'_, W>
where
    W: io::Write,
{
    fn encode_record<R: DbnEncodable>(&mut self, record: &R) -> Result<()> {
        match self {
            DynEncoderImpl::Dbn(enc) => enc.encode_record(record),
            DynEncoderImpl::Csv(enc) => enc.encode_record(record),
            DynEncoderImpl::Json(enc) => enc.encode_record(record),
        }
    }

    fn flush(&mut self) -> Result<()> {
        match self {
            DynEncoderImpl::Dbn(enc) => enc.flush(),
            DynEncoderImpl::Csv(enc) => enc.flush(),
            DynEncoderImpl::Json(enc) => enc.flush(),
        }
    }
}

impl<W> EncodeRecordRef for DynEncoderImpl<'_, W>
where
    W: io::Write,
{
    fn encode_record_ref(&mut self, record: RecordRef) -> Result<()> {
        match self {
            DynEncoderImpl::Dbn(enc) => enc.encode_record_ref(record),
            DynEncoderImpl::Csv(enc) => enc.encode_record_ref(record),
            DynEncoderImpl::Json(enc) => enc.encode_record_ref(record),
        }
    }

    unsafe fn encode_record_ref_ts_out(&mut self, record: RecordRef, ts_out: bool) -> Result<()> {
        match self {
            DynEncoderImpl::Dbn(enc) => enc.encode_record_ref_ts_out(record, ts_out),
            DynEncoderImpl::Csv(enc) => enc.encode_record_ref_ts_out(record, ts_out),
            DynEncoderImpl::Json(enc) => enc.encode_record_ref_ts_out(record, ts_out),
        }
    }
}

impl<W> EncodeDbn for DynEncoderImpl<'_, W>
where
    W: io::Write,
{
    fn encode_records<R: DbnEncodable>(&mut self, records: &[R]) -> Result<()> {
        match self {
            DynEncoderImpl::Dbn(encoder) => encoder.encode_records(records),
            DynEncoderImpl::Csv(encoder) => encoder.encode_records(records),
            DynEncoderImpl::Json(encoder) => encoder.encode_records(records),
        }
    }

    fn encode_stream<R: DbnEncodable>(
        &mut self,
        stream: impl FallibleStreamingIterator<Item = R, Error = Error>,
    ) -> Result<()> {
        match self {
            DynEncoderImpl::Dbn(encoder) => encoder.encode_stream(stream),
            DynEncoderImpl::Csv(encoder) => encoder.encode_stream(stream),
            DynEncoderImpl::Json(encoder) => encoder.encode_stream(stream),
        }
    }

    fn encode_decoded<D: DecodeRecordRef + DbnMetadata>(&mut self, decoder: D) -> Result<()> {
        match self {
            DynEncoderImpl::Dbn(encoder) => encoder.encode_decoded(decoder),
            DynEncoderImpl::Csv(encoder) => encoder.encode_decoded(decoder),
            DynEncoderImpl::Json(encoder) => encoder.encode_decoded(decoder),
        }
    }
}

impl<W> EncodeRecordTextExt for DynEncoderImpl<'_, W>
where
    W: io::Write,
{
    fn encode_record_with_sym<R: DbnEncodable>(
        &mut self,
        record: &R,
        symbol: Option<&str>,
    ) -> Result<()> {
        match self {
            // Not supported for DBN so ignore `symbol`
            Self::Dbn(encoder) => encoder.encode_record(record),
            Self::Csv(encoder) => encoder.encode_record_with_sym(record, symbol),
            Self::Json(encoder) => encoder.encode_record_with_sym(record, symbol),
        }
    }
}

```

## High-Level Overview

This file is located at `rust/dbn/src/encode/dyn_encoder.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** all_pretty, build, builder, delimiter, encode_decoded, encode_header, encode_header_for_schema, encode_record, encode_record_ref, encode_record_ref_ts_out, encode_record_with_sym, encode_records, encode_stream, flush, new, should_pretty_print, use_pretty_px, use_pretty_ts, with_symbol, write_header

**Structs defined:** DynEncoder, DynEncoderBuilder

**Enums defined:** DynEncoderImpl

**Dependencies:** This file imports from 4 modules


#### Detailed Walkthrough


##### Function: `new`

```rust
pub fn new(
        writer: W,
        encoding: Encoding,
        compression: Compression,
        metadata: &'m Metadata,
    ) -> Self {
```


##### Function: `write_header`

```rust
pub fn write_header(mut self, write_header: bool) -> Self {
```


##### Function: `all_pretty`

```rust
pub fn all_pretty(self, all_pretty: bool) -> Self {
```


##### Function: `should_pretty_print`

```rust
pub fn should_pretty_print(mut self, should_pretty_print: bool) -> Self {
```


##### Function: `use_pretty_px`

```rust
pub fn use_pretty_px(mut self, use_pretty_px: bool) -> Self {
```


##### Function: `use_pretty_ts`

```rust
pub fn use_pretty_ts(mut self, use_pretty_ts: bool) -> Self {
```


##### Function: `with_symbol`

```rust
pub fn with_symbol(mut self, with_symbol: bool) -> Self {
```


##### Function: `delimiter`

```rust
pub fn delimiter(mut self, delimiter: u8) -> Self {
```


##### Function: `build`

```rust
pub fn build<'a>(self) -> crate::Result<DynEncoder<'a, W>> {
```


##### Function: `new`

```rust
pub fn new(
        writer: W,
        encoding: Encoding,
        compression: Compression,
        metadata: &Metadata,
        should_pretty_print: bool,
        use_pretty_px: bool,
        use_pretty_ts: bool,
    ) -> Result<Self> {
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

