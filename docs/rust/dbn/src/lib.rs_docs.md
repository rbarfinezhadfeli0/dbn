# Documentation: rust/dbn/src/lib.rs

## File Metadata

**Path:** `rust/dbn/src/lib.rs`
**Filename:** `lib.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../../rust/dbn/src/lib.rs`

### Source Content

```rs
//! The official crate for working with [**D**atabento](https://databento.com)
//! **B**inary E**n**coding (DBN), an extremely fast message encoding and storage format
//! for normalized market data. The DBN specification includes a simple, self-describing
//! metadata header and a fixed set of struct definitions, which enforce a standardized
//! way to normalize market data.
//!
//! All official Databento client libraries use DBN under the hood, both as a data
//! interchange format and for in-memory representation of data. DBN is also the default
//! encoding for all Databento APIs, including live data streaming, historical data
//! streaming, and batch flat files. For more information about the encoding, read our
//! [introduction to DBN](https://databento.com/docs/standards-and-conventions/databento-binary-encoding).
//!
//! The crate supports reading and writing DBN files and streams, as well as converting
//! them to other [`Encoding`]s. It can also be used to update legacy
//! DBZ files to DBN.
//!
//! This crate provides:
//! - [Decoders](crate::decode) for DBN and DBZ (the precursor to DBN), both
//!   sync and async, with the `async` feature flag
//! - [Encoders](crate::encode) for CSV, DBN, and JSON, both sync and async,
//!   with the `async` feature flag
//! - [Normalized market data struct definitions](crate::record) corresponding to the
//!   different market data schemas offered by Databento
//! - A [wrapper type](crate::RecordRef) for holding a reference to a record struct of
//!   a dynamic type
//! - Helper functions and [macros] for common tasks
//!
//! # Feature flags
//! - `async`: enables async decoding and encoding
//! - `python`: enables `pyo3` bindings
//! - `serde`: enables deriving `serde` traits for types
//! - `trivial_copy`: enables deriving the `Copy` trait for records

// Experimental feature to allow docs.rs to display features
#![cfg_attr(docsrs, feature(doc_auto_cfg))]
#![deny(missing_docs)]
#![deny(rustdoc::broken_intra_doc_links)]
#![deny(clippy::missing_errors_doc)]

pub mod compat;
pub mod decode;
pub mod encode;
pub mod enums;
pub mod error;
pub mod flags;
mod json_writer;
pub mod macros;
pub mod metadata;
pub mod pretty;
pub mod publishers;
#[cfg(feature = "python")]
pub mod python;
pub mod record;
mod record_enum;
pub mod record_ref;
pub mod symbol_map;
#[cfg(test)]
mod test_utils;
pub mod v1;
pub mod v2;
pub mod v3;

pub use crate::{
    enums::{
        rtype, Action, Compression, Encoding, InstrumentClass, MatchAlgorithm, RType, SType,
        Schema, SecurityUpdateAction, Side, StatType, StatUpdateAction, StatusAction, StatusReason,
        TradingEvent, TriState, UserDefinedInstrument, VersionUpgradePolicy,
    },
    error::{Error, Result},
    flags::FlagSet,
    metadata::{MappingInterval, Metadata, MetadataBuilder, SymbolMapping},
    publishers::{Dataset, Publisher, Venue},
    record::{
        Bbo1MMsg, Bbo1SMsg, BboMsg, BidAskPair, Cbbo1MMsg, Cbbo1SMsg, CbboMsg, Cmbp1Msg,
        ConsolidatedBidAskPair, ErrorMsg, HasRType, ImbalanceMsg, InstrumentDefMsg, MboMsg,
        Mbp10Msg, Mbp1Msg, OhlcvMsg, Record, RecordHeader, RecordMut, StatMsg, StatusMsg,
        SymbolMappingMsg, SystemMsg, TbboMsg, TradeMsg, WithTsOut,
    },
    record_enum::{RecordEnum, RecordRefEnum},
    record_ref::RecordRef,
    symbol_map::{PitSymbolMap, SymbolIndex, TsSymbolMap},
};

/// The current version of the DBN encoding, which is different from the crate version.
pub const DBN_VERSION: u8 = 2;
/// The length of fixed-length symbol strings.
pub const SYMBOL_CSTR_LEN: usize = compat::SYMBOL_CSTR_LEN_V2;

const METADATA_DATASET_CSTR_LEN: usize = 16;
const METADATA_RESERVED_LEN: usize = 53;
/// Excludes magic string, version, and length.
const METADATA_FIXED_LEN: usize = 100;
const NULL_LIMIT: u64 = 0;
const NULL_RECORD_COUNT: u64 = u64::MAX;
const NULL_SCHEMA: u16 = u16::MAX;
const NULL_STYPE: u8 = u8::MAX;

/// The denominator of fixed prices in DBN.
pub const FIXED_PRICE_SCALE: i64 = 1_000_000_000;
/// The sentinel value for an unset or null price.
pub const UNDEF_PRICE: i64 = i64::MAX;
/// The sentinel value for an unset or null order quantity.
pub const UNDEF_ORDER_SIZE: u32 = u32::MAX;
/// The sentinel value for an unset or null stat quantity.
pub const UNDEF_STAT_QUANTITY: i32 = i32::MAX;
/// The sentinel value for an unset or null timestamp.
pub const UNDEF_TIMESTAMP: u64 = u64::MAX;
/// The length in bytes of the largest record type.
pub const MAX_RECORD_LEN: usize = std::mem::size_of::<WithTsOut<v3::InstrumentDefMsg>>();

/// Contains dataset code constants.
#[deprecated(since = "0.25.0", note = "Use the `Dataset` enum instead")]
pub mod datasets {
    use crate::publishers::Dataset;

    /// The dataset code for Databento Equities Basic.
    pub const DBEQ_BASIC: &str = Dataset::DbeqBasic.as_str();
    /// The dataset code for CME Globex MDP 3.0.
    pub const GLBX_MDP3: &str = Dataset::GlbxMdp3.as_str();
    /// The dataset code for OPRA PILLAR.
    pub const OPRA_PILLAR: &str = Dataset::OpraPillar.as_str();
    /// The dataset code for Nasdaq TotalView-ITCH.
    pub const XNAS_ITCH: &str = Dataset::XnasItch.as_str();
}

```

## High-Level Overview

This file is located at `rust/dbn/src/lib.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Structs defined:** definitions, of

**Enums defined:** instead

**Traits defined:** for

**Dependencies:** This file imports from 3 modules


#### Detailed Walkthrough



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

