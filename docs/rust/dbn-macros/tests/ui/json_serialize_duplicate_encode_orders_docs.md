# json_serialize_duplicate_encode_orders.stderr

## File Metadata

- **Path:** `rust/dbn-macros/tests/ui/json_serialize_duplicate_encode_orders.stderr`
- **Type:** .stderr
- **Lines:** 7
- **Characters:** 198
- **Words:** 23
- **Size:** text

## Original Source

```
error: Specified duplicate encode order `1` for field
  --> tests/ui/json_serialize_duplicate_encode_orders.rs:9:5
   |
9  | /     #[dbn(encode_order(1))]
10 | |     pub c: u8,
   | |_____________^

```

## Overview

This file is part of the repository at `rust/dbn-macros/tests/ui`.

## Detailed Analysis

## Performance & Security Notes


## Related Files

- Parent directory: `rust/dbn-macros/tests/ui/`

## Testing

This file appears to be a test file.

