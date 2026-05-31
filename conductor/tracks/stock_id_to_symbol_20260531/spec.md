# Specification: Stock ID to Symbol Transformation Utility

## Overview
This feature implements a new utility module `tools/stock_info.py` to convert a Taiwan Stock ID (e.g., `2330`, `8069`) into a Yahoo Finance stock symbol (e.g., `2330.TW`, `8069.TWO`). It resolves the market type (listed/"上市" vs. OTC/"上櫃") using the `twstock` library and implements a CSV-backed caching mechanism to avoid redundant lookups and provide fast offline mapping.

## Functional Requirements
1. **Module Location:** Implement the functionality in `finance_agent/tools/stock_info.py`.
2. **Custom Exception:**
   - Define a custom exception `StockNotFoundError` in `finance_agent/tools/exceptions.py`.
   - `StockNotFoundError` must inherit from both `KeyError` (retaining standard dict lookup interface compatibility) and `FinanceDataError`.
   - Raising this exception must provide a clear, descriptive message indicating the missing Stock ID.
3. **CSV Cache Decorator (`csv_cache`):**
   - Cache stock ID to Yahoo Finance symbol mappings in a CSV file.
   - The default cache file path is `tw_stock_info_listed.csv` located in the project's root directory, but it must be configurable via an environment variable `TW_STOCK_CACHED_CSV_PATH`.
   - On application startup or first import of the module, if the CSV cache file does not exist, initialize it by creating the file and writing the header row: `stock_id,stock_symbol`.
   - Read the existing cache from the CSV file once when the decorator is applied.
   - When the decorated function resolves a new mapping, it must immediately append the new entry back to the CSV file on disk.
4. **Stock ID to Symbol Conversion (`stock_id_to_symbol`):**
   - Decorated with `@csv_cache`.
   - Accepts a `stock_id` as either `str` or `int`.
   - Converts it to a string.
   - If the ID is cached, returns the cached symbol immediately.
   - If the ID is not in the cache:
     - Query the `twstock` library codes database using `twstock.codes[stock_id_str]`.
     - If the ID does not exist in `twstock`, raise a custom `StockNotFoundError`.
     - Determine the market type of the stock:
       - If `stock.market == "上市"`, append `.TW` to form the Yahoo Finance symbol (e.g., `2330.TW`).
       - Otherwise, append `.TWO` to form the Yahoo Finance symbol (e.g., `8069.TWO`).
     - Save the new mapping to the CSV cache file.
     - Return the resolved symbol.

## Non-Functional Requirements
- **Performance:** Caching ensures O(1) lookups for previously resolved IDs and avoids redundant library/API calls.
- **Robustness:** Handles type casting gracefully (`str` or `int`).
- **Simplicity:** High-quality code style adhering to PEP 8, formatted with `ruff`.

## Acceptance Criteria
- [ ] `finance_agent/tools/stock_info.py` exists with both `csv_cache` and `stock_id_to_symbol` implemented.
- [ ] Custom exception `StockNotFoundError` is defined in `finance_agent/tools/exceptions.py`.
- [ ] First import of `stock_info` initializes the CSV cache file with headers if it does not exist.
- [ ] `stock_id_to_symbol` resolves listed stocks (e.g., `2330` -> `2330.TW`) and OTC stocks (e.g., `8069` -> `8069.TWO`) correctly.
- [ ] Resolved mappings are persisted back to the CSV file immediately.
- [ ] Unknown stock IDs raise `StockNotFoundError`.
- [ ] Unit tests are written and coverage is >80%.

## Out of Scope
- Fetching actual stock prices or historical data from Yahoo Finance (handled by other modules).
- Resolving stocks from non-Taiwanese markets (e.g., US, Europe).
