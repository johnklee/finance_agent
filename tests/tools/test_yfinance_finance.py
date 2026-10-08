import pytest
from unittest.mock import patch, MagicMock
from finance_agent.tools.yfinance_finance import (
  YahooFinanceProvider,
  _dump_stock_info_cache,
  _load_stock_info_cache,
)
from finance_agent.tools.exceptions import FinanceDataError
from finance_agent.tools import StockInfo, SymbolInfo


@pytest.fixture(autouse=True)
def isolate_cache_dir(tmp_path, monkeypatch):
  monkeypatch.chdir(tmp_path)


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
def test_yahoo_finance_provider_success(mock_ticker):
  # Arrange
  mock_ticker_instance = MagicMock()
  mock_ticker_instance.info = {
    "longName": "Test Company",
    "currency": "USD",
    "currentPrice": 150.0,
    "previousClose": 145.0,
    "marketCap": 1000000.0,
    "dividendRate": 7.5,
  }
  mock_ticker.return_value = mock_ticker_instance

  provider = YahooFinanceProvider()

  # Act
  stock_info = provider.get_stock_info("TEST")

  # Assert
  assert isinstance(stock_info, StockInfo)
  assert stock_info.company_name == "Test Company"
  assert stock_info.currency == "USD"
  assert stock_info.current_price == 150.0
  assert stock_info.previous_close_price == 145.0
  assert stock_info.market_cap == 1000000.0
  assert stock_info.stock_symbol == "TEST"
  assert stock_info.annual_dividend == 7.5
  assert stock_info.dividend_yield == 5.0
  mock_ticker.assert_called_once_with("TEST")


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
def test_yahoo_finance_provider_invalid_symbol(mock_ticker):
  # Arrange
  mock_ticker_instance = MagicMock()
  # yfinance often returns an empty dict or raises an exception for invalid symbols
  # Let's simulate an exception being raised by yfinance
  mock_ticker_instance.info = {}
  # We can mock a property access to raise an exception if needed,
  # but let's assume the provider checks if info is empty or raises an error
  # Let's mock yfinance raising an exception directly for simplicity in this test
  mock_ticker.side_effect = Exception("Invalid symbol")

  provider = YahooFinanceProvider()

  # Act & Assert
  with pytest.raises(FinanceDataError) as exc_info:
    provider.get_stock_info("INVALID")

  assert "Invalid symbol" in str(exc_info.value)


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
def test_yahoo_finance_provider_stock_not_exist(mock_ticker):
  # Arrange
  mock_ticker_instance = MagicMock()
  mock_ticker_instance.info = {"trailingPegRatio": None}
  mock_ticker.return_value = mock_ticker_instance

  provider = YahooFinanceProvider()

  # Act & Assert
  with pytest.raises(FinanceDataError) as exc_info:
    provider.get_stock_info("999999999")

  assert "No data found for symbol: 999999999" in str(exc_info.value)


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
@patch("finance_agent.tools.yfinance_finance.stock_id_to_symbol")
def test_yahoo_finance_provider_stock_id_integer(mock_stock_id_to_symbol, mock_ticker):
  # Arrange
  mock_stock_id_to_symbol.return_value = "2330.TW"
  mock_ticker_instance = MagicMock()
  mock_ticker_instance.info = {
    "longName": "TSMC",
    "currency": "TWD",
    "currentPrice": 600.0,
    "previousClose": 590.0,
    "marketCap": 15000000.0,
  }
  mock_ticker.return_value = mock_ticker_instance

  provider = YahooFinanceProvider()

  # Act
  stock_info = provider.get_stock_info(2330)

  # Assert
  assert stock_info.company_name == "TSMC"
  assert stock_info.current_price == 600.0
  assert stock_info.stock_symbol == "2330.TW"
  mock_stock_id_to_symbol.assert_called_once_with("2330")
  mock_ticker.assert_called_once_with("2330.TW")


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
@patch("finance_agent.tools.yfinance_finance.stock_id_to_symbol")
def test_yahoo_finance_provider_stock_id_string(mock_stock_id_to_symbol, mock_ticker):
  # Arrange
  mock_stock_id_to_symbol.return_value = "2330.TW"
  mock_ticker_instance = MagicMock()
  mock_ticker_instance.info = {
    "longName": "TSMC",
    "currency": "TWD",
    "currentPrice": 600.0,
    "previousClose": 590.0,
    "marketCap": 15000000.0,
  }
  mock_ticker.return_value = mock_ticker_instance

  provider = YahooFinanceProvider()

  # Act
  stock_info = provider.get_stock_info("2330")

  # Assert
  assert stock_info.company_name == "TSMC"
  assert stock_info.current_price == 600.0
  assert stock_info.stock_symbol == "2330.TW"
  mock_stock_id_to_symbol.assert_called_once_with("2330")
  mock_ticker.assert_called_once_with("2330.TW")


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
@patch("finance_agent.tools.yfinance_finance.stock_id_to_symbol")
def test_yahoo_finance_provider_stock_id_not_found_fallback(
  mock_stock_id_to_symbol, mock_ticker
):
  # Arrange
  from finance_agent.tools.exceptions import StockNotFoundError

  mock_stock_id_to_symbol.side_effect = StockNotFoundError("Not found")

  mock_ticker_instance = MagicMock()
  mock_ticker_instance.info = {
    "longName": "Fallback Company",
    "currency": "USD",
    "currentPrice": 100.0,
    "previousClose": 95.0,
    "marketCap": 500000.0,
  }
  mock_ticker.return_value = mock_ticker_instance

  provider = YahooFinanceProvider()

  # Act
  stock_info = provider.get_stock_info("2330.TW")

  # Assert
  assert stock_info.company_name == "Fallback Company"
  assert stock_info.current_price == 100.0
  assert stock_info.stock_symbol == "2330.TW"
  mock_stock_id_to_symbol.assert_called_once_with("2330.TW")
  mock_ticker.assert_called_once_with("2330.TW")


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
def test_yahoo_finance_provider_dividend_rate_fallback(mock_ticker):
  # Arrange
  mock_ticker_instance = MagicMock()
  mock_ticker_instance.info = {
    "longName": "Test Company",
    "currency": "USD",
    "currentPrice": 100.0,
    "previousClose": 95.0,
    "marketCap": 1000000.0,
    "trailingAnnualDividendRate": 5.0,
  }
  mock_ticker.return_value = mock_ticker_instance

  provider = YahooFinanceProvider()

  # Act
  stock_info = provider.get_stock_info("TEST")

  # Assert
  assert stock_info.annual_dividend == 5.0
  assert stock_info.dividend_yield == 5.0


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
def test_yahoo_finance_provider_get_latest_roe_success(mock_ticker):
  # Arrange
  mock_ticker_instance = MagicMock()
  mock_ticker_instance.info = {
    "returnOnEquity": 0.2153,
  }
  mock_ticker.return_value = mock_ticker_instance

  provider = YahooFinanceProvider()

  # Act
  roe = provider.get_latest_roe("TEST")

  # Assert
  assert roe == pytest.approx(21.53)
  mock_ticker.assert_called_once_with("TEST")


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
def test_yahoo_finance_provider_get_latest_roe_missing(mock_ticker):
  # Arrange
  mock_ticker_instance = MagicMock()
  mock_ticker_instance.info = {
    "longName": "Test Company",
  }
  mock_ticker.return_value = mock_ticker_instance

  provider = YahooFinanceProvider()

  # Act & Assert
  with pytest.raises(FinanceDataError) as exc_info:
    provider.get_latest_roe("TEST")

  assert "ROE is unavailable for symbol: TEST" in str(exc_info.value)


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
@patch("finance_agent.tools.yfinance_finance.stock_id_to_symbol")
def test_yahoo_finance_provider_get_latest_roe_with_id_resolution(
  mock_stock_id_to_symbol, mock_ticker
):
  # Arrange
  mock_stock_id_to_symbol.return_value = "2330.TW"
  mock_ticker_instance = MagicMock()
  mock_ticker_instance.info = {
    "returnOnEquity": 0.325,
  }
  mock_ticker.return_value = mock_ticker_instance

  provider = YahooFinanceProvider()

  # Act
  roe = provider.get_latest_roe(2330)

  # Assert
  assert roe == 32.5
  mock_stock_id_to_symbol.assert_called_once_with("2330")
  mock_ticker.assert_called_once_with("2330.TW")


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
def test_yahoo_finance_provider_get_latest_roe_empty_info(mock_ticker):
  # Arrange
  mock_ticker_instance = MagicMock()
  mock_ticker_instance.info = {}
  mock_ticker.return_value = mock_ticker_instance

  provider = YahooFinanceProvider()

  # Act & Assert
  with pytest.raises(FinanceDataError) as exc_info:
    provider.get_latest_roe("TEST")

  assert "No data found for symbol: TEST" in str(exc_info.value)


