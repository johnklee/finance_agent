# Specification: Support StockInfo object as input for get_alpha and get_beta (Issue #40)

## Overview
Currently, `YahooFinanceProvider.get_alpha` and `YahooFinanceProvider.get_beta` accept stock identifier inputs of types `str`, `int`, and `SymbolInfo`. When a user passes a `StockInfo` dataclass instance (such as the object returned by `fin_provider.get_stock_info(...)`), the symbol resolution stringifies the object, leading to a 404/Not Found quote error from Yahoo Finance. This specification details enhancing `_resolve_symbol` and related APIs to accept `StockInfo` instances directly and resolve their `stock_symbol` attribute.

## Functional Requirements
1. **Extend `YahooFinanceProvider._resolve_symbol`**:
   - Update `_resolve_symbol(symbol: str | int | SymbolInfo | StockInfo) -> str` in `finance_agent/tools/yfinance_finance.py`.
   - When `isinstance(symbol, StockInfo)`, return `symbol.stock_symbol`.
2. **Update Method Signatures and Type Hints in Provider and Protocols**:
   - In `finance_agent/tools/yfinance_finance.py`, update signatures and docstrings of `get_alpha`, `get_beta`, `get_stock_info`, and `get_latest_roe` to accept `StockInfo` in `symbol: str | int | SymbolInfo | StockInfo`.
   - In `finance_agent/tools/__init__.py`, update `BaseProvider` protocol signatures and docstrings to include `StockInfo` in `symbol: str | int | SymbolInfo | StockInfo`.
3. **Update Agent Signatures**:
   - In `finance_agent/agent/__init__.py`, update signatures and docstrings of `get_stock_info`, `get_latest_roe`, `get_beta`, `get_alpha` (and internal methods of `FinanceAgent`) to support `StockInfo`.
4. **Cache Decorator Compatibility**:
   - Ensure `finance_agent/tools/stock_info.py`'s cache decorator handles `StockInfo` instances when querying cached records by symbol.

## Non-Functional Requirements
- Maintain backward compatibility with `str`, `int`, and `SymbolInfo`.
- Strictly adhere to Google Python Style Guide and pass `ruff` lint checks.
- Maintain test coverage > 80% for modified modules.

## Acceptance Criteria
- Calling `provider.get_alpha(stock_info)` successfully extracts `stock_info.stock_symbol` and calculates alpha without 404 quote lookup errors.
- Calling `provider.get_beta(stock_info)` successfully extracts `stock_info.stock_symbol` and calculates beta without errors.
- Unit tests cover passing `StockInfo` into `get_alpha`, `get_beta`, `get_latest_roe`, and `get_stock_info`.
- All existing tests pass.

## Out of Scope
- Altering the underlying mathematical formulas of CAPM Alpha or Beta.
