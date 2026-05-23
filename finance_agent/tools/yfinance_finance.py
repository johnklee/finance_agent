"""Yahoo Finance data provider implementation."""

import yfinance as yf
from finance_agent.tools import BaseProvider, StockInfo
from finance_agent.tools.exceptions import FinanceDataError


class YahooFinanceProvider(BaseProvider):
    """Provider to get Finance data using yfinance."""

    def get_stock_info(self, symbol: str) -> StockInfo:
        """Gets stock information according to given symbol.

        Args:
         symbol: Stock symbol. e.g. `2330.TW`.

        Returns:
         Company information as `StockInfo`.

        Raises:
         FinanceDataError: If there is an error fetching data or the symbol is invalid.
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            if not info:
                raise FinanceDataError(f"No data found for symbol: {symbol}")

            return StockInfo(
                company_name=info.get("longName", ""),
                currency=info.get("currency", "TWD"),
                current_price=info.get("currentPrice", 0.0),
                previous_close_price=info.get("previousClose", 0.0),
                market_cap=info.get("marketCap", 0.0),
            )
        except Exception as e:
            raise FinanceDataError(f"Error fetching data for {symbol}: {e}") from e
