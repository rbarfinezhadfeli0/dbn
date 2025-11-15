# Documentation: python/python/databento_dbn/_lib.pyi

## File Metadata

**Path:** `python/python/databento_dbn/_lib.pyi`
**Filename:** `_lib.pyi`
**Extension:** `.pyi`
**Type:** Text

## Original Source

**Location:** `../../../../python/python/databento_dbn/_lib.pyi`

### Source Content

```pyi
# ruff: noqa: UP007 PYI021 PYI053 PYI011
from __future__ import annotations

import datetime as dt
from collections.abc import Iterable
from collections.abc import Sequence
from enum import Enum
from typing import BinaryIO
from typing import ClassVar
from typing import Optional
from typing import SupportsBytes
from typing import TextIO
from typing import Union

from databento_dbn import MappingIntervalDict
from databento_dbn import SymbolMapping

DBN_VERSION: int
FIXED_PRICE_SCALE: int
UNDEF_PRICE: int
UNDEF_ORDER_SIZE: int
UNDEF_STAT_QUANTITY: int
UNDEF_TIMESTAMP: int

_DBNRecord = Union[
    Metadata,
    MBOMsg,
    MBP1Msg,
    BBOMsg,
    CMBP1Msg,
    CBBOMsg,
    MBP10Msg,
    OHLCVMsg,
    TradeMsg,
    InstrumentDefMsg,
    InstrumentDefMsgV1,
    InstrumentDefMsgV3,
    ImbalanceMsg,
    ErrorMsg,
    ErrorMsgV1,
    SymbolMappingMsg,
    SymbolMappingMsgV1,
    SystemMsg,
    SystemMsgV1,
    StatMsg,
    StatusMsg,
]

class DBNError(Exception):
    """
    An exception from databento_dbn Rust code.
    """

class Side(Enum):
    """
    A side of the market. The side of the market for resting orders, or the side
    of the aggressor for trades.

    ASK
        A sell order or sell aggressor in a trade.
    BID
        A buy order or a buy aggressor in a trade.
    NONE
        No side specified by the original source.

    """

    ASK: str
    BID: str
    NONE: str

    @classmethod
    def from_str(cls, value: str) -> Side: ...
    @classmethod
    def variants(cls) -> Iterable[Side]: ...

class Action(Enum):
    """
    A tick action.

    MODIFY
        An existing order was modified.
    TRADE
        A trade executed.
    FILL
        An existing order was filled.
    CANCEL
        An order was cancelled.
    ADD
        A new order was added.
    CLEAR
        Reset the book; clear all orders for an instrument.
    NONE
        Has no effect on the book, but may carry `flags` or other information.
    """

    MODIFY: str
    TRADE: str
    FILL: str
    CANCEL: str
    ADD: str
    CLEAR: str
    NONE: str

    @classmethod
    def from_str(cls, value: str) -> Action: ...
    @classmethod
    def variants(cls) -> Iterable[Action]: ...

class InstrumentClass(Enum):
    """
    The class of instrument.

    BOND
        A bond.
    CALL
        A call option.
    FUTURE
        A future.
    STOCK
        A stock.
    MIXED_SPREAD
        A spread composed of multiple instrument classes.
    PUT
        A put option.
    FUTURE_SPREAD
        A spread composed of futures.
    OPTION_SPREAD
        A spread composed of options.
    FX_SPOT
        A foreign exchange spot.
    COMMODITY_SPOT
        A commodity being traded for immediate delivery.

    """

    BOND: str
    CALL: str
    FUTURE: str
    STOCK: str
    MIXED_SPREAD: str
    PUT: str
    FUTURE_SPREAD: str
    OPTION_SPREAD: str
    FX_SPOT: str
    COMMODITY_SPOT: str

    @classmethod
    def from_str(cls, value: str) -> InstrumentClass: ...
    @classmethod
    def variants(cls) -> Iterable[InstrumentClass]: ...

class MatchAlgorithm(Enum):
    """
    The type of matching algorithm used for the instrument at the exchange.


    UNDEFINED
        No matching algorithm was specified.
    FIFO
        First-in-first-out matching.
    CONFIGURABLE
        A configurable match algorithm.
    PRO_RATA
        Trade quantity is allocated to resting orders based on a pro-rata percentage: resting order quantity divided by total quantity.
    FIFO_LMM
        Like `FIFO` but with LMM allocations prior to FIFO allocations.
    THRESHOLD_PRO_RATA
        Like `PRO_RATA` but includes a configurable allocation to the first order that improves the market.
    FIFO_TOP_LMM
        Like `FIFO_LMM` but includes a configurable allocation to the first order that improves the market.
    THRESHOLD_PRO_RATA_LMM
        Like `THRESHOLD_PRO_RATA` but includes a special priority to LMMs.
    EURODOLLAR_FUTURES
        Special variant used only for Eurodollar futures on CME.
    TIME_PRO_RATA
        Trade quantity is shared between all orders at the best price. Orders with the
        highest time priority receive a higher matched quantity.
    """

    UNDEFINED: str
    FIFO: str
    CONFIGURABLE: str
    PRO_RATA: str
    FIFO_LMM: str
    THRESHOLD_PRO_RATA: str
    FIFO_TOP_LMM: str
    THRESHOLD_PRO_RATA_LMM: str
    EURODOLLAR_FUTURES: str
    TIME_PRO_RATA: str

    @classmethod
    def from_str(cls, value: str) -> MatchAlgorithm: ...
    @classmethod
    def variants(cls) -> Iterable[MatchAlgorithm]: ...

class UserDefinedInstrument(Enum):
    """
    Whether the instrument is user-defined.

    NO
        The instrument is not user-defined.
    YES
        The instrument is user-defined.

    """

    NO: str
    YES: str

    @classmethod
    def from_str(cls, value: str) -> UserDefinedInstrument: ...
    @classmethod
    def variants(cls) -> Iterable[UserDefinedInstrument]: ...

class SType(Enum):
    """
    A DBN symbology type.

    INSTRUMENT_ID
        Symbology using a unique numeric ID.
    RAW_SYMBOL
        Symbology using the original symbols provided by the publisher.
    CONTINUOUS
        A Databento-specific symbology where one symbol may point to different
        instruments at different points of time, e.g. to always refer to the front month
        future.
    PARENT
        A Databento-specific symbology for referring to a group of symbols by one
        "parent" symbol, e.g. ES.FUT to refer to all ES futures.
    NASDAQ_SYMBOL
        Symbology for US equities using NASDAQ Integrated suffix conventions.
    CMS_SYMBOL
        Symbology for US equities using CMS suffix conventions.
    ISIN
        Symbology using International Security Identification Numbers (ISIN) - ISO 6166.
    US_CODE
        Symbology using US domestic Committee on Uniform Securities Identification Procedure (CUSIP) codes.
    BBG_COMP_ID
        Symbology using Bloomberg composite global IDs.
    BBG_COMP_TICKER
        Symbology using Bloomberg composite tickers.
    FIGI
        Symbology using Bloomberg FIGI exchange level IDs.
    FIGI_TICKER
        Symbology using Bloomberg exchange level tickers.

    """

    INSTRUMENT_ID: str
    RAW_SYMBOL: str
    CONTINUOUS: str
    PARENT: str
    NASDAQ_SYMBOL: str
    CMS_SYMBOL: str
    ISIN: str
    US_CODE: str
    BBG_COMP_ID: str
    BBG_COMP_TICKER: str
    FIGI: str
    FIGI_TICKER: str

    @classmethod
    def from_str(cls, value: str) -> SType: ...
    @classmethod
    def variants(cls) -> Iterable[SType]: ...

class RType(Enum):
    """
    A DBN record type.

    MBP0
        Denotes a market-by-price record with a book depth of 0 (used for the `Trades` schema).
    MBP1
        Denotes a market-by-price record with a book depth of 1 (also used for the
        `Tbbo` schema).
    MBP10
        Denotes a market-by-price record with a book depth of 10.
    OHLCV_DEPRECATED
        Denotes an open, high, low, close, and volume record at an unspecified cadence.
    OHLCV_1S
        Denotes an open, high, low, close, and volume record at a 1-second cadence.
    OHLCV_1M
        Denotes an open, high, low, close, and volume record at a 1-minute cadence.
    OHLCV_1H
        Denotes an open, high, low, close, and volume record at an hourly cadence.
    OHLCV_1D
        Denotes an open, high, low, close, and volume record at a daily cadence
        based on the UTC date.
    OHLCV_EOD
        Denotes an open, high, low, close, and volume record at a daily cadence
        based on the end of the trading session.
    STATUS
        Denotes an exchange status record.
    INSTRUMENT_DEF
        Denotes an instrument definition record.
    IMBALANCE
        Denotes an order imbalance record.
    ERROR
        Denotes an error from gateway.
    SYMBOL_MAPPING
        Denotes a symbol mapping record.
    SYSTEM
        Denotes a non-error message from the gateway. Also used for heartbeats.
    STATISTICS
        Denotes a statistics record from the publisher (not calculated by Databento).
    MBO
        Denotes a market by order record.
    CBBO
        Denotes a consolidated best bid and offer record.
    CBBO_1S
        Denotes a consolidated best bid and offer record.
    CBBO_1M
        Denotes a consolidated best bid and offer record subsampled on a one-minute
        interval.
    TCBBO
        Denotes a consolidated best bid and offer trade record containing the
        consolidated BBO before the trade.
    BBO_1S
        Denotes a best bid and offer record subsampled on a one-second interval.
    BBO_1M
        Denotes a best bid and offer record subsampled on a one-minute interval.

    """  # noqa: D405, D411

    @classmethod
    def from_int(cls, value: int) -> RType: ...
    @classmethod
    def from_schema(cls, value: Schema) -> RType: ...
    @classmethod
    def from_str(cls, value: str) -> RType: ...
    @classmethod
    def variants(cls) -> Iterable[RType]: ...

class Schema(Enum):
    """
    A DBN record schema.

    MBO
        Market by order.
    MBP_1
        Market by price with a book depth of 1.
    MBP_10
        Market by price with a book depth of 10.
    TBBO
        All trade events with the best bid and offer (BBO) immediately before the effect of the trade.
    TRADES
        All trade events.
    OHLCV_1S
        Open, high, low, close, and volume at a one-second interval.
    OHLCV_1M
        Open, high, low, close, and volume at a one-minute interval.
    OHLCV_1H
        Open, high, low, close, and volume at an hourly interval.
    OHLCV_1D
        Open, high, low, close, and volume at a daily interval.
    OHLCV_EOD
        Open, high, low, close, and volume at a daily cadence based on the end of the trading session.
    DEFINITION
        Instrument definitions.
    STATISTICS
        Additional data disseminated by publishers.
    STATUS
        Exchange status.
    IMBALANCE
        Auction imbalance events.
    CMBP_1
        Consolidated best bid and offer.
    CBBO_1S
        Consolidated best bid and offer record.
    CBBO_1M
        Consolidated best bid and offer record subsampled on a one-second interval.
    TCBBO
        Consolidated best bid and offer record subsampled on a one-minute interval.
    BBO_1S
        Consolidated best bid and offer trade record containing the consolidated BBO before the trade.
    BBO_1M
        Best bid and offer record subsampled on a one-second interval.

    """

    MBO: str
    MBP_1: str
    MBP_10: str
    TBBO: str
    TRADES: str
    OHLCV_1S: str
    OHLCV_1M: str
    OHLCV_1H: str
    OHLCV_1D: str
    OHLCV_EOD: str
    DEFINITION: str
    STATISTICS: str
    STATUS: str
    IMBALANCE: str
    CMBP_1: str
    CBBO_1S: str
    CBBO_1M: str
    TCBBO: str
    BBO_1S: str
    BBO_1M: str

    @classmethod
    def from_str(cls, value: str) -> Schema: ...
    @classmethod
    def variants(cls) -> Iterable[Schema]: ...

class Encoding(Enum):
    """
    Data output encoding.

    DBN
        Databento Binary Encoding.
    CSV
        Comma-separated values.
    JSON
        JavaScript object notation.

    """

    DBN: str
    CSV: str
    JSON: str

    @classmethod
    def from_str(cls, value: str) -> Encoding: ...
    @classmethod
    def variants(cls) -> Iterable[Encoding]: ...

class Compression(Enum):
    """
    Data compression format.

    NONE
        Uncompressed.
    ZSTD
        Zstandard compressed.

    """

    NONE: str
    ZSTD: str

    @classmethod
    def from_str(cls, value: str) -> Compression: ...
    @classmethod
    def variants(cls) -> Iterable[Compression]: ...

class SecurityUpdateAction(Enum):
    """
    The type of definition update.

    ADD
        A new instrument definition.
    MODIFY
        A modified instrument definition of an existing one.
    DELETE
        Removal of an instrument definition.
    INVALID
        Deprecated

    """

    ADD: str
    MODIFY: str
    DELETE: str
    INVALID: str

    @classmethod
    def from_str(cls, value: str) -> SecurityUpdateAction: ...
    @classmethod
    def variants(cls) -> Iterable[SecurityUpdateAction]: ...

class StatType(Enum):
    """
    The type of statistic contained in a `StatMsg`.

    OPENING_PRICE
        The price of the first trade of an instrument. `price` will be set.
        `quantity` will be set when provided by the venue.
    INDICATIVE_OPENING_PRICE
        The probable price of the first trade of an instrument published during pre- open. Both
        `price` and `quantity` will be set.
    SETTLEMENT_PRICE
        The settlement price of an instrument. `price` will be set and `flags` indicate whether the
        price is final or preliminary and actual or theoretical. `ts_ref` will indicate the trading
        date of the settlement price.
    TRADING_SESSION_LOW_PRICE
        The lowest trade price of an instrument during the trading session. `price` will be set.
    TRADING_SESSION_HIGH_PRICE
        The highest trade price of an instrument during the trading session. `price` will be set.
    CLEARED_VOLUME
        The number of contracts cleared for an instrument on the previous trading date. `quantity`
        will be set. `ts_ref` will indicate the trading date of the volume.
    LOWEST_OFFER
        The lowest offer price for an instrument during the trading session. `price` will be set.
    HIGHEST_BID
        The highest bid price for an instrument during the trading session. `price` will be set.
    OPEN_INTEREST
        The current number of outstanding contracts of an instrument. `quantity` will be set.
        `ts_ref` will indicate the trading date for which the open interest was calculated.
    FIXING_PRICE
        The volume-weighted average price (VWAP) for a fixing period. `price` will be set.
    CLOSE_PRICE
        The last trade price during a trading session. `price` will be set.
        `quantity` will be set when provided by the venue.
    NET_CHANGE
        The change in price from the close price of the previous trading session to the most recent
        trading session. `price` will be set.
    VWAP
        The volume-weighted average price (VWAP) during the trading session. `price` will be set to
        the VWAP while `quantity` will be the traded volume.
    VOLATILITY
        The implied volatility associated with the settlement price.
    DELTA
        The option delta associated with the settlement price.
    UNCROSSING_PRICE
        The auction uncrossing price. This is used for auctions that are neither the
        official opening auction nor the official closing auction. `price` will be set.
        `quantity` will be set when provided by the venue.

    """

    OPENING_PRICE: int
    INDICATIVE_OPENING_PRICE: int
    SETTLEMENT_PRICE: int
    TRADING_SESSION_LOW_PRICE: int
    TRADING_SESSION_HIGH_PRICE: int
    CLEARED_VOLUME: int
    LOWEST_OFFER: int
    HIGHEST_BID: int
    OPEN_INTEREST: int
    FIXING_PRICE: int
    CLOSE_PRICE: int
    NET_CHANGE: int
    VWAP: int
    VOLATILITY: int
    DELTA: int
    UNCROSSING_PRICE: int

    @classmethod
    def variants(cls) -> Iterable[StatType]: ...

class StatUpdateAction(Enum):
    """
    The type of `StatMsg` update.

    NEW
        A new statistic.
    DELETE
        A removal of a statistic.

    """

    NEW: str
    DELETE: str

    @classmethod
    def from_str(cls, value: str) -> StatUpdateAction: ...
    @classmethod
    def variants(cls) -> Iterable[StatUpdateAction]: ...

class StatusAction(Enum):
    """
    The primary enum for the type of `StatusMsg` update.

    NONE
        No change.
    PRE_OPEN
        The instrument is in a pre-open period.
    PRE_CROSS
        The instrument is in a pre-cross period.
    QUOTING
        The instrument is quoting but not trading.
    CROSS
        The instrument is in a cross/auction.
    ROTATION
        The instrument is being opened through a trading rotation.
    NEW_PRICE_INDICATION
        A new price indication is available for the instrument.
    TRADING
        The instrument is trading.
    HALT
        Trading in the instrument has been halted.
    PAUSE
        Trading in the instrument has been paused.
    SUSPEND
        Trading in the instrument has been suspended.
    PRE_CLOSE
        The instrument is in a pre-close period.
    CLOSE
        Trading in the instrument has closed.
    POST_CLOSE
        The instrument is in a post-close period.
    SSR_CHANGE
        A change in short-selling restrictions.
    NOT_AVAILABLE_FOR_TRADING
        The instrument is not available for trading, either trading has closed or been halted.

    """

    NONE: int
    PRE_OPEN: int
    PRE_CROSS: int
    QUOTING: int
    CROSS: int
    ROTATION: int
    NEW_PRICE_INDICATION: int
    TRADING: int
    HALT: int
    PAUSE: int
    SUSPEND: int
    PRE_CLOSE: int
    CLOSE: int
    POST_CLOSE: int
    SSR_CHANGE: int
    NOT_AVAILABLE_FOR_TRADING: int

    @classmethod
    def variants(cls) -> Iterable[StatusAction]: ...

class StatusReason(Enum):
    """
    The secondary enum for a `StatusMsg` update, explains the cause of a halt or other change in
    `action`.

    NONE
        No reason is given.
    SCHEDULED
        The change in status occurred as scheduled.
    SURVEILLANCE_INTERVENTION
        The instrument stopped due to a market surveillance intervention.
    MARKET_EVENT
        The status changed due to activity in the market.
    INSTRUMENT_ACTIVATION
        The derivative instrument began trading.
    INSTRUMENT_EXPIRATION
        The derivative instrument expired.
    RECOVERY_IN_PROCESS
        Recovery in progress.
    REGULATORY
        The status change was caused by a regulatory action.
    ADMINISTRATIVE
        The status change was caused by an administrative action.
    NON_COMPLIANCE
        The status change was caused by the issuer not being compliance with regulatory
        requirements.
    FILINGS_NOT_CURRENT
        Trading halted because the issuer's filings are not current.
    SEC_TRADING_SUSPENSION
        Trading halted due to an SEC trading suspension.
    NEW_ISSUE
        The status changed because a new issue is available.
    ISSUE_AVAILABLE
        The status changed because an issue is available.
    ISSUES_REVIEWED
        The status changed because the issue(s) were reviewed.
    FILING_REQS_SATISFIED
        The status changed because the filing requirements were satisfied.
    NEWS_PENDING
        Relevant news is pending.
    NEWS_RELEASED
        Relevant news was released.
    NEWS_AND_RESUMPTION_TIMES
        The news has been fully disseminated and times are available for the resumption in quoting
        and trading.
    NEWS_NOT_FORTHCOMING
        The relevants news was not forthcoming.
    ORDER_IMBALANCE
        Halted for order imbalance.
    LULD_PAUSE
        The instrument hit limit up or limit down.
    OPERATIONAL
        An operational issue occurred with the venue.
    ADDITIONAL_INFORMATION_REQUESTED
        The status changed until the exchange receives additional information.
    MERGER_EFFECTIVE
        Trading halted due to merger becoming effective.
    ETF
        Trading is halted in an ETF due to conditions with the component securities.
    CORPORATE_ACTION
        Trading is halted for a corporate action.
    NEW_SECURITY_OFFERING
        Trading is halted because the instrument is a new offering.
    MARKET_WIDE_HALT_LEVEL1
        Halted due to the market-wide circuit breaker level 1.
    MARKET_WIDE_HALT_LEVEL2
        Halted due to the market-wide circuit breaker level 2.
    MARKET_WIDE_HALT_LEVEL3
        Halted due to the market-wide circuit breaker level 3.
    MARKET_WIDE_HALT_CARRYOVER
        Halted due to the carryover of a market-wide circuit breaker from the previous trading day.
    MARKET_WIDE_HALT_RESUMPTION
        Resumption due to the end of the a market-wide circuit breaker halt.
    QUOTATION_NOT_AVAILABLE
        Halted because quotation is not available.

    """

    NONE: int
    SCHEDULED: int
    SURVEILLANCE_INTERVENTION: int
    MARKET_EVENT: int
    INSTRUMENT_ACTIVATION: int
    INSTRUMENT_EXPIRATION: int
    RECOVERY_IN_PROCESS: int
    REGULATORY: int
    ADMINISTRATIVE: int
    NON_COMPLIANCE: int
    FILINGS_NOT_CURRENT: int
    SEC_TRADING_SUSPENSION: int
    NEW_ISSUE: int
    ISSUE_AVAILABLE: int
    ISSUES_REVIEWED: int
    FILING_REQS_SATISFIED: int
    NEWS_PENDING: int
    NEWS_RELEASED: int
    NEWS_AND_RESUMPTION_TIMES: int
    NEWS_NOT_FORTHCOMING: int
    ORDER_IMBALANCE: int
    LULD_PAUSE: int
    OPERATIONAL: int
    ADDITIONAL_INFORMATION_REQUESTED: int
    MERGER_EFFECTIVE: int
    ETF: int
    CORPORATE_ACTION: int
    NEW_SECURITY_OFFERING: int
    MARKET_WIDE_HALT_CARRYOVER: int
    MARKET_WIDE_HALT_RESUMPTION: int
    QUOTATION_NOT_AVAILABLE: int

    @classmethod
    def variants(cls) -> Iterable[StatusReason]: ...

class TradingEvent(Enum):
    """
    Further information about a status update.


    NONE
        No additional information given.
    NO_CANCEL
        Order entry and modification are not allowed.
    CHANGE_TRADING_SESSION
        A change of trading session occurred. Daily statistics are reset.
    IMPLIED_MATCHING_ON
        Implied matching is available.
    IMPLIED_MATCHING_OFF
        Implied matching is not available.

    """

    NONE: int
    NO_CANCEL: int
    CHANGE_TRADING_SESSION: int
    IMPLIED_MATCHING_ON: int
    IMPLIED_MATCHING_OFF: int

    @classmethod
    def variants(cls) -> Iterable[TradingEvent]: ...

class TriState(Enum):
    """
    An enum for representing unknown, true, or false values. Equivalent to `Optional[bool]`.

    NOT_AVAILABLE
        The value is not applicable or not known.
    NO
        False
    YES
        True

    """

    NOT_AVAILABLE: str
    NO: str
    YES: str

    @classmethod
    def from_str(cls, value: str) -> TriState: ...
    @classmethod
    def variants(cls) -> Iterable[TriState]: ...
    def opt_bool(self) -> Optional[bool]: ...

class VersionUpgradePolicy(Enum):
    """
    How to handle decoding a DBN data from a prior version.

    AS_IS
        Decode data from previous versions as-is.
    UPGRADE_TO_V2
        Decode and convert data from DBN versions prior to version 2 to that version.
        Attempting to decode data from newer versions (when they're introduced) will
        fail.

    """

    AS_IS: int
    UPGRADE_TO_V2: int

class Metadata(SupportsBytes):
    """
    Information about the data contained in a DBN file or stream. DBN requires
    the Metadata to be included at the start of the encoded data.
    """

    def __init__(
        self,
        dataset: str,
        start: int,
        stype_in: SType | None,
        stype_out: SType,
        schema: Schema | None,
        symbols: list[str] | None = None,
        partial: list[str] | None = None,
        not_found: list[str] | None = None,
        mappings: Sequence[SymbolMapping] | None = None,
        end: int | None = None,
        limit: int | None = None,
        ts_out: bool | None = None,
        version: int | None = None,
    ) -> None: ...
    def __bytes__(self) -> bytes: ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...
    @property
    def version(self) -> int:
        """
        The DBN schema version number.

        Returns
        -------
        int

        """

    @property
    def dataset(self) -> str:
        """
        The dataset code.

        Returns
        -------
        str

        """

    @property
    def schema(self) -> str | None:
        """
        The data record schema. Specifies which record type is stored in the
        Zstd-compressed DBN file.

        Returns
        -------
        str | None

        """

    @property
    def start(self) -> int:
        """
        The UNIX nanosecond timestamp of the query start, or the first record
        if the file was split.

        Returns
        -------
        int

        """

    @property
    def end(self) -> int:
        """
        The UNIX nanosecond timestamp of the query end, or the last record if
        the file was split.

        Returns
        -------
        int

        """

    @property
    def limit(self) -> int:
        """
        The optional maximum number of records for the query.

        Returns
        -------
        int

        """

    @property
    def stype_in(self) -> SType | None:
        """
        The input symbology type to map from.

        Returns
        -------
        SType | None

        """

    @property
    def stype_out(self) -> SType:
        """
        The output symbology type to map to.

        Returns
        -------
        SType

        """

    @property
    def ts_out(self) -> bool:
        """
        `true` if this store contains live data with send timestamps appended
        to each record.

        Returns
        -------
        bool

        """

    @property
    def symbols(self) -> list[str]:
        """
        The original query input symbols from the request.

        Returns
        -------
        list[str]

        """

    @property
    def partial(self) -> list[str]:
        """
        Symbols that did not resolve for at least one day in the query time
        range.

        Returns
        -------
        list[str]

        """

    @property
    def not_found(self) -> list[str]:
        """
        Symbols that did not resolve for any day in the query time range.

        Returns
        -------
        list[str]

        """

    @property
    def mappings(self) -> dict[str, list[MappingIntervalDict]]:
        """
        Symbol mappings containing a native symbol and its mapping intervals.

        Returns
        -------
        dict[str, list[dict[str, Any]]]:

        """

    @classmethod
    def decode(cls, data: bytes, upgrade_policy: VersionUpgradePolicy | None = None) -> Metadata:
        """
        Decode the given Python `bytes` to `Metadata`. Returns a `Metadata`
        object with all the DBN metadata attributes.

        Parameters
        ----------
        data : bytes
            The bytes to decode from.
        upgrade_policy : VersionUpgradePolicy, default UPGRADE
            How to decode data from prior DBN versions. Defaults to upgrade decoding.

        Returns
        -------
        Metadata

        Raises
        ------
        DBNError
            When a Metadata instance cannot be parsed from `data`.

        """

    def encode(self) -> bytes:
        """
        Encode the Metadata to bytes.

        Returns
        -------
        bytes

        Raises
        ------
        DBNError
            When the Metadata object cannot be encoded.

        """

class RecordHeader:
    """
    DBN Record Header.
    """

    @property
    def length(self) -> int:
        """
        The length of the record.

        Returns
        -------
        int

        """

    @property
    def rtype(self) -> int:
        """
        The record type.

        Returns
        -------
        int

        """

    @property
    def publisher_id(self) -> int:
        """
        The publisher ID assigned by Databento, which denotes the dataset and venue.

        Returns
        -------
        int

        """

    @property
    def instrument_id(self) -> int:
        """
        The numeric ID assigned to the instrument.

        Returns
        -------
        int

        """

    @property
    def ts_event(self) -> int:
        """
        The matching-engine-received timestamp expressed as the number of
        nanoseconds since the UNIX epoch.

        Returns
        -------
        int

        """

class Record(SupportsBytes):
    """
    Base class for DBN records.
    """

    size_hint: ClassVar[int]
    _dtypes: ClassVar[list[tuple[str, str]]]
    _hidden_fields: ClassVar[list[str]]
    _price_fields: ClassVar[list[str]]
    _ordered_fields: ClassVar[list[str]]
    _timestamp_fields: ClassVar[list[str]]

    def __bytes__(self) -> bytes: ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...
    @property
    def hd(self) -> RecordHeader:
        """
        The common header.

        Returns
        -------
        RecordHeader

        """

    @property
    def record_size(self) -> int:
        """
        Return the size of the record in bytes.

        Returns
        -------
        int

        See Also
        --------
        size_hint

        """

    @property
    def rtype(self) -> int:
        """
        The record type.

        Returns
        -------
        int

        """

    @property
    def publisher_id(self) -> int:
        """
        The publisher ID assigned by Databento, which denotes the dataset and venue.

        Returns
        -------
        int

        """

    @property
    def instrument_id(self) -> int:
        """
        The numeric ID assigned to the instrument.

        Returns
        -------
        int

        """

    @property
    def pretty_ts_event(self) -> dt.datetime | None:
        """
        The matching-engine-received timestamp expressed as a
        datetime or a `pandas.Timestamp`, if available.

        Returns
        -------
        datetime.datetime

        """

    @property
    def ts_event(self) -> int:
        """
        The matching-engine-received timestamp expressed as the number of
        nanoseconds since the UNIX epoch.

        Returns
        -------
        int

        """

    @property
    def ts_out(self) -> int | None:
        """
        The live gateway send timestamp expressed as the number of nanoseconds
        since the UNIX epoch.

        Returns
        -------
        int | None

        """

class _MBOBase:
    """
    Base for market-by-order messages.
    """

    @property
    def order_id(self) -> int:
        """
        The order ID assigned at the venue.

        Returns
        -------
        int

        """

    @property
    def pretty_price(self) -> float:
        """
        The order price as a float.

        Returns
        -------
        float

        See Also
        --------
        price

        """

    @property
    def price(self) -> int:
        """
        The order price expressed as a signed integer where every 1 unit
        corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001.

        Returns
        -------
        int

        See Also
        --------
        pretty_price

        """

    @property
    def size(self) -> int:
        """
        The order quantity.

        Returns
        -------
        int

        """

    @property
    def flags(self) -> int:
        """
        A bit field indicating event end, message characteristics, and data quality.

        Returns
        -------
        int

        """

    @property
    def channel_id(self) -> int:
        """
        A channel ID within the venue.

        Returns
        -------
        int

        """

    @property
    def action(self) -> str:
        """
        The event action. Can be `A`dd, `C`ancel, `M`odify, clea`R`, `T`rade,
        or `F`ill.

        Returns
        -------
        str

        """

    @property
    def side(self) -> str:
        """
        The side that initiates the event. Can be `A`sk for a sell order (or sell
        aggressor in a trade), `B`id for a buy order (or buy aggressor in a trade), or
        `N`one where no side is specified by the original source.

        Returns
        -------
        str

        """

    @property
    def pretty_ts_recv(self) -> dt.datetime | None:
        """
        The capture-server-received timestamp as a datetime or
        `pandas.Timestamp`, if available.

        Returns
        -------
        datetime.datetime

        """

    @property
    def ts_recv(self) -> int:
        """
        The capture-server-received timestamp expressed as the number of
        nanoseconds since the UNIX epoch.

        Returns
        -------
        int

        """

    @property
    def ts_in_delta(self) -> int:
        """
        The delta of `ts_recv - ts_exchange_send`, max 2 seconds.

        Returns
        -------
        int

        """

    @property
    def sequence(self) -> int:
        """
        The message sequence number assigned at the venue.

        Returns
        -------
        int

        """

class MBOMsg(Record, _MBOBase):
    """
    A market-by-order (MBO) tick message.
    """

    def __init__(
        self,
        publisher_id: int,
        instrument_id: int,
        ts_event: int,
        order_id: int,
        price: int,
        size: int,
        action: str,
        side: str,
        ts_recv: int,
        flags: int | None = None,
        channel_id: int | None = None,
        ts_in_delta: int | None = None,
        sequence: int | None = None,
    ) -> None: ...

class BidAskPair:
    """
    A book level.
    """

    def __init__(
        self,
        bid_px: int = UNDEF_PRICE,
        ask_px: int = UNDEF_PRICE,
        bid_sz: int = 0,
        ask_sz: int = 0,
        bid_ct: int = 0,
        ask_ct: int = 0,
    ) -> None: ...
    @property
    def pretty_bid_px(self) -> float:
        """
        The bid price as a float.

        Returns
        -------
        float

        See Also
        --------
        bid_px

        """

    @property
    def bid_px(self) -> int:
        """
        The bid price expressed as a signed integer where every 1 unit
        corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001.

        Returns
        -------
        int

        See Also
        --------
        pretty_bid_px

        """

    @property
    def pretty_ask_px(self) -> float:
        """
        The ask price as a float.

        Returns
        -------
        float

        See Also
        --------
        ask_px

        """

    @property
    def ask_px(self) -> int:
        """
        The ask price as a signed integer where every 1 unit
        corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001.

        Returns
        -------
        int

        See Also
        --------
        pretty_ask_px

        """

    @property
    def bid_sz(self) -> int:
        """
        The bid size.

        Returns
        -------
        int

        """

    @property
    def ask_sz(self) -> int:
        """
        The ask size.

        Returns
        -------
        int

        """

    @property
    def bid_ct(self) -> int:
        """
        The bid order count.

        Returns
        -------
        int

        """

    @property
    def ask_ct(self) -> int:
        """
        The ask order count.

        Returns
        -------
        int

        """

class ConsolidatedBidAskPair:
    """
    A consolidated book level.
    """

    def __init__(
        self,
        bid_px: int = UNDEF_PRICE,
        ask_px: int = UNDEF_PRICE,
        bid_sz: int = 0,
        ask_sz: int = 0,
        bid_pb: int = 0,
        ask_pb: int = 0,
    ) -> None: ...
    @property
    def pretty_bid_px(self) -> float:
        """
        The bid price as a float.

        Returns
        -------
        float

        See Also
        --------
        bid_px

        """

    @property
    def bid_px(self) -> int:
        """
        The bid price expressed as a signed integer where every 1 unit
        corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001.

        Returns
        -------
        int

        See Also
        --------
        pretty_bid_px

        """

    @property
    def pretty_ask_px(self) -> float:
        """
        The ask price as a float.

        Returns
        -------
        float

        See Also
        --------
        ask_px

        """

    @property
    def ask_px(self) -> int:
        """
        The ask price as a signed integer where every 1 unit
        corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001.

        Returns
        -------
        int

        See Also
        --------
        pretty_ask_px

        """

    @property
    def bid_sz(self) -> int:
        """
        The bid size.

        Returns
        -------
        int

        """

    @property
    def ask_sz(self) -> int:
        """
        The ask size.

        Returns
        -------
        int

        """

    @property
    def bid_pb(self) -> int:
        """
        The bid publisher.

        Returns
        -------
        int

        """

    @property
    def pretty_bid_pb(self) -> Optional[str]:
        """
        The human-readable bid publisher.

        Returns
        -------
        Optional[str]

        """

    @property
    def ask_pb(self) -> int:
        """
        The ask publisher.

        Returns
        -------
        int

        """

    @property
    def pretty_ask_pb(self) -> Optional[str]:
        """
        The human-readable ask publisher.

        Returns
        -------
        Optional[str]

        """

class _MBPBase:
    """
    Base for market-by-price messages.
    """

    @property
    def pretty_price(self) -> float:
        """
        The order price as a float.

        Returns
        -------
        float

        See Also
        --------
        price

        """

    @property
    def price(self) -> int:
        """
        The order price expressed as a signed integer where every 1 unit
        corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001.

        Returns
        -------
        int

        See Also
        --------
        pretty_price

        """

    @property
    def size(self) -> int:
        """
        The order quantity.

        Returns
        -------
        int

        """

    @property
    def action(self) -> str:
        """
        The event action. Can be `A`dd, `C`ancel, `M`odify, clea`R`, or
        `T`rade.

        Returns
        -------
        str

        """

    @property
    def side(self) -> str:
        """
        The side that initiates the event. Can be `A`sk for a sell order (or sell
        aggressor in a trade), `B`id for a buy order (or buy aggressor in a trade), or
        `N`one where no side is specified by the original source.

        Returns
        -------
        str

        """

    @property
    def flags(self) -> int:
        """
        A bit field indicating event end, message characteristics, and data quality.

        Returns
        -------
        int

        """

    @property
    def depth(self) -> int:
        """
        The depth of actual book change.

        Returns
        -------
        int

        """

    @property
    def pretty_ts_recv(self) -> dt.datetime | None:
        """
        The capture-server-received timestamp as a datetime or
        `pandas.Timestamp`, if available.

        Returns
        -------
        datetime.datetime

        """

    @property
    def ts_recv(self) -> int:
        """
        The capture-server-received timestamp expressed as the number of
        nanoseconds since the UNIX epoch.

        Returns
        -------
        int

        """

    @property
    def ts_in_delta(self) -> int:
        """
        The delta of `ts_recv - ts_exchange_send`, max 2 seconds.

        Returns
        -------
        int

        """

    @property
    def sequence(self) -> int:
        """
        The message sequence number assigned at the venue.

        Returns
        -------
        int

        """

class TradeMsg(Record, _MBPBase):
    """
    Market by price implementation with a book depth of 0.

    Equivalent to MBP-0. The record of the `Trades` schema.

    """

    def __init__(
        self,
        publisher_id: int,
        instrument_id: int,
        ts_event: int,
        price: int,
        size: int,
        action: str,
        side: str,
        depth: int,
        ts_recv: int,
        flags: int | None = None,
        ts_in_delta: int | None = None,
        sequence: int | None = None,
    ) -> None: ...

class MBP1Msg(Record, _MBPBase):
    """
    Market by price implementation with a known book depth of 1.
    """

    def __init__(
        self,
        publisher_id: int,
        instrument_id: int,
        ts_event: int,
        price: int,
        size: int,
        action: str,
        side: str,
        depth: int,
        ts_recv: int,
        flags: int | None = None,
        ts_in_delta: int | None = None,
        sequence: int | None = None,
        levels: BidAskPair | None = None,
    ) -> None: ...
    @property
    def levels(self) -> list[BidAskPair]:
        """
        The top of the order book.

        Returns
        -------
        list[BidAskPair]

        Notes
        -----
        MBP1Msg contains 1 level of BidAskPair.

        """

class BBOMsg(Record):
    """
    Subsampled market by price with a known book depth of 1.
    """

    def __init__(
        self,
        rtype: int,
        publisher_id: int,
        instrument_id: int,
        ts_event: int,
        price: int,
        size: int,
        action: str,
        side: str,
        ts_recv: int,
        flags: int | None = None,
        sequence: int | None = None,
        levels: BidAskPair | None = None,
    ) -> None: ...
    @property
    def pretty_price(self) -> float:
        """
        The price of the last trade as a float.

        Returns
        -------
        float

        See Also
        --------
        price

        """

    @property
    def price(self) -> int:
        """
        The price of the last trade expressed as a signed integer where every 1 unit
        corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001.

        Returns
        -------
        int

        See Also
        --------
        pretty_price

        """

    @property
    def size(self) -> int:
        """
        The quantity of the last trade.

        Returns
        -------
        int

        """

    @property
    def side(self) -> str:
        """
        The side that initiated the last trade. Can be `A`sk for a sell order (or sell
        aggressor in a trade), `B`id for a buy order (or buy aggressor in a trade), or
        `N`one where no side is specified by the original source.

        Returns
        -------
        str

        """

    @property
    def flags(self) -> int:
        """
        A bit field indicating event end, message characteristics, and data quality.

        Returns
        -------
        int

        """

    @property
    def pretty_ts_recv(self) -> dt.datetime | None:
        """
        The capture-server-received timestamp as a datetime or
        `pandas.Timestamp`, if available.

        Returns
        -------
        datetime.datetime

        """

    @property
    def ts_recv(self) -> int:
        """
        The capture-server-received timestamp expressed as the number of
        nanoseconds since the UNIX epoch.

        Returns
        -------
        int

        """

    @property
    def sequence(self) -> int:
        """
        The message sequence number assigned at the venue of the last update.

        Returns
        -------
        int

        """

    @property
    def levels(self) -> list[BidAskPair]:
        """
        The top of the order book.

        Returns
        -------
        list[BidAskPair]

        Notes
        -----
        BBOMsg contains 1 level of BidAskPair.

        """

class CMBP1Msg(Record):
    """
    Consolidated best bid and offer implementation.
    """

    def __init__(
        self,
        rtype: int,
        publisher_id: int,
        instrument_id: int,
        ts_event: int,
        price: int,
        size: int,
        action: str,
        side: str,
        ts_recv: int,
        flags: int | None = None,
        ts_in_delta: int | None = None,
        levels: ConsolidatedBidAskPair | None = None,
    ) -> None: ...
    @property
    def pretty_price(self) -> float:
        """
        The order price as a float.

        Returns
        -------
        float

        See Also
        --------
        price

        """

    @property
    def price(self) -> int:
        """
        The order price expressed as a signed integer where every 1 unit
        corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001.

        Returns
        -------
        int

        See Also
        --------
        pretty_price

        """

    @property
    def size(self) -> int:
        """
        The order quantity.

        Returns
        -------
        int

        """

    @property
    def action(self) -> str:
        """
        The event action. Can be `A`dd, `C`ancel, `M`odify, clea`R`, or
        `T`rade.

        Returns
        -------
        str

        """

    @property
    def side(self) -> str:
        """
        The order side. Can be `A`sk, `B`id or `N`one.

        Returns
        -------
        str

        """

    @property
    def flags(self) -> int:
        """
        A bit field indicating event end, message characteristics, and data quality.

        Returns
        -------
        int

        """

    @property
    def depth(self) -> int:
        """
        The depth of actual book change.

        Returns
        -------
        int

        """

    @property
    def pretty_ts_recv(self) -> dt.datetime | None:
        """
        The interval timestamp as a datetime or `pandas.Timestamp` if available.

        Returns
        -------
        datetime.datetime

        """

    @property
    def ts_recv(self) -> int:
        """
        The interval timestamp expressed as the number of nanoseconds since the UNIX epoch.

        Returns
        -------
        int

        """

    @property
    def ts_in_delta(self) -> int:
        """
        The delta of `ts_recv - ts_exchange_send`, max 2 seconds.

        Returns
        -------
        int

        """

    @property
    def sequence(self) -> int:
        """
        The message sequence number assigned at the venue.

        Returns
        -------
        int

        """

    @property
    def levels(self) -> list[ConsolidatedBidAskPair]:
        """
        The top of the consolidated order book.

        Returns
        -------
        list[ConsolidatedBidAskPair]

        Notes
        -----
        CMBP1Msg contains 1 level of ConsolidatedBidAskPair.

        """

class CBBOMsg(Record):
    """
    Subsampled consolidated best bid and offer.
    """

    def __init__(
        self,
        rtype: int,
        publisher_id: int,
        instrument_id: int,
        ts_event: int,
        price: int,
        size: int,
        side: str,
        ts_recv: int,
        flags: int | None = None,
        levels: ConsolidatedBidAskPair | None = None,
    ) -> None: ...
    @property
    def pretty_price(self) -> float:
        """
        The price of the last trade as a float.

        Returns
        -------
        float

        See Also
        --------
        price

        """

    @property
    def price(self) -> int:
        """
        The price of the last trade expressed as a signed integer where every 1 unit
        corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001.

        Returns
        -------
        int

        See Also
        --------
        pretty_price

        """

    @property
    def size(self) -> int:
        """
        The quantity of the last trade.

        Returns
        -------
        int

        """

    @property
    def side(self) -> str:
        """
        The side that initiated the last trade. Can be `A`sk for a sell order (or sell
        aggressor in a trade), `B`id for a buy order (or buy aggressor in a trade), or
        `N`one where no side is specified by the original source.

        Returns
        -------
        str

        """

    @property
    def flags(self) -> int:
        """
        A bit field indicating event end, message characteristics, and data quality.

        Returns
        -------
        int

        """

    @property
    def pretty_ts_recv(self) -> dt.datetime | None:
        """
        The capture-server-received timestamp as a datetime or
        `pandas.Timestamp`, if available.

        Returns
        -------
        datetime.datetime

        """

    @property
    def ts_recv(self) -> int:
        """
        The capture-server-received timestamp expressed as the number of
        nanoseconds since the UNIX epoch.

        Returns
        -------
        int

        """

    @property
    def sequence(self) -> int:
        """
        The message sequence number assigned at the venue of the last update.

        Returns
        -------
        int

        """

    @property
    def levels(self) -> list[ConsolidatedBidAskPair]:
        """
        The top of the order book.

        Returns
        -------
        list[BidAskPair]

        Notes
        -----
        BBOMsg contains 1 level of ConsolidatedBidAskPair.

        """

class MBP10Msg(Record, _MBPBase):
    """
    Market by price implementation with a known book depth of 10.
    """

    def __init__(
        self,
        publisher_id: int,
        instrument_id: int,
        ts_event: int,
        price: int,
        size: int,
        action: str,
        side: str,
        depth: int,
        ts_recv: int,
        flags: int | None = None,
        ts_in_delta: int | None = None,
        sequence: int | None = None,
        levels: list[BidAskPair] | None = None,
    ) -> None: ...
    @property
    def levels(self) -> list[BidAskPair]:
        """
        The top 10 levels.

        Returns
        -------
        list[BidAskPair]

        Notes
        -----
        MBP10Msg contains 10 levels of BidAskPairs.

        """

class OHLCVMsg(Record):
    """
    Open, high, low, close, and volume message.
    """

    def __init__(
        self,
        rtype: int,
        publisher_id: int,
        instrument_id: int,
        ts_event: int,
        open: in...
```

## High-Level Overview

This file is located at `python/python/databento_dbn/_lib.pyi` within the repository.

### File Overview

This file is part of the repository's supporting infrastructure or data.

