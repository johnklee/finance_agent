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


def test_symbol_info():
  from finance_agent.tools import SymbolInfo

  info = SymbolInfo(symbol="2330.TW", industrial_group="半導體業")
  assert info.symbol == "2330.TW"
  assert info.industrial_group == "半導體業"


def test_cache_decorator(tmp_path):
  from datetime import timedelta
  import pandas as pd
  from finance_agent.tools import SymbolInfo, cache

  cache_file = tmp_path / "test_symbol_cache.csv"

  def loader(df: pd.DataFrame) -> list[SymbolInfo]:
    return [
      SymbolInfo(
        symbol=str(row["symbol"]),
        industrial_group=str(row["industrial_group"]),
      )
      for _, row in df.iterrows()
    ]

  def dumper(symbols: list[SymbolInfo]) -> pd.DataFrame:
    import dataclasses

    return pd.DataFrame([dataclasses.asdict(s) for s in symbols])

  calls = []

  @cache(
    life_time=timedelta(days=1),
    cache_file=cache_file,
    loader=loader,
    dumper=dumper,
  )
  def mock_get_symbols() -> list[SymbolInfo]:
    calls.append(1)
    return [SymbolInfo(symbol="1101.TW", industrial_group="水泥工業")]

  # First call executes function and writes CSV
  res1 = mock_get_symbols()
  assert len(res1) == 1
  assert res1[0].symbol == "1101.TW"
  assert len(calls) == 1
  assert cache_file.exists()

  # Second call reads from CSV cache without executing function
  res2 = mock_get_symbols()
  assert len(res2) == 1
  assert res2[0].symbol == "1101.TW"
  assert len(calls) == 1

  # Force refresh executes function again
  res3 = mock_get_symbols(force_refresh=True)
  assert len(res3) == 1
  assert len(calls) == 2


def test_get_twse_symbols(tmp_path):
  from unittest.mock import MagicMock
  from finance_agent.tools import get_twse_symbols

  sample_html = """
  <html>
    <body>
      <table>
        <tr><th>Col1</th><th>Col2</th><th>Col3</th><th>Col4</th><th>Col5</th></tr>
        <tr><td>1101 台泥</td><td>TW0001101004</td><td>2062/02/09</td><td>股票</td><td>水泥工業</td></tr>
        <tr><td>2330 台積電</td><td>TW0002330008</td><td>1994/09/05</td><td>股票</td><td>半導體業</td></tr>
        <tr><td>0050 元大台灣50</td><td>TW0000050004</td><td>2003/06/30</td><td>ETF</td><td>ETF</td></tr>
      </table>
    </body>
  </html>
  """

  mock_response = MagicMock()
  mock_response.content = sample_html.encode("big5")
  mock_response.raise_for_status.return_value = None

  with patch("requests.get", return_value=mock_response):
    with patch("finance_agent.tools.stock_info.cache") as mock_cache:
      # Bypass cache decorator for direct unit testing of get_twse_symbols logic
      mock_cache.side_effect = lambda **kwargs: lambda func: func
      symbols = get_twse_symbols()

      assert len(symbols) == 3
      assert symbols[0].symbol == "1101.TW"
      assert symbols[0].industrial_group == "水泥工業"
      assert symbols[1].symbol == "2330.TW"
      assert symbols[1].industrial_group == "半導體業"
      assert symbols[2].symbol == "0050.TW"
      assert symbols[2].industrial_group == "ETF"
