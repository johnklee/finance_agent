import os
from unittest.mock import patch
import pytest

from finance_agent.tools.exceptions import StockNotFoundError
from finance_agent.tools.stock_info import csv_cache, stock_id_to_symbol


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


def test_stock_id_to_symbol_listed(tmp_path):
  cache_file = tmp_path / "test_cache.csv"
  with patch.dict(os.environ, {"TW_STOCK_CACHED_CSV_PATH": str(cache_file)}):
    # 2330 is 台積電 (listed/上市)
    result = stock_id_to_symbol("2330")
    assert result == "2330.TW"


def test_stock_id_to_symbol_otc(tmp_path):
  cache_file = tmp_path / "test_cache.csv"
  with patch.dict(os.environ, {"TW_STOCK_CACHED_CSV_PATH": str(cache_file)}):
    # 8069 is 元太 (OTC/上櫃)
    result = stock_id_to_symbol("8069")
    assert result == "8069.TWO"


def test_stock_id_to_symbol_invalid(tmp_path):
  cache_file = tmp_path / "test_cache.csv"
  with patch.dict(os.environ, {"TW_STOCK_CACHED_CSV_PATH": str(cache_file)}):
    with pytest.raises(StockNotFoundError) as exc_info:
      stock_id_to_symbol("1111")
    assert "1111" in str(exc_info.value)


def test_stock_info_dividend_yield():
  from finance_agent.tools import StockInfo

  # Test case 1: normal calculation
  stock = StockInfo(
    company_name="Test Company",
    currency="TWD",
    current_price=100.0,
    previous_close_price=95.0,
    market_cap=1000000.0,
    annual_dividend=5.0,
  )
  assert stock.annual_dividend == 5.0
  assert stock.dividend_yield == 5.0

  # Test case 2: annual_dividend is None
  stock_no_div = StockInfo(
    company_name="Test Company",
    currency="TWD",
    current_price=100.0,
    previous_close_price=95.0,
    market_cap=1000000.0,
    annual_dividend=None,
  )
  assert stock_no_div.annual_dividend is None
  assert stock_no_div.dividend_yield is None

  # Test case 3: current_price is 0.0 (division by zero handling)
  stock_zero_price = StockInfo(
    company_name="Test Company",
    currency="TWD",
    current_price=0.0,
    previous_close_price=95.0,
    market_cap=1000000.0,
    annual_dividend=5.0,
  )
  assert stock_zero_price.dividend_yield is None
