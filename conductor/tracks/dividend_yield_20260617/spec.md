# Specification: Support finding Stocks With Dividend Yield Over 5%

## Overview
This feature adds support for retrieving a stock's annual dividend and calculating its dividend yield. It updates the `StockInfo` dataclass to include `annual_dividend` and a dynamic `dividend_yield` property, and updates the `YahooFinanceProvider` to extract `dividendRate` from Yahoo Finance's ticker info.

## Functional Requirements
1. **Extend `StockInfo` Dataclass**:
   - Add a field `annual_dividend: float | None` representing the annual dividend per share.
   - Implement a dynamic property `@property def dividend_yield(self) -> float | None` that returns the dividend yield as a percentage (e.g., `5.0` for `5%`).
   - If `current_price` is missing/zero or `annual_dividend` is missing, `dividend_yield` must return `None`.
2. **Update `YahooFinanceProvider` (`finance_agent/tools/yfinance_finance.py`)**:
   - Fetch the annual dividend using `info.get("dividendRate")` (as `annual_dividend`).
   - Pass this value to `StockInfo` when constructing the return object.

## Non-Functional Requirements
- Ensure calculations are fast and do not block.
- Follow existing PEP 8 code style, type hints, and docstrings.

## Acceptance Criteria
- `StockInfo` can be instantiated with `annual_dividend` as a float or `None`.
- `StockInfo.dividend_yield` correctly calculates yield as `(annual_dividend / current_price) * 100`.
- `StockInfo.dividend_yield` returns `None` if `current_price` is `0` or if `annual_dividend` is `None`.
- `YahooFinanceProvider.get_stock_info()` correctly maps `dividendRate` to `annual_dividend`.
- Unit tests written and passing for:
  - `StockInfo.dividend_yield` logic (under `tests/tools/test_stock_info.py`).
  - `YahooFinanceProvider.get_stock_info` fetching and mapping (under `tests/tools/test_yfinance_finance.py`).

## Out of Scope
- Building the command-line search/filter query interface for screening stocks with dividend yield > 5% (this track is specifically for the data-retrieval and representation foundations).
