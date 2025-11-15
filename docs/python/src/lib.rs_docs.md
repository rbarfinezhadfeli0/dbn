# Documentation: python/src/lib.rs

## File Metadata

**Path:** `python/src/lib.rs`
**Filename:** `lib.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../python/src/lib.rs`

### Source Content

```rs
//! Python bindings for the [`dbn`] crate using [`pyo3`].

use pyo3::{prelude::*, wrap_pyfunction, PyClass};

use dbn::{
    compat::{ErrorMsgV1, InstrumentDefMsgV1, InstrumentDefMsgV3, SymbolMappingMsgV1, SystemMsgV1},
    flags,
    python::{DBNError, EnumIterator},
    Action, BboMsg, BidAskPair, CbboMsg, Cmbp1Msg, Compression, ConsolidatedBidAskPair, Encoding,
    ErrorMsg, ImbalanceMsg, InstrumentClass, InstrumentDefMsg, MatchAlgorithm, MboMsg, Mbp10Msg,
    Mbp1Msg, Metadata, OhlcvMsg, RType, RecordHeader, SType, Schema, SecurityUpdateAction, Side,
    StatMsg, StatType, StatUpdateAction, StatusAction, StatusMsg, StatusReason, SymbolMappingMsg,
    SystemMsg, TradeMsg, TradingEvent, TriState, UserDefinedInstrument, VersionUpgradePolicy,
    DBN_VERSION, FIXED_PRICE_SCALE, UNDEF_ORDER_SIZE, UNDEF_PRICE, UNDEF_STAT_QUANTITY,
    UNDEF_TIMESTAMP,
};

mod dbn_decoder;
mod encode;
mod transcoder;

/// A Python module wrapping dbn functions
#[pymodule] // The name of the function must match `lib.name` in `Cargo.toml`
#[pyo3(name = "_lib")]
fn databento_dbn(_py: Python<'_>, m: &Bound<PyModule>) -> PyResult<()> {
    fn checked_add_class<T: PyClass>(m: &Bound<PyModule>) -> PyResult<()> {
        // ensure a module was specified, otherwise it defaults to builtins
        assert_eq!(T::MODULE.unwrap(), "databento_dbn");
        m.add_class::<T>()
    }
    // all functions exposed to Python need to be added here
    m.add_wrapped(wrap_pyfunction!(encode::update_encoded_metadata))?;
    m.add("DBNError", m.py().get_type::<DBNError>())?;
    checked_add_class::<EnumIterator>(m)?;
    checked_add_class::<Metadata>(m)?;
    checked_add_class::<dbn_decoder::DbnDecoder>(m)?;
    checked_add_class::<transcoder::Transcoder>(m)?;
    // Records
    checked_add_class::<RecordHeader>(m)?;
    checked_add_class::<MboMsg>(m)?;
    checked_add_class::<BidAskPair>(m)?;
    checked_add_class::<ConsolidatedBidAskPair>(m)?;
    checked_add_class::<TradeMsg>(m)?;
    checked_add_class::<Mbp1Msg>(m)?;
    checked_add_class::<Mbp10Msg>(m)?;
    checked_add_class::<OhlcvMsg>(m)?;
    checked_add_class::<ImbalanceMsg>(m)?;
    checked_add_class::<StatusMsg>(m)?;
    checked_add_class::<InstrumentDefMsg>(m)?;
    checked_add_class::<InstrumentDefMsgV1>(m)?;
    checked_add_class::<InstrumentDefMsgV3>(m)?;
    checked_add_class::<ErrorMsg>(m)?;
    checked_add_class::<ErrorMsgV1>(m)?;
    checked_add_class::<SymbolMappingMsg>(m)?;
    checked_add_class::<SymbolMappingMsgV1>(m)?;
    checked_add_class::<SystemMsg>(m)?;
    checked_add_class::<SystemMsgV1>(m)?;
    checked_add_class::<StatMsg>(m)?;
    checked_add_class::<BboMsg>(m)?;
    checked_add_class::<CbboMsg>(m)?;
    checked_add_class::<Cmbp1Msg>(m)?;
    // PyClass enums
    checked_add_class::<Action>(m)?;
    checked_add_class::<Compression>(m)?;
    checked_add_class::<Encoding>(m)?;
    checked_add_class::<InstrumentClass>(m)?;
    checked_add_class::<MatchAlgorithm>(m)?;
    checked_add_class::<RType>(m)?;
    checked_add_class::<SType>(m)?;
    checked_add_class::<Schema>(m)?;
    checked_add_class::<SecurityUpdateAction>(m)?;
    checked_add_class::<Side>(m)?;
    checked_add_class::<StatType>(m)?;
    checked_add_class::<StatUpdateAction>(m)?;
    checked_add_class::<StatusAction>(m)?;
    checked_add_class::<StatusReason>(m)?;
    checked_add_class::<TradingEvent>(m)?;
    checked_add_class::<TriState>(m)?;
    checked_add_class::<UserDefinedInstrument>(m)?;
    checked_add_class::<VersionUpgradePolicy>(m)?;
    // constants
    m.add("DBN_VERSION", DBN_VERSION)?;
    m.add("FIXED_PRICE_SCALE", FIXED_PRICE_SCALE)?;
    m.add("UNDEF_PRICE", UNDEF_PRICE)?;
    m.add("UNDEF_ORDER_SIZE", UNDEF_ORDER_SIZE)?;
    m.add("UNDEF_STAT_QUANTITY", UNDEF_STAT_QUANTITY)?;
    m.add("UNDEF_TIMESTAMP", UNDEF_TIMESTAMP)?;
    m.add("F_LAST", flags::LAST)?;
    m.add("F_TOB", flags::TOB)?;
    m.add("F_SNAPSHOT", flags::SNAPSHOT)?;
    m.add("F_MBP", flags::MBP)?;
    m.add("F_BAD_TS_RECV", flags::BAD_TS_RECV)?;
    m.add("F_MAYBE_BAD_BOOK", flags::MAYBE_BAD_BOOK)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use std::sync::Once;

    use dbn::enums::SType;
    use pyo3::ffi::c_str;

    use super::*;

    pub const TEST_DATA_PATH: &str = concat!(env!("CARGO_MANIFEST_DIR"), "/../tests/data");

    pub static INIT: Once = Once::new();

    pub fn setup() {
        INIT.call_once(|| {
            // add to available modules
            pyo3::append_to_inittab!(databento_dbn);
            // initialize interpreter
            pyo3::prepare_freethreaded_python();
        });
    }

    #[test]
    fn test_metadata_identity() {
        // initialize interpreter
        setup();
        let stype_in = SType::RawSymbol as u8;
        let stype_out = SType::InstrumentId as u8;
        Python::with_gil(|py| {
            pyo3::py_run!(
                  py,
                  stype_in stype_out,
                  r#"from _lib import Metadata, Schema, SType

metadata = Metadata(
    dataset="GLBX.MDP3",
    schema=Schema.MBO,
    start=1,
    stype_in=SType.RAW_SYMBOL,
    stype_out=SType.INSTRUMENT_ID,
    end=2,
    symbols=[],
    partial=[],
    not_found=[],
    mappings=[]
)
metadata_bytes = metadata.encode()
metadata = Metadata.decode(metadata_bytes)
assert metadata.dataset == "GLBX.MDP3"
assert metadata.schema == Schema.MBO
assert metadata.start == 1
assert metadata.end == 2
assert metadata.limit is None
assert metadata.stype_in == SType.RAW_SYMBOL
assert metadata.stype_out == SType.INSTRUMENT_ID
assert metadata.ts_out is False"#
            );
        });
    }

    #[test]
    fn test_dbn_decoder_metadata_error() {
        setup();
        Python::with_gil(|py| {
            py.run(
                c_str!(
                    r#"from _lib import DBNDecoder

decoder = DBNDecoder()
try:
    records = decoder.decode()
    # If this code is called, the test will fail
    assert False
except Exception:
    pass
"#
                ),
                None,
                None,
            )
        })
        .unwrap();
    }
}

```

## High-Level Overview

This file is located at `python/src/lib.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** checked_add_class, databento_dbn, setup, test_dbn_decoder_metadata_error, test_metadata_identity

**Dependencies:** This file imports from 6 modules


#### Detailed Walkthrough


##### Function: `databento_dbn`

```rust
fn databento_dbn(_py: Python<'_>, m: &Bound<PyModule>) -> PyResult<()> {
```


##### Function: `checked_add_class`

```rust
fn checked_add_class<T: PyClass>(m: &Bound<PyModule>) -> PyResult<()> {
```


##### Function: `setup`

```rust
pub fn setup() {
```


##### Function: `test_metadata_identity`

```rust
fn test_metadata_identity() {
```


##### Function: `test_dbn_decoder_metadata_error`

```rust
fn test_dbn_decoder_metadata_error() {
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

