# Documentation: rust/dbn-macros/tests/ui/csv_serialize_duplicate_encode_orders.stderr

## File Metadata

**Path:** `rust/dbn-macros/tests/ui/csv_serialize_duplicate_encode_orders.stderr`
**Filename:** `csv_serialize_duplicate_encode_orders.stderr`
**Extension:** `.stderr`
**Type:** Text

## Original Source

**Location:** `../../../../../rust/dbn-macros/tests/ui/csv_serialize_duplicate_encode_orders.stderr`

### Source Content

```stderr
error: Specified duplicate encode order `1` for field
  --> tests/ui/csv_serialize_duplicate_encode_orders.rs:9:5
   |
9  | /     #[dbn(encode_order(1))]
10 | |     pub c: u8,
   | |_____________^

```

## High-Level Overview

This file is located at `rust/dbn-macros/tests/ui/csv_serialize_duplicate_encode_orders.stderr` within the repository.

### File Overview

This file is part of the repository's supporting infrastructure or data.

