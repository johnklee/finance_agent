"""Yahoo Finance data provider implementation."""

import yfinance as yf
from finance_agent.tools import BaseProvider, StockInfo
from finance_agent.tools.exceptions import FinanceDataError, StockNotFoundError
from finance_agent.tools.stock_info import stock_id_to_symbol


class YahooFinanceProvider(BaseProvider):
    """Provider to get Finance data using yfinance."""

    def get_stock_info(self, symbol: str | int) -> StockInfo:
        """Gets stock information according to given symbol.

        Args:
         symbol: Stock symbol. e.g. `2330.TW` or ID `2330`.

        Returns:
         Company information as `StockInfo`.

        Raises:
         FinanceDataError: If there is an error fetching data or the symbol is invalid.
        """
        resolved_symbol = str(symbol)
        try:
            resolved_symbol = stock_id_to_symbol(resolved_symbol)
        except StockNotFoundError:
            # Fallback to querying yfinance directly with the original input string
            pass

        try:
            ticker = yf.Ticker(resolved_symbol)
            info = ticker.info

            if not info:
                raise FinanceDataError(f"No data found for symbol: {resolved_symbol}")

            return StockInfo(
                company_name=info.get("longName", ""),
                currency=info.get("currency", "TWD"),
                current_price=info.get("currentPrice", 0.0),
                previous_close_price=info.get("previousClose", 0.0),
                market_cap=info.get("marketCap", 0.0),
            )
        except Exception as e:
            if isinstance(e, FinanceDataError):
                raise
            raise FinanceDataError(
                f"Error fetching data for {resolved_symbol}: {e}"
            ) from e
