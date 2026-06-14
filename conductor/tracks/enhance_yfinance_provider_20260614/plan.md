# Implementation Plan - Support both Stock ID and Symbol in YahooFinanceProvider

## Phase 1: Test updates and implementation

- [ ] Task: Write failing tests (Red Phase)
    - [ ] Update `tests/tools/test_yfinance_finance.py` with tests for passing integers (e.g. `2330`), string IDs (e.g. `"2330"`), standard symbols (e.g. `"2330.TW"`), and invalid stock IDs.
    - [ ] Run the tests and verify that they fail as expected.
- [ ] Task: Implement support in protocol and provider (Green Phase)
    - [ ] Update `finance_agent/tools/__init__.py` protocol signature for `BaseProvider.get_stock_info` to accept `str | int`.
    - [ ] Update `YahooFinanceProvider.get_stock_info` in `finance_agent/tools/yfinance_finance.py` to support `str | int` and handle resolution with fallback.
    - [ ] Run the tests and verify that they all pass successfully.
- [ ] Task: Quality Gates and Verification
    - [ ] Run `ruff check` and `ruff format` to ensure style guidelines are met.
    - [ ] Verify test coverage for the tool modules.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Test updates and implementation' (Protocol in workflow.md)
