# Documentation: rust/dbn/src/pretty.rs

## File Metadata

**Path:** `rust/dbn/src/pretty.rs`
**Filename:** `pretty.rs`
**Extension:** `.rs`
**Type:** Text

## Original Source

**Location:** `../../../../rust/dbn/src/pretty.rs`

### Source Content

```rs
//! Contains new types for pretty-printing values found in DBN
//! records.

use std::fmt;

use time::format_description::BorrowedFormatItem;

use crate::FIXED_PRICE_SCALE;

/// A new type for formatting nanosecond UNIX timestamps.
#[derive(Clone, Copy, Default, PartialEq, Eq, PartialOrd, Ord)]
#[repr(transparent)]
pub struct Ts(pub u64);

/// A new type for formatting prices.
#[derive(Clone, Copy, Default, PartialEq, Eq, PartialOrd, Ord)]
#[repr(transparent)]
pub struct Px(pub i64);

impl From<u64> for Ts {
    fn from(value: u64) -> Self {
        Self(value)
    }
}

impl From<i64> for Px {
    fn from(value: i64) -> Self {
        Self(value)
    }
}

impl fmt::Debug for Ts {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.0.fmt(f)
    }
}

impl fmt::Debug for Px {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&fmt_px(self.0))
    }
}

impl fmt::Display for Ts {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&fmt_ts(self.0))
    }
}

impl fmt::Display for Px {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&fmt_px(self.0))
    }
}

/// Converts a fixed-precision price to a decimal string.
pub fn fmt_px(px: i64) -> String {
    if px == crate::UNDEF_PRICE {
        "UNDEF_PRICE".to_owned()
    } else {
        let (sign, px_abs) = if px < 0 { ("-", -px) } else { ("", px) };
        let px_integer = px_abs / FIXED_PRICE_SCALE;
        let px_fraction = px_abs % FIXED_PRICE_SCALE;
        format!("{sign}{px_integer}.{px_fraction:09}")
    }
}

/// Converts a nanosecond UNIX timestamp to a human-readable string in the format
/// `[year]-[month]-[day]T[hour]:[minute]:[second].[subsecond digits:9]Z`.
pub fn fmt_ts(ts: u64) -> String {
    const TS_FORMAT: &[BorrowedFormatItem<'static>] = time::macros::format_description!(
        "[year]-[month]-[day]T[hour]:[minute]:[second].[subsecond digits:9]Z"
    );
    if ts == 0 {
        String::new()
    } else {
        time::OffsetDateTime::from_unix_timestamp_nanos(ts as i128)
            .map_err(|_| ())
            .and_then(|dt| dt.format(TS_FORMAT).map_err(|_| ()))
            .unwrap_or_else(|_| ts.to_string())
    }
}

/// Converts a fixed-precision price to a floating point.
///
/// `UNDEF_PRICE` will be converted to NaN.
pub fn px_to_f64(px: i64) -> f64 {
    if px == crate::UNDEF_PRICE {
        f64::NAN
    } else {
        px as f64 / FIXED_PRICE_SCALE as f64
    }
}

#[cfg(test)]
mod tests {
    use crate::UNDEF_PRICE;

    use super::*;

    #[test]
    fn test_fmt_px_negative() {
        assert_eq!(fmt_px(-100_000), "-0.000100000");
    }

    #[test]
    fn test_fmt_px_positive() {
        assert_eq!(fmt_px(32_500_000_000), "32.500000000");
    }

    #[test]
    fn test_fmt_px_zero() {
        assert_eq!(fmt_px(0), "0.000000000");
    }

    #[test]
    fn test_fmt_px_undef() {
        assert_eq!(fmt_px(UNDEF_PRICE), "UNDEF_PRICE");
    }

    #[test]
    fn test_fmt_ts_0() {
        assert!(fmt_ts(0).is_empty());
    }

    #[test]
    fn test_fmt_ts_1() {
        assert_eq!(fmt_ts(1), "1970-01-01T00:00:00.000000001Z");
    }

    #[test]
    fn test_fmt_ts_future() {
        assert_eq!(
            fmt_ts(1622838300000000000),
            "2021-06-04T20:25:00.000000000Z"
        );
    }
}

```

## High-Level Overview

This file is located at `rust/dbn/src/pretty.rs` within the repository.

### Language: Rust

This is a Rust source file, part of the DBN (Databento Binary Encoding) library ecosystem.

#### Key Components


**Functions defined:** fmt, fmt_px, fmt_ts, from, px_to_f64, test_fmt_px_negative, test_fmt_px_positive, test_fmt_px_undef, test_fmt_px_zero, test_fmt_ts_0, test_fmt_ts_1, test_fmt_ts_future

**Structs defined:** Px, Ts

**Dependencies:** This file imports from 5 modules


#### Detailed Walkthrough


##### Function: `from`

```rust
fn from(value: u64) -> Self {
```


##### Function: `from`

```rust
fn from(value: i64) -> Self {
```


##### Function: `fmt`

```rust
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
```


##### Function: `fmt`

```rust
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
```


##### Function: `fmt`

```rust
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
```


##### Function: `fmt`

```rust
fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
```


##### Function: `fmt_px`

```rust
pub fn fmt_px(px: i64) -> String {
```


##### Function: `fmt_ts`

```rust
pub fn fmt_ts(ts: u64) -> String {
```


##### Function: `px_to_f64`

```rust
pub fn px_to_f64(px: i64) -> f64 {
```


##### Function: `test_fmt_px_negative`

```rust
fn test_fmt_px_negative() {
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