@patch("finance_agent.tools.yfinance_finance.yf.download")
def test_get_beta_success(mock_download):
  # Arrange
  import pandas as pd

  dates = pd.date_range("2026-01-01", periods=5)
  data = {
    ("Close", "TEST"): [10.0, 11.0, 12.0, 11.0, 13.0],
    ("Close", "^TWII"): [100.0, 101.0, 102.0, 101.0, 103.0],
  }
  mock_df = pd.DataFrame(data, index=dates)
  mock_download.return_value = mock_df

  provider = YahooFinanceProvider()

  # Act
  beta = provider.get_beta("TEST", "^TWII", period="1mo")

  # Assert
  assert isinstance(beta, float)
  assert beta == pytest.approx(8.976885215675251)
  mock_download.assert_called_once_with(
    tickers=["TEST", "^TWII"],
    period="1mo",
    auto_adjust=True,
    progress=False,
  )


@patch("finance_agent.tools.yfinance_finance.yf.download")
@patch("finance_agent.tools.yfinance_finance.stock_id_to_symbol")
def test_get_beta_with_id_resolution(mock_stock_id_to_symbol, mock_download):
  # Arrange
  import pandas as pd

  mock_stock_id_to_symbol.return_value = "2330.TW"
  dates = pd.date_range("2026-01-01", periods=5)
  data = {
    ("Close", "2330.TW"): [10.0, 11.0, 12.0, 11.0, 13.0],
    ("Close", "^TWII"): [100.0, 101.0, 102.0, 101.0, 103.0],
  }
  mock_df = pd.DataFrame(data, index=dates)
  mock_download.return_value = mock_df

  provider = YahooFinanceProvider()

  # Act
  beta = provider.get_beta(2330, "^TWII")

  # Assert
  assert beta == pytest.approx(8.976885215675251)
  mock_stock_id_to_symbol.assert_called_once_with("2330")
  mock_download.assert_called_once_with(
    tickers=["2330.TW", "^TWII"],
    period="5y",
    auto_adjust=True,
    progress=False,
  )


