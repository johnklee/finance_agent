"""Package to keep tools/utilities used in the repo."""

import dataclasses
from typing import Protocol, runtime_checkable

from finance_agent import constants
from finance_agent.tools.stock_info import (
  SymbolInfo as SymbolInfo,
  cache as cache,
  csv_cache as csv_cache,
  get_twse_symbols as get_twse_symbols,
  stock_id_to_symbol as stock_id_to_symbol,
)


TW_BENCHMARK_SYMBOL = constants.TW_BENCHMARK_SYMBOL


@dataclasses.dataclass(frozen=True, kw_only=True)
class StockInfo:
  """Stock information.

  Attributes:
    company_name: Company name. e.g. `Taiwan Semiconductor Manufacturing Company Limited`
    currency: Currency unit. e.g. `TWD` (default).
    current_price: Current stock price
    previous_close_price: Previous close price.
    market_cap: Market capitalization.
  """

  annual_dividend: float | None = None
  company_name: str
  currency: str
  current_price: float
  previous_close_price: float
  market_cap: float

  @property
  def dividend_yield(self) -> float | None:
    """Calculates the dividend yield as a percentage."""
    if self.annual_dividend is None or not self.current_price:
      return None
    return (self.annual_dividend / self.current_price) * 100


@runtime_checkable
class BaseProvider(Protocol):
  """Provider base class to get Finance data."""

  def get_stock_info(self, symbol: str | int) -> StockInfo:
    """Gets stock information according to given sympol.

    Args:
      symbol: Stock symbol. e.g. `2330.TW` or ID `2330`

    Returns:
      Compony information as `StockInfo`.
    """
    pass

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
    pass

  def get_beta(
    self,
    symbol: str | int,
    benchmark_symbol: str = TW_BENCHMARK_SYMBOL,
    period: str = "5y",
  ) -> float:
    """
    Calculate a stock's beta relative to a benchmark index.

    Beta measures how sensitive a stock's returns are to benchmark returns:
    - beta = 1.0: moves roughly in line with the benchmark
    - beta > 1.0: tends to be more volatile than the benchmark
    - beta < 1.0: tends to be less volatile than the benchmark
    - beta < 0.0: tends to move in the opposite direction

    Args:
      symbol: Stock symbol. e.g. `2330.TW` or ID `2330`
      benchmark_symbol: Benchmark ticker, default is "^GSPC" for S&P 500.
      period: Historical-data period accepted by yfinance, for example
          "1y", "2y", "5y", or "10y".

    Returns:
      The calculated beta as a float.

    Raises:
      ValueError: If historical price data is unavailable or insufficient.
    """
    pass

  def get_alpha(
    self,
    symbol: str | int,
    benchmark_symbol: str = TW_BENCHMARK_SYMBOL,
    risk_free_rate: float = 0.015,
    period: str = "5y",
  ) -> float:
    """
    Calculate CAPM Alpha.

    Formula:
      alpha = Ri - [Rf + beta * (Rm - Rf)]

    Args:
      symbol: Stock symbol. e.g. `2330.TW` or ID `2330`
      benchmark_symbol: Market index (e.g. "^TWII", "^GSPC")
      risk_free_rate: Annual risk-free rate in decimal form.
        Example: 0.015 = 1.5%, 0.04  = 4%
      period: Historical period used to estimate returns and beta.

    Returns:
      Annualized alpha (percentage).
      Example: 3.2 means 3.2%
    """
    pass
