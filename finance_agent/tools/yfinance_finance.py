"""Yahoo Finance data provider implementation."""

import pandas as pd
import yfinance as yf
from finance_agent.tools import BaseProvider, StockInfo, TW_BENCHMARK_SYMBOL
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
        annual_dividend=info.get("dividendRate")
        or info.get("trailingAnnualDividendRate"),
      )
    except Exception as e:
      if isinstance(e, FinanceDataError):
        raise
      raise FinanceDataError(f"Error fetching data for {resolved_symbol}: {e}") from e

  def get_latest_roe(self, symbol: str | int) -> float:
    """Gets latest ROE of given stock sympol/ID.

    Args:
      symbol: Stock symbol/ID. e.g. `2330.TW` or ID `2330`

    Returns:
      Latest ROE as a percentage.

      For example:
      - ``21.53`` represents **21.53%**
      - ``8.41`` represents **8.41%**
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

      roe = info.get("returnOnEquity")
      if roe is None:
        raise FinanceDataError(f"ROE is unavailable for symbol: {resolved_symbol}")

      # Yahoo Finance returns a decimal (e.g. 0.2153). Convert to percentage.
      return float(roe) * 100.0
    except Exception as e:
      if isinstance(e, FinanceDataError):
        raise
      raise FinanceDataError(f"Error fetching data for {resolved_symbol}: {e}") from e

  def get_beta(
    self,
    symbol: str | int,
    benchmark_symbol: str = TW_BENCHMARK_SYMBOL,
    period: str = "5y",
  ) -> float:
    """Calculate a stock's beta relative to a benchmark index.

    Beta measures how sensitive a stock's returns are to benchmark returns:
    - beta = 1.0: moves roughly in line with the benchmark
    - beta > 1.0: tends to be more volatile than the benchmark
    - beta < 1.0: tends to be less volatile than the benchmark
    - beta < 0.0: tends to move in the opposite direction

    Args:
      symbol: Stock symbol. e.g. "2330.TW" or ID "2330"
      benchmark_symbol: Benchmark ticker, default is "^GSPC" for S&P 500.
      period: Historical-data period accepted by yfinance, for example
          "1y", "2y", "5y", or "10y".

    Returns:
      The calculated beta as a float.

    Raises:
      FinanceDataError: If historical price data is unavailable or insufficient.
    """
    resolved_symbol = str(symbol)
    try:
      resolved_symbol = stock_id_to_symbol(resolved_symbol)
    except StockNotFoundError:
      pass

    try:
      prices = yf.download(
        tickers=[resolved_symbol, benchmark_symbol],
        period=period,
        auto_adjust=True,
        progress=False,
      )

      if prices.empty:
        raise FinanceDataError("Unable to retrieve sufficient historical price data.")

      close_prices = prices["Close"]
      if close_prices.empty or close_prices.shape[1] < 2:
        raise FinanceDataError("Unable to retrieve sufficient historical price data.")

      close_prices = close_prices.dropna()
      returns = close_prices.pct_change().dropna()

      if returns.empty:
        raise FinanceDataError("Insufficient historical price data after processing.")

      stock_returns = returns[resolved_symbol]
      benchmark_returns = returns[benchmark_symbol]

      cov = stock_returns.cov(benchmark_returns)
      var = benchmark_returns.var()

      if var == 0 or pd.isna(var):
        raise FinanceDataError("Benchmark variance is zero or NaN.")

      beta = cov / var
      if pd.isna(beta):
        raise FinanceDataError("Calculated beta is NaN.")

      return float(beta)
    except Exception as e:
      if isinstance(e, FinanceDataError):
        raise
      raise FinanceDataError(
        f"Error calculating beta for {resolved_symbol}: {e}"
      ) from e

  def get_alpha(
    self,
    symbol: str | int,
    benchmark_symbol: str = TW_BENCHMARK_SYMBOL,
    risk_free_rate: float = 0.015,
    period: str = "5y",
  ) -> float:
    """Calculate CAPM Alpha.

    Formula:
      alpha = Ri - [Rf + beta * (Rm - Rf)]

    Args:
      symbol: Stock symbol. e.g. "2330.TW" or ID "2330"
      benchmark_symbol: Market index (e.g. "^TWII", "^GSPC")
      risk_free_rate: Annual risk-free rate in decimal form.
        Example: 0.015 = 1.5%, 0.04  = 4%
      period: Historical period used to estimate returns and beta.

    Returns:
      Annualized alpha (percentage).
      Example: 3.2 means 3.2%
    """
    resolved_symbol = str(symbol)
    try:
      resolved_symbol = stock_id_to_symbol(resolved_symbol)
    except StockNotFoundError:
      pass

    try:
      prices = yf.download(
        tickers=[resolved_symbol, benchmark_symbol],
        period=period,
        auto_adjust=True,
        progress=False,
      )

      if prices.empty:
        raise FinanceDataError("Unable to retrieve sufficient historical price data.")

      close_prices = prices["Close"]
      if close_prices.empty or close_prices.shape[1] < 2:
        raise FinanceDataError("Unable to retrieve sufficient historical price data.")

      close_prices = close_prices.dropna()

      stock_prices = close_prices[resolved_symbol]
      market_prices = close_prices[benchmark_symbol]

      stock_returns = stock_prices.pct_change().dropna()
      market_returns = market_prices.pct_change().dropna()

      returns = pd.concat(
        [stock_returns, market_returns],
        axis=1,
        join="inner",
      )

      if returns.empty:
        raise FinanceDataError("Insufficient historical price data after processing.")

      returns.columns = ["stock", "market"]

      covariance = returns["stock"].cov(returns["market"])
      market_variance = returns["market"].var()

      if market_variance == 0 or pd.isna(market_variance):
        raise FinanceDataError("Benchmark variance is zero or NaN.")

      beta = covariance / market_variance
      if pd.isna(beta):
        raise FinanceDataError("Calculated beta is NaN.")

      trading_days = 252

      ri = (1 + returns["stock"].mean()) ** trading_days - 1
      rm = (1 + returns["market"].mean()) ** trading_days - 1

      alpha = ri - (risk_free_rate + beta * (rm - risk_free_rate))

      if pd.isna(alpha):
        raise FinanceDataError("Calculated alpha is NaN.")

      return float(alpha) * 100.0
    except Exception as e:
      if isinstance(e, FinanceDataError):
        raise
      raise FinanceDataError(
        f"Error calculating alpha for {resolved_symbol}: {e}"
      ) from e
