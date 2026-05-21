# Specification: YahooFinanceProvider Implementation

## Overview
This track implements the `YahooFinanceProvider` class, which uses the `yfinance` library to fetch stock information. It will implement the `BaseProvider` protocol defined in `finance_agent/tools/__init__.py`. Additionally, it will fix existing typos in the `BaseProvider` definition.

## Functional Requirements
1.  **Fix `BaseProvider` Typos:**
    *   Correct `from typing import Protocl` to `from typing import Protocol` in `finance_agent/tools/__init__.py`.
    *   Correct `@dataclasses(frozen=True, kw_only=True)` to `@dataclasses.dataclass(frozen=True, kw_only=True)` in `finance_agent/tools/__init__.py`.
2.  **Implement `YahooFinanceProvider`:**
    *   Create a new module: `finance_agent/tools/yfinance_finance.py`.
    *   Create a class `YahooFinanceProvider` that inherits from/implements `BaseProvider`.
    *   Implement the `get_stock_info(self, symbol: str) -> StockInfo` method.
    *   Use the `yfinance` package (specifically `yfinance.Ticker`) to fetch the required data:
        *   `company_name` (from `info.get('longName')` or similar)
        *   `currency` (from `info.get('currency', 'TWD')`)
        *   `current_price` (from `info.get('currentPrice')`)
        *   `previous_close_price` (from `info.get('previousClose')`)
        *   `market_cap` (from `info.get('marketCap')`)
3.  **Error Handling:**
    *   Define a custom exception `FinanceDataError` (e.g., in `finance_agent/tools/exceptions.py` or within the same module).
    *   Catch exceptions raised by `yfinance` (e.g., network errors, invalid symbols) and raise a `FinanceDataError` with a descriptive message.

## Non-Functional Requirements
*   **Testing:** Implement unit tests for `YahooFinanceProvider` using mocked `yfinance` responses to ensure fast and reliable testing without network dependencies.

## Acceptance Criteria
*   [ ] `BaseProvider` typos are fixed and the code runs without syntax/import errors.
*   [ ] `YahooFinanceProvider` is implemented and correctly returns a populated `StockInfo` object for a valid symbol.
*   [ ] `YahooFinanceProvider` raises a `FinanceDataError` when an invalid symbol is provided or a network error occurs.
*   [ ] Unit tests are written using mocks and pass successfully.
*   [ ] Code coverage for the new module is >80%.

## Out of Scope
*   Implementing other data providers.
*   Live integration tests (only mocked unit tests are required for this track).