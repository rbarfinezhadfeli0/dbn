# json_serialize_invalid_dbn_attr.stderr

## File Metadata

- **Path:** `rust/dbn-macros/tests/ui/json_serialize_invalid_dbn_attr.stderr`
- **Type:** .stderr
- **Lines:** 29
- **Characters:** 887
- **Words:** 93
- **Size:** text

## Original Source

```
error: unrecognized dbn attr argument unknown
 --> tests/ui/json_serialize_invalid_dbn_attr.rs:6:11
  |
6 |     #[dbn(unknown)]
  |           ^^^^^^^

error[E0433]: failed to resolve: unresolved import
 --> tests/ui/json_serialize_invalid_dbn_attr.rs:3:10
  |
3 | #[derive(JsonSerialize)]
  |          ^^^^^^^^^^^^^ unresolved import
  |
  = note: this error originates in the derive macro `JsonSerialize` (in Nightly builds, run with -Z macro-backtrace for more info)

error[E0603]: module `serialize` is private
 --> tests/ui/json_serialize_invalid_dbn_attr.rs:3:10
  |
3 | #[derive(JsonSerialize)]
  |          ^^^^^^^^^^^^^
  |          |
  |          private module
  |          trait `WriteField` is not publicly re-exported
  |
note: the module `serialize` is defined here
 --> $WORKSPACE/rust/dbn/src/encode/json.rs
  |
  | pub(crate) mod serialize;
  | ^^^^^^^^^^^^^^^^^^^^^^^^

```

## Overview

This file is part of the repository at `rust/dbn-macros/tests/ui`.

## Detailed Analysis

### Dependencies/Imports (2)

- `-->`
- `|`

## Performance & Security Notes


## Related Files

- Parent directory: `rust/dbn-macros/tests/ui/`
- See imported modules in Dependencies section above

## Testing

This file appears to be a test file.

