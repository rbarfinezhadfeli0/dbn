# __init__.py

## File Metadata

- **Path:** `python/python/databento_dbn/__init__.py`
- **Type:** .py
- **Lines:** 57
- **Characters:** 1,123
- **Words:** 138
- **Size:** text

## Original Source

```python
import datetime as dt
from collections.abc import Sequence
from typing import Protocol
from typing import TypedDict

# Import native module
from ._lib import *  # noqa: F403


class MappingInterval(Protocol):
    """
    Represents a symbol mapping over a start and end date range interval.

    Parameters
    ----------
    start_date : dt.date
        The start of the mapping period.
    end_date : dt.date
        The end of the mapping period.
    symbol : str
        The symbol value.

    """

    start_date: dt.date
    end_date: dt.date
    symbol: str


class MappingIntervalDict(TypedDict):
    """
    Represents a symbol mapping over a start and end date range interval.

    Parameters
    ----------
    start_date : dt.date
        The start of the mapping period.
    end_date : dt.date
        The end of the mapping period.
    symbol : str
        The symbol value.

    """

    start_date: dt.date
    end_date: dt.date
    symbol: str


class SymbolMapping(Protocol):
    """
    Represents the mappings for one native symbol.
    """

    raw_symbol: str
    intervals: Sequence[MappingInterval]

```

## Overview

This file is part of the repository at `python/python/databento_dbn`.

This is a Python source file.

## Detailed Analysis

### Classes (3)

- `MappingInterval`
- `MappingIntervalDict`
- `SymbolMapping`

### Dependencies/Imports (9)

- `*`
- `._lib`
- `Protocol`
- `Sequence`
- `TypedDict`
- `collections.abc`
- `datetime`
- `typing`

## Performance & Security Notes


## Related Files

- Parent directory: `python/python/databento_dbn/`
- See imported modules in Dependencies section above

## Testing

- Test file location: Not specified

