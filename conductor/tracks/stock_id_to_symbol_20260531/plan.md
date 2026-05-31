# Implementation Plan: Stock ID to Symbol Transformation Utility

## Phase 1: Setup and Exception Definition [checkpoint: e2a8b23]
- [x] Task: Define the custom Exception
    - [x] Create `StockNotFoundError` in `finance_agent/tools/exceptions.py`
    - [x] Ensure it inherits from both `KeyError` and `FinanceDataError`
    - [x] Write unit tests to verify the exception can be raised with a descriptive message
- [x] Task: Conductor - User Manual Verification 'Phase 1: Setup and Exception Definition' (Protocol in workflow.md)

## Phase 2: Implement CSV Cache Decorator [checkpoint: d969cf4]
- [x] Task: Create tests for `csv_cache` decorator (Red Phase)
    - [x] Write unit tests in `tests/test_stock_info.py` for the decorator behavior (loading, checking, writing)
    - [x] Verify the tests fail as expected
- [x] Task: Implement `csv_cache` decorator (Green Phase)
    - [x] Implement the `csv_cache` decorator function in `finance_agent/tools/stock_info.py`
    - [x] Support default path and environment variable configuration
    - [x] Initialize the file with headers if it does not exist
    - [x] Verify that newly added mappings are immediately written to disk
    - [x] Ensure all tests pass and verify coverage (>80%)
- [x] Task: Conductor - User Manual Verification 'Phase 2: Implement CSV Cache Decorator' (Protocol in workflow.md)

## Phase 3: Implement Stock ID to Symbol Conversion
- [ ] Task: Create tests for `stock_id_to_symbol` function (Red Phase)
    - [ ] Write unit tests in `tests/test_stock_info.py` for stock ID to symbol conversion
    - [ ] Test resolving listed stock ID (e.g., `2330` -> `2330.TW`) and OTC stock ID (e.g., `8069` -> `8069.TWO`)
    - [ ] Test raising `StockNotFoundError` for invalid stock IDs
    - [ ] Verify the tests fail as expected
- [ ] Task: Implement `stock_id_to_symbol` (Green Phase)
    - [ ] Implement the `stock_id_to_symbol` function decorated with `@csv_cache` in `finance_agent/tools/stock_info.py`
    - [ ] Use `twstock.codes` to resolve market type
    - [ ] Ensure all tests pass and verify coverage (>80%)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Implement Stock ID to Symbol Conversion' (Protocol in workflow.md)