@patch("finance_agent.tools.yfinance_finance.yf.download")
def test_get_beta_empty_prices(mock_download):
  # Arrange
  import pandas as pd

  mock_download.return_value = pd.DataFrame()

  provider = YahooFinanceProvider()

  # Act & Assert
  with pytest.raises(FinanceDataError) as exc_info:
    provider.get_beta("TEST")

  assert "Unable to retrieve sufficient historical price data" in str(exc_info.value)


@patch("finance_agent.tools.yfinance_finance.yf.download")
def test_get_alpha_success(mock_download):
  # Arrange
  import pandas as pd

  dates = pd.date_range("2026-01-01", periods=5)
  # Design return data to give steady alpha
  data = {
    ("Close", "TEST"): [10.0, 10.1, 10.2, 10.3, 10.4],
    ("Close", "^TWII"): [100.0, 100.5, 101.0, 101.5, 102.0],
  }
  mock_df = pd.DataFrame(data, index=dates)
  mock_download.return_value = mock_df

  provider = YahooFinanceProvider()

  # Act
  alpha = provider.get_alpha("TEST", "^TWII", risk_free_rate=0.015, period="1mo")

  # Assert
  assert isinstance(alpha, float)
  mock_download.assert_called_once_with(
    tickers=["TEST", "^TWII"],
    period="1mo",
    auto_adjust=True,
    progress=False,
  )


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
def test_yahoo_finance_provider_symbol_info(mock_ticker):
  # Arrange
  mock_ticker_instance = MagicMock()
  mock_ticker_instance.info = {
    "longName": "TSMC",
    "currency": "TWD",
    "currentPrice": 600.0,
    "previousClose": 590.0,
    "marketCap": 15000000.0,
  }
  mock_ticker.return_value = mock_ticker_instance

  provider = YahooFinanceProvider()
  symbol_info = SymbolInfo(symbol="2330.TW", industrial_group="半導體業")

  # Act
  stock_info = provider.get_stock_info(symbol_info)

  # Assert
  assert stock_info.company_name == "TSMC"
  assert stock_info.current_price == 600.0
  assert stock_info.stock_symbol == "2330.TW"
  mock_ticker.assert_called_once_with("2330.TW")


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
def test_yahoo_finance_provider_get_latest_roe_with_symbol_info(mock_ticker):
  # Arrange
  mock_ticker_instance = MagicMock()
  mock_ticker_instance.info = {
    "returnOnEquity": 0.28,
  }
  mock_ticker.return_value = mock_ticker_instance

  provider = YahooFinanceProvider()
  symbol_info = SymbolInfo(symbol="2330.TW", industrial_group="半導體業")

  # Act
  roe = provider.get_latest_roe(symbol_info)

  # Assert
  assert roe == pytest.approx(28.0)
  mock_ticker.assert_called_once_with("2330.TW")


