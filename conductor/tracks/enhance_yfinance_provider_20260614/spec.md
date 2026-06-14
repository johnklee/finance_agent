# Specification: Support both Stock ID and Symbol in YahooFinanceProvider

## Overview
Currently, `YahooFinanceProvider` expects a full Yahoo Finance stock symbol (e.g., `"2330.TW"`). It does not natively support passing in a Taiwan stock ID (either as a string like `"2330"` or as an integer like `2330`). This track enhances `BaseProvider` and `YahooFinanceProvider` to allow both full symbols and raw stock IDs of type `str` or `int`, automatically resolving IDs to full symbols where applicable.

## Functional Requirements
1. **Update `BaseProvider` Protocol**:
   - Change `get_stock_info(self, symbol: str) -> StockInfo` to `get_stock_info(self, symbol: str | int) -> StockInfo`.
   - Update docstring to reflect the new signature and support for both symbols and raw IDs.

2. **Update `YahooFinanceProvider.get_stock_info` implementation**:
   - Accept `symbol: str | int`.
   - Convert integer inputs to string representations first.
   - Resolution Logic:
     - Check if the input is a stock ID by attempting to convert it to a full symbol using `stock_id_to_symbol(input)`.
     - If `stock_id_to_symbol` succeeds, use the resolved full symbol to query `yfinance`.
     - If `stock_id_to_symbol` raises `StockNotFoundError` or if the input is already a symbol (e.g., already contains a suffix), fall back to querying `yfinance` directly with the original input string.
     - If any exception or error is encountered during the `yfinance` query, or if no data is found, raise `FinanceDataError`.

## Non-Functional Requirements
- Maintain backward compatibility for existing code that passes a full symbol string (e.g., `"2330.TW"`).
- Keep performance overhead minimal by utilizing the existing CSV caching mechanism decorated on `stock_id_to_symbol`.

## Acceptance Criteria
1. Passing `2330` (integer) to `YahooFinanceProvider.get_stock_info` successfully returns stock info for `2330.TW` (TSMC).
2. Passing `"2330"` (string) to `YahooFinanceProvider.get_stock_info` successfully returns stock info for `2330.TW`.
3. Passing `"2330.TW"` (string with suffix) to `YahooFinanceProvider.get_stock_info` successfully returns stock info.
4. Passing non-existent stock ID (e.g., `999999`) or invalid symbols raises `FinanceDataError`.
5. Unit tests are added to verify all these scenarios.

## Out of Scope
- Support for international stock IDs beyond Taiwan stock IDs handled by `twstock`.
