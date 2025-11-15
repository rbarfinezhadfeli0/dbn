# Documentation: python/python/databento_dbn/__init__.py

## File Metadata

**Path:** `python/python/databento_dbn/__init__.py`
**Filename:** `__init__.py`
**Extension:** `.py`
**Type:** Text

## Original Source

**Location:** `../../../../python/python/databento_dbn/__init__.py`

### Source Content

```py
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

## High-Level Overview

This file is located at `python/python/databento_dbn/__init__.py` within the repository.

### Language: Python

This is a Python source file, typically used for bindings, scripts, or testing.

#### Key Components


**Classes:** MappingInterval, MappingIntervalDict, SymbolMapping

**Imports:** Protocol, Sequence, TypedDict, collections, datetime, typing


#### Python Integration

This file is part of the Python bindings for the DBN Rust library, enabling Python developers
to work with Databento Binary Encoding format efficiently.

