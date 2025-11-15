# compat.rs

## File Metadata

- **Path:** `c/src/compat.rs`
- **Type:** .rs
- **Lines:** 41
- **Characters:** 1,253
- **Words:** 126
- **Size:** text

## Original Source

```rust
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

## Overview

This file is part of the repository at `c/src`.

This is a Rust source file.

## Detailed Analysis

### Functions (6)

- `from_error_v1_to_v2()`
- `from_instrument_def_v1_to_v2()`
- `from_instrument_def_v1_to_v3()`
- `from_instrument_def_v2_to_v3()`
- `from_symbol_mapping_v1_to_v2()`
- `from_system_v1_to_v2()`

### Dependencies/Imports (1)

- `dbn::{`

## Performance & Security Notes


## Related Files

- Parent directory: `c/src/`
- See imported modules in Dependencies section above

## Testing

- Test file location: Not specified

