# Implementation Plan: Support StockInfo object as input for get_alpha and get_beta (Issue #40)

## Phase 1: Test updates and implementation

- [ ] Task: TDD Red - Write failing tests for StockInfo input
    - [ ] Update `tests/tools/test_yfinance_finance.py` with tests for passing `StockInfo` to `get_alpha`, `get_beta`, `get_stock_info`, and `get_latest_roe`.
    - [ ] Update `tests/agent/test_agent.py` to assert that agent tools accept and properly delegate `StockInfo`.
    - [ ] Run pytest to confirm that tests fail on unresolved `StockInfo` input.
- [ ] Task: TDD Green - Update implementation to support StockInfo
    - [ ] Update `YahooFinanceProvider._resolve_symbol` in `finance_agent/tools/yfinance_finance.py` to resolve `symbol.stock_symbol` when `isinstance(symbol, StockInfo)`.
    - [ ] Update method signatures and docstrings across `finance_agent/tools/yfinance_finance.py`, `finance_agent/tools/__init__.py`, and `finance_agent/agent/__init__.py`.
    - [ ] Update cache symbol resolution in `finance_agent/tools/stock_info.py` to support `StockInfo`.
    - [ ] Run pytest to verify all tests pass green.
- [ ] Task: Quality and Coverage Verification
    - [ ] Run `ruff check .` to verify no lint or formatting issues.
    - [ ] Verify test suite passes with full coverage.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Test updates and implementation' (Protocol in workflow.md)
