# Documentation: c/src/compat.rs

## File Metadata

**Path:** `c/src/compat.rs`
**Filename:** `compat.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../c/src/compat.rs`

### Source Content

```rs
use dbn::{
    compat::{ErrorMsgV1, InstrumentDefMsgV1, InstrumentDefMsgV3, SymbolMappingMsgV1, SystemMsgV1},
    ErrorMsg, InstrumentDefMsg, SymbolMappingMsg, SystemMsg,
};

/// Converts an V1 ErrorMsg to V2.
#[no_mangle]
pub extern "C" fn from_error_v1_to_v2(def_v1: &ErrorMsgV1) -> ErrorMsg {
    ErrorMsg::from(def_v1)
}

/// Converts an V1 InstrumentDefMsg to V2.
#[no_mangle]
pub extern "C" fn from_instrument_def_v1_to_v2(def_v1: &InstrumentDefMsgV1) -> InstrumentDefMsg {
    InstrumentDefMsg::from(def_v1)
}

/// Converts a V1 InstrumentDefMsg to V3.
#[no_mangle]
pub extern "C" fn from_instrument_def_v1_to_v3(def_v1: &InstrumentDefMsgV1) -> InstrumentDefMsgV3 {
    InstrumentDefMsgV3::from(def_v1)
}

/// Converts a V2 InstrumentDefMsg to V3.
#[no_mangle]
pub extern "C" fn from_instrument_def_v2_to_v3(def_v2: &InstrumentDefMsg) -> InstrumentDefMsgV3 {
    InstrumentDefMsgV3::from(def_v2)
}

/// Converts an V1 SymbolMappingMsg to V2.
#[no_mangle]
pub extern "C" fn from_symbol_mapping_v1_to_v2(def_v1: &SymbolMappingMsgV1) -> SymbolMappingMsg {
    SymbolMappingMsg::from(def_v1)
}

/// Converts an V1 SystemMsg to V2.
#[no_mangle]
pub extern "C" fn from_system_v1_to_v2(def_v1: &SystemMsgV1) -> SystemMsg {
    SystemMsg::from(def_v1)
}

```

## High-Level Overview

This file is located at `c/src/compat.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** from_error_v1_to_v2, from_instrument_def_v1_to_v2, from_instrument_def_v1_to_v3, from_instrument_def_v2_to_v3, from_symbol_mapping_v1_to_v2, from_system_v1_to_v2

**Dependencies:** This file imports from 1 modules


#### Detailed Walkthrough


##### Function: `from_error_v1_to_v2`

```rust
fn from_error_v1_to_v2(def_v1: &ErrorMsgV1) -> ErrorMsg {
```


##### Function: `from_instrument_def_v1_to_v2`

```rust
fn from_instrument_def_v1_to_v2(def_v1: &InstrumentDefMsgV1) -> InstrumentDefMsg {
```


##### Function: `from_instrument_def_v1_to_v3`

```rust
fn from_instrument_def_v1_to_v3(def_v1: &InstrumentDefMsgV1) -> InstrumentDefMsgV3 {
```


##### Function: `from_instrument_def_v2_to_v3`

```rust
fn from_instrument_def_v2_to_v3(def_v2: &InstrumentDefMsg) -> InstrumentDefMsgV3 {
```


##### Function: `from_symbol_mapping_v1_to_v2`

```rust
fn from_symbol_mapping_v1_to_v2(def_v1: &SymbolMappingMsgV1) -> SymbolMappingMsg {
```


##### Function: `from_system_v1_to_v2`

```rust
fn from_system_v1_to_v2(def_v1: &SystemMsgV1) -> SystemMsg {
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

