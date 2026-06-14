# Implementation Plan - Support both Stock ID and Symbol in YahooFinanceProvider

## Phase 1: Test updates and implementation [checkpoint: c948c71]

- [x] Task: Write failing tests (Red Phase)
    - [x] Update `tests/tools/test_yfinance_finance.py` with tests for passing integers (e.g. `2330`), string IDs (e.g. `"2330"`), standard symbols (e.g. `"2330.TW"`), and invalid stock IDs.
    - [x] Run the tests and verify that they fail as expected.
- [x] Task: Implement support in protocol and provider (Green Phase)
    - [x] Update `finance_agent/tools/__init__.py` protocol signature for `BaseProvider.get_stock_info` to accept `str | int`.
    - [x] Update `YahooFinanceProvider.get_stock_info` in `finance_agent/tools/yfinance_finance.py` to support `str | int` and handle resolution with fallback.
    - [x] Run the tests and verify that they all pass successfully.
- [x] Task: Quality Gates and Verification
    - [x] Run `ruff check` and `ruff format` to ensure style guidelines are met.
    - [x] Verify test coverage for the tool modules.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Test updates and implementation' (Protocol in workflow.md)
