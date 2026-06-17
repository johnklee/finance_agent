# Implementation Plan: Support finding Stocks With Dividend Yield Over 5%

## Phase 1: Extend StockInfo and Implement Tests

- [ ] Task: TDD Red - Write failing tests for StockInfo changes
    - [ ] Add tests to `tests/tools/test_stock_info.py` that check instantiation with `annual_dividend` (both float and None)
    - [ ] Add tests for `dividend_yield` property calculation: normal calculation, division by zero, and None propagation
    - [ ] Run the test suite and confirm these new tests fail as expected
- [ ] Task: TDD Green - Extend StockInfo dataclass
    - [ ] Add `annual_dividend: float | None` field to `StockInfo` in `finance_agent/tools/__init__.py`
    - [ ] Add `@property def dividend_yield(self) -> float | None` to calculate yield as percentage or return `None`
    - [ ] Run test suite to verify that all new tests now pass successfully
- [ ] Task: Code style and formatting checks
    - [ ] Run `ruff` to ensure compliance with styling rules
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Extend StockInfo and Implement Tests' (Protocol in workflow.md)

## Phase 2: Update YahooFinanceProvider and Integrate

- [ ] Task: TDD Red - Write failing tests for YahooFinanceProvider
    - [ ] Update `tests/tools/test_yfinance_finance.py` to assert that `annual_dividend` is present and correctly extracted from mock yfinance response
    - [ ] Run the tests and confirm they fail
- [ ] Task: TDD Green - Update YahooFinanceProvider logic
    - [ ] Update `get_stock_info` in `finance_agent/tools/yfinance_finance.py` to retrieve `dividendRate` and pass it to `StockInfo`
    - [ ] Run tests and verify they pass successfully
- [ ] Task: Quality and Coverage Verification
    - [ ] Verify test coverage is >80% for the changed modules
    - [ ] Run full pre-commit/formatting checks
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Update YahooFinanceProvider and Integrate' (Protocol in workflow.md)