@patch("finance_agent.tools.yfinance_finance.yf.download")
def test_get_beta_with_symbol_info(mock_download):
  # Arrange
  import pandas as pd

  dates = pd.date_range("2026-01-01", periods=5)
  data = {
    ("Close", "2330.TW"): [10.0, 11.0, 12.0, 11.0, 13.0],
    ("Close", "^TWII"): [100.0, 101.0, 102.0, 101.0, 103.0],
  }
  mock_df = pd.DataFrame(data, index=dates)
  mock_download.return_value = mock_df

  provider = YahooFinanceProvider()
  symbol_info = SymbolInfo(symbol="2330.TW", industrial_group="半導體業")

  # Act
  beta = provider.get_beta(symbol_info, "^TWII")

  # Assert
  assert beta == pytest.approx(8.976885215675251)
  mock_download.assert_called_once_with(
    tickers=["2330.TW", "^TWII"],
    period="5y",
    auto_adjust=True,
    progress=False,
  )


@patch("finance_agent.tools.yfinance_finance.yf.download")
def test_get_alpha_with_symbol_info(mock_download):
  # Arrange
  import pandas as pd

  dates = pd.date_range("2026-01-01", periods=5)
  data = {
    ("Close", "2330.TW"): [10.0, 10.1, 10.2, 10.3, 10.4],
    ("Close", "^TWII"): [100.0, 100.5, 101.0, 101.5, 102.0],
  }
  mock_df = pd.DataFrame(data, index=dates)
  mock_download.return_value = mock_df

  provider = YahooFinanceProvider()
  symbol_info = SymbolInfo(symbol="2330.TW", industrial_group="半導體業")

  # Act
  alpha = provider.get_alpha(symbol_info, "^TWII", risk_free_rate=0.015, period="1mo")

  # Assert
  assert isinstance(alpha, float)
  mock_download.assert_called_once_with(
    tickers=["2330.TW", "^TWII"],
    period="1mo",
    auto_adjust=True,
    progress=False,
  )


def test_dump_and_load_stock_info_cache():
  stock = StockInfo(
    company_name="TSMC",
    currency="TWD",
    current_price=600.0,
    previous_close_price=590.0,
    market_cap=15000000.0,
    stock_symbol="2330.TW",
    annual_dividend=12.0,
  )
  df = _dump_stock_info_cache(stock)
  loaded = _load_stock_info_cache(df)
  assert loaded == stock

  stock_no_div = StockInfo(
    company_name="No Div Co",
    currency="TWD",
    current_price=50.0,
    previous_close_price=49.0,
    market_cap=500000.0,
    stock_symbol="1101.TW",
    annual_dividend=None,
  )
  df_no_div = _dump_stock_info_cache(stock_no_div)
  loaded_no_div = _load_stock_info_cache(df_no_div)
  assert loaded_no_div == stock_no_div


@patch("finance_agent.tools.yfinance_finance.yf.Ticker")
def test_yahoo_finance_provider_get_stock_info_cache(mock_ticker, tmp_path):
  info_map = {
    "2330.TW": {
      "longName": "TSMC",
      "currency": "TWD",
      "currentPrice": 600.0,
      "previousClose": 590.0,
      "marketCap": 15000000.0,
      "symbol": "2330.TW",
      "dividendRate": 12.0,
    },
    "2317.TW": {
      "longName": "Hon Hai",
      "currency": "TWD",
      "currentPrice": 200.0,
      "previousClose": 195.0,
      "marketCap": 3000000.0,
      "symbol": "2317.TW",
      "dividendRate": 5.5,
    },
  }

  def ticker_side_effect(sym: str):
    instance = MagicMock()
    instance.info = info_map[sym]
    return instance

  mock_ticker.side_effect = ticker_side_effect
  provider = YahooFinanceProvider()

  # First call for 2330.TW fetches from yfinance and writes cache
  res1 = provider.get_stock_info("2330.TW")
  assert res1.company_name == "TSMC"
  assert res1.stock_symbol == "2330.TW"
  assert mock_ticker.call_count == 1
  assert (tmp_path / "cache" / "stock_info_cache.csv").exists()

  # Second call for 2330.TW hits cache without calling yfinance
  res2 = provider.get_stock_info("2330.TW")
  assert res2 == res1
  assert mock_ticker.call_count == 1

  # Call for 2317.TW misses cache, fetches from yfinance, and appends to cache
  res3 = provider.get_stock_info("2317.TW")
  assert res3.company_name == "Hon Hai"
  assert res3.stock_symbol == "2317.TW"
  assert mock_ticker.call_count == 2

  # Subsequent calls for both 2330.TW and 2317.TW hit cache
  assert provider.get_stock_info("2330.TW") == res1
  assert provider.get_stock_info("2317.TW") == res3
  assert mock_ticker.call_count == 2

  # Flush forces re-fetch
  res_flushed = provider.get_stock_info("2330.TW", flush=True)
  assert res_flushed == res1
  assert mock_ticker.call_count == 3
