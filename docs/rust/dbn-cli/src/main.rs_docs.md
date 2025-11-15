# Documentation: rust/dbn-cli/src/main.rs

## File Metadata

**Path:** `rust/dbn-cli/src/main.rs`
**Filename:** `main.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../../rust/dbn-cli/src/main.rs`

### Source Content

```rs
use std::{
    fs::File,
    io::{self, BufRead, BufReader},
    path::Path,
};

use anyhow::Context;
use clap::Parser;
use dbn::decode::{
    DbnMetadata, DbnRecordDecoder, DecodeRecordRef, DynDecoder, MergeDecoder, MergeRecordDecoder,
};
use dbn_cli::{
    encode::{encode_from_dbn, encode_from_frag, silence_broken_pipe},
    filter::{LimitFilter, SchemaFilter},
    Args,
};

const STDIN_SENTINEL: &str = "-";

fn open_input_file(path: &Path) -> anyhow::Result<File> {
    File::open(path).with_context(|| format!("opening file to decode at path '{}'", path.display()))
}

fn wrap_frag(args: &Args, decoder: impl DecodeRecordRef) -> impl DecodeRecordRef {
    LimitFilter::new_no_metadata(
        SchemaFilter::new_no_metadata(decoder, args.schema_filter),
        args.limit,
    )
}

/// assume no ts_out for fragments
const FRAG_TS_OUT: bool = false;

fn decode_frag(args: &Args, reader: impl io::Read) -> anyhow::Result<impl DecodeRecordRef> {
    Ok(wrap_frag(
        args,
        DbnRecordDecoder::with_version(
            reader,
            args.input_version(),
            args.upgrade_policy(),
            FRAG_TS_OUT,
        )?,
    ))
}

fn wrap(
    args: &Args,
    decoder: impl DecodeRecordRef + DbnMetadata,
) -> impl DecodeRecordRef + DbnMetadata {
    LimitFilter::new(SchemaFilter::new(decoder, args.schema_filter), args.limit)
}

fn with_inputs(args: Args) -> anyhow::Result<()> {
    if args.is_input_fragment {
        let decoders = args
            .input
            .iter()
            .map(|input| {
                Ok(DbnRecordDecoder::with_version(
                    BufReader::new(open_input_file(input)?),
                    args.input_version(),
                    args.upgrade_policy(),
                    FRAG_TS_OUT,
                )?)
            })
            .collect::<anyhow::Result<Vec<DbnRecordDecoder<BufReader<File>>>>>()?;
        encode_from_frag(&args, MergeRecordDecoder::new(decoders)?)
    } else if args.is_input_zstd_fragment {
        let decoders = args
            .input
            .iter()
            .map(|input| {
                Ok(DbnRecordDecoder::with_version(
                    zstd::stream::Decoder::new(open_input_file(input)?)?,
                    args.input_version(),
                    args.upgrade_policy(),
                    FRAG_TS_OUT,
                )?)
            })
            .collect::<anyhow::Result<Vec<DbnRecordDecoder<zstd::stream::Decoder<BufReader<File>>>>>>()?;
        encode_from_frag(&args, MergeRecordDecoder::new(decoders)?)
    } else {
        let decoders = args
            .input
            .iter()
            .map(|input| DynDecoder::from_file(input, args.upgrade_policy()))
            .collect::<dbn::Result<Vec<DynDecoder<BufReader<File>>>>>()?;
        encode_from_dbn(&args, wrap(&args, MergeDecoder::new(decoders)?))
    }
}

fn with_input(args: Args, reader: impl BufRead) -> anyhow::Result<()> {
    if args.is_input_fragment {
        encode_from_frag(&args, decode_frag(&args, reader)?)
    } else if args.is_input_zstd_fragment {
        encode_from_frag(
            &args,
            decode_frag(&args, zstd::stream::Decoder::with_buffer(reader)?)?,
        )
    } else {
        encode_from_dbn(
            &args,
            wrap(
                &args,
                DynDecoder::inferred_with_buffer(reader, args.upgrade_policy())?,
            ),
        )
    }
}

fn main() -> anyhow::Result<()> {
    let args = Args::parse();
    if args.input.len() > 1 {
        with_inputs(args)
    } else if args.input[0].as_os_str() == STDIN_SENTINEL {
        with_input(args, io::stdin().lock())
    } else {
        let reader = BufReader::new(open_input_file(&args.input[0])?);
        with_input(args, reader)
    }
    .or_else(silence_broken_pipe)
}

```

## High-Level Overview

This file is located at `rust/dbn-cli/src/main.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** decode_frag, main, open_input_file, with_input, with_inputs, wrap, wrap_frag

**Dependencies:** This file imports from 5 modules


#### Detailed Walkthrough


##### Function: `open_input_file`

```rust
fn open_input_file(path: &Path) -> anyhow::Result<File> {
```


##### Function: `wrap_frag`

```rust
fn wrap_frag(args: &Args, decoder: impl DecodeRecordRef) -> impl DecodeRecordRef {
```


##### Function: `decode_frag`

```rust
fn decode_frag(args: &Args, reader: impl io::Read) -> anyhow::Result<impl DecodeRecordRef> {
```


##### Function: `wrap`

```rust
fn wrap(
    args: &Args,
    decoder: impl DecodeRecordRef + DbnMetadata,
) -> impl DecodeRecordRef + DbnMetadata {
```


##### Function: `with_inputs`

```rust
fn with_inputs(args: Args) -> anyhow::Result<()> {
```


##### Function: `with_input`

```rust
fn with_input(args: Args, reader: impl BufRead) -> anyhow::Result<()> {
```


##### Function: `main`

```rust
fn main() -> anyhow::Result<()> {
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

