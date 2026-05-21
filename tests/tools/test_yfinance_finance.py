import pytest
from unittest.mock import patch, MagicMock
from finance_agent.tools.yfinance_finance import YahooFinanceProvider
from finance_agent.tools.exceptions import FinanceDataError
from finance_agent.tools import StockInfo


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
