# v1.py

## File Metadata

- **Path:** `python/python/databento_dbn/v1.py`
- **Type:** .py
- **Lines:** 26
- **Characters:** 644
- **Words:** 93
- **Size:** text

## Original Source

```python
# ruff: noqa: F401, F811
from ._lib import BBOMsg
from ._lib import CBBOMsg
from ._lib import CMBP1Msg
from ._lib import ErrorMsgV1 as ErrorMsg
from ._lib import ImbalanceMsg
from ._lib import InstrumentDefMsgV1 as InstrumentDefMsg
from ._lib import MBOMsg
from ._lib import MBP1Msg
from ._lib import MBP10Msg
from ._lib import OHLCVMsg
from ._lib import StatMsg
from ._lib import StatusMsg
from ._lib import SymbolMappingMsgV1 as SymbolMappingMsg
from ._lib import SystemMsgV1 as SystemMsg
from ._lib import TradeMsg


# Aliases
TBBOMsg = MBP1Msg
BBO1SMsg = BBOMsg
BBO1MMsg = BBOMsg
TCBBOMsg = CMBP1Msg
CBBO1SMsg = CBBOMsg
CBBO1MMsg = CBBOMsg

```

## Overview

This file is part of the repository at `python/python/databento_dbn`.

This is a Python source file.

## Detailed Analysis

### Dependencies/Imports (30)

- `._lib`
- `BBOMsg`
- `CBBOMsg`
- `CMBP1Msg`
- `ErrorMsgV1`
- `ImbalanceMsg`
- `InstrumentDefMsgV1`
- `MBOMsg`
- `MBP10Msg`
- `MBP1Msg`
- `OHLCVMsg`
- `StatMsg`
- `StatusMsg`
- `SymbolMappingMsgV1`
- `SystemMsgV1`
- `TradeMsg`

## Performance & Security Notes


## Related Files

- Parent directory: `python/python/databento_dbn/`
- See imported modules in Dependencies section above

## Testing

- Test file location: Not specified

