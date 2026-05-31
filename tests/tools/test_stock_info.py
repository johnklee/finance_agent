import os
from unittest.mock import patch

# We import the decorator. Since the file does not exist yet, this should fail.
from finance_agent.tools.stock_info import csv_cache


def test_csv_cache_initialization_creates_file(tmp_path):
    cache_file = tmp_path / "test_cache.csv"

    with patch.dict(os.environ, {"TW_STOCK_CACHED_CSV_PATH": str(cache_file)}):
        # Define a mock function to decorate
        @csv_cache
        def mock_func(stock_id):
            return "symbol"

        # The file should be created immediately upon applying the decorator
        assert cache_file.exists()
        content = cache_file.read_text()
        assert content.strip() == "stock_id,stock_symbol"


def test_csv_cache_loads_existing_mappings(tmp_path):
    cache_file = tmp_path / "test_cache.csv"
    cache_file.write_text("stock_id,stock_symbol\n2330,2330.TW\n")

    with patch.dict(os.environ, {"TW_STOCK_CACHED_CSV_PATH": str(cache_file)}):
        calls = []

        @csv_cache
        def mock_func(stock_id):
            calls.append(stock_id)
            return f"{stock_id}.TW"

        # Since 2330 is in the cache, the decorated function should return it directly
        # and NOT call the underlying mock_func.
        result = mock_func("2330")
        assert result == "2330.TW"
        assert len(calls) == 0


def test_csv_cache_persists_new_mappings_immediately(tmp_path):
    cache_file = tmp_path / "test_cache.csv"
    cache_file.write_text("stock_id,stock_symbol\n")

    with patch.dict(os.environ, {"TW_STOCK_CACHED_CSV_PATH": str(cache_file)}):
        calls = []

        @csv_cache
        def mock_func(stock_id):
            calls.append(stock_id)
            return f"{stock_id}.TW"

        # Calling with a new ID should trigger the decorated function
        result = mock_func("2330")
        assert result == "2330.TW"
        assert len(calls) == 1

        # It should immediately persist to the CSV file
        lines = cache_file.read_text().splitlines()
        assert "2330,2330.TW" in lines

        # Subsequent call with the same ID should be cached
        result2 = mock_func("2330")
        assert result2 == "2330.TW"
        assert len(calls) == 1
