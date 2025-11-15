# v1.rs

## File Metadata

- **Path:** `rust/dbn/src/v1.rs`
- **Type:** .rs
- **Lines:** 116
- **Characters:** 3,244
- **Words:** 242
- **Size:** text

## Original Source

```rust
//! Record data types for encoding different Databento [`Schema`](crate::enums::Schema)s
//! in DBN version 1.

pub use crate::compat::ErrorMsgV1 as ErrorMsg;
pub use crate::compat::InstrumentDefMsgV1 as InstrumentDefMsg;
use crate::compat::InstrumentDefRec;
pub use crate::compat::SymbolMappingMsgV1 as SymbolMappingMsg;
pub use crate::compat::SystemMsgV1 as SystemMsg;
pub use crate::compat::SYMBOL_CSTR_LEN_V1 as SYMBOL_CSTR_LEN;
pub use crate::record::{
    Bbo1MMsg, Bbo1SMsg, BboMsg, Cbbo1MMsg, Cbbo1SMsg, CbboMsg, Cmbp1Msg, ImbalanceMsg, MboMsg,
    OhlcvMsg, StatMsg, StatusMsg, TbboMsg, TcbboMsg, TradeMsg, WithTsOut,
};

mod impl_default;
mod methods;

use crate::compat::SymbolMappingRec;

impl SymbolMappingRec for SymbolMappingMsg {
    fn stype_in_symbol(&self) -> crate::Result<&str> {
        Self::stype_in_symbol(self)
    }

    fn stype_out_symbol(&self) -> crate::Result<&str> {
        Self::stype_out_symbol(self)
    }

    fn start_ts(&self) -> Option<time::OffsetDateTime> {
        Self::start_ts(self)
    }

    fn end_ts(&self) -> Option<time::OffsetDateTime> {
        Self::end_ts(self)
    }
}

impl InstrumentDefRec for InstrumentDefMsg {
    fn raw_symbol(&self) -> crate::Result<&str> {
        Self::raw_symbol(self)
    }

    fn asset(&self) -> crate::Result<&str> {
        Self::asset(self)
    }

    fn security_type(&self) -> crate::Result<&str> {
        Self::security_type(self)
    }

    fn security_update_action(&self) -> crate::Result<crate::SecurityUpdateAction> {
        Ok(self.security_update_action)
    }

    fn channel_id(&self) -> u16 {
        self.channel_id
    }
}

#[cfg(test)]
mod tests {
    use std::mem;

    use rstest::*;
    use type_layout::{Field, TypeLayout};

    use crate::v2;

    use super::*;

    #[test]
    fn test_default_equivalency() {
        assert_eq!(
            v2::InstrumentDefMsg::from(&InstrumentDefMsg::default()),
            v2::InstrumentDefMsg::default()
        );
    }

    #[cfg(feature = "python")]
    #[test]
    fn test_strike_price_order_didnt_change() {
        use crate::python::PyFieldDesc;

        assert_eq!(
            InstrumentDefMsg::ordered_fields(""),
            v2::InstrumentDefMsg::ordered_fields("")
        );
    }

    #[rstest]
    #[case::definition(InstrumentDefMsg::default(), 360)]
    #[case::error(ErrorMsg::default(), 80)]
    #[case::symbol_mapping(SymbolMappingMsg::default(), 80)]
    #[case::system(SystemMsg::default(), 80)]
    fn test_sizes<R: Sized>(#[case] _rec: R, #[case] exp: usize) {
        assert_eq!(mem::size_of::<R>(), exp);
        assert!(mem::size_of::<R>() <= crate::MAX_RECORD_LEN);
    }

    #[rstest]
    #[case::definition(InstrumentDefMsg::default())]
    #[case::error(ErrorMsg::default())]
    #[case::symbol_mapping(SymbolMappingMsg::default())]
    #[case::system(SystemMsg::default())]
    fn test_alignment_and_no_padding<R: TypeLayout>(#[case] _rec: R) {
        let layout = R::type_layout();
        assert_eq!(layout.alignment, 8, "Unexpected alignment: {layout}");
        for field in layout.fields.iter() {
            assert!(
                matches!(field, Field::Field { .. }),
                "Detected padding: {layout}"
            );
        }
    }
}

```

## Overview

This file is part of the repository at `rust/dbn/src`.

This is a Rust source file.

## Detailed Analysis

### Functions (13)

- `stype_in_symbol()`
- `stype_out_symbol()`
- `start_ts()`
- `end_ts()`
- `raw_symbol()`
- `asset()`
- `security_type()`
- `security_update_action()`
- `channel_id()`
- `test_default_equivalency()`
- `test_strike_price_order_didnt_change()`
- `test_sizes()`
- `test_alignment_and_no_padding()`

### Dependencies/Imports (14)

- `crate::compat::ErrorMsgV1`
- `crate::compat::InstrumentDefMsgV1`
- `crate::compat::InstrumentDefRec`
- `crate::compat::SYMBOL_CSTR_LEN_V1`
- `crate::compat::SymbolMappingMsgV1`
- `crate::compat::SymbolMappingRec`
- `crate::compat::SystemMsgV1`
- `crate::python::PyFieldDesc`
- `crate::record::{`
- `crate::v2`
- `rstest::*`
- `std::mem`
- `super::*`
- `type_layout::{Field,`

## Performance & Security Notes


## Related Files

- Parent directory: `rust/dbn/src/`
- See imported modules in Dependencies section above

## Testing

- Test file location: Not specified

