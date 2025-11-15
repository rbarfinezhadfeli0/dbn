# README.md

## File Metadata

- **Path:** `rust/dbn/README.md`
- **Type:** .md
- **Lines:** 43
- **Characters:** 1,389
- **Words:** 111
- **Size:** text

## Original Source

```markdown
# dbn

[![build](https://github.com/databento/dbn/actions/workflows/build.yaml/badge.svg)](https://github.com/databento/dbn/actions/workflows/build.yaml)
[![Documentation](https://img.shields.io/docsrs/dbn)](https://docs.rs/dbn/latest/dbn/)
![license](https://img.shields.io/github/license/databento/dbn?color=blue)
[![Current Crates.io Version](https://img.shields.io/crates/v/dbn.svg)](https://crates.io/crates/dbn)

The official crate for working with Databento Binary Encoding (DBN).
For more information about DBN, read our [introduction to DBN](https://databento.com/docs/standards-and-conventions/databento-binary-encoding).

Check out the [databento crate](https://crates.io/crates/databento) for the official Databento Rust client.

## Installation

To add the crate to an existing project, run the following command:
```sh
cargo add dbn
```

## Usage

To read a DBN file with MBO data and print each row:
```rust
use dbn::{
    decode::dbn::Decoder,
    record::MboMsg,
};
use streaming_iterator::StreamingIterator;

let mut dbn_stream = Decoder::from_zstd_file("20201228.dbn.zst")?.decode_stream::<MboMsg>()?;
while let Some(mbo_msg) = dbn_stream.next() {
    println!("{mbo_msg:?}");
}
```

## Documentation

See [the docs](https://docs.rs/dbn) for more detailed usage.

## License

Distributed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0.html).

```

## Overview

This file is part of the repository at `rust/dbn`.

This is a README file providing documentation and instructions for this component.

## Detailed Analysis

### Dependencies/Imports (2)

- `dbn::{`
- `streaming_iterator::StreamingIterator`

## Performance & Security Notes


## Related Files

- Parent directory: `rust/dbn/`
- See imported modules in Dependencies section above

## Testing

- Test file location: Not specified

