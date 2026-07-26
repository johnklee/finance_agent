"""Package for ADK agent implementation in finance_agent."""

import warnings

from google.adk.agents import Agent
from finance_agent.tools import BaseProvider, StockInfo, TW_BENCHMARK_SYMBOL
from finance_agent.tools.yfinance_finance import YahooFinanceProvider

# Suppress experimental UserWarnings emitted by ADK framework
warnings.filterwarnings("ignore", category=UserWarning, module=r".*google\.adk.*")
warnings.filterwarnings("ignore", category=UserWarning, message=r".*\[EXPERIMENTAL\].*")

# Default provider instance for tool functions
_provider: BaseProvider = YahooFinanceProvider()


def get_stock_info(symbol: str | int) -> StockInfo:
  """Gets stock information including price, market cap, and dividend yield.

  Args:
    symbol: Stock symbol or Taiwan stock ID (e.g., '2330.TW' or 2330).

  Returns:
    StockInfo dataclass containing company details.
  """
  return _provider.get_stock_info(symbol)


def get_latest_roe(symbol: str | int) -> float:
  """Gets the latest Return on Equity (ROE) percentage for a given stock.

  Args:
    symbol: Stock symbol or Taiwan stock ID (e.g., '2330.TW' or 2330).

  Returns:
    Latest ROE as a percentage float.
  """
  return _provider.get_latest_roe(symbol)


def get_beta(
  symbol: str | int,
  benchmark_symbol: str = TW_BENCHMARK_SYMBOL,
  period: str = "5y",
) -> float:
  """Calculates a stock's beta relative to a benchmark index.

  Args:
    symbol: Stock symbol or Taiwan stock ID (e.g., '2330.TW' or 2330).
    benchmark_symbol: Benchmark index symbol (default: ^TWII).
    period: Historical period (e.g., '1y', '5y').

  Returns:
    Calculated beta as a float.
  """
  return _provider.get_beta(symbol, benchmark_symbol=benchmark_symbol, period=period)


def get_alpha(
  symbol: str | int,
  benchmark_symbol: str = TW_BENCHMARK_SYMBOL,
  risk_free_rate: float = 0.015,
  period: str = "5y",
) -> float:
  """Calculates CAPM Alpha for a stock relative to a benchmark index.

  Args:
    symbol: Stock symbol or Taiwan stock ID (e.g., '2330.TW' or 2330).
    benchmark_symbol: Benchmark index symbol (default: ^TWII).
    risk_free_rate: Annual risk-free rate decimal (default: 0.015).
    period: Historical period (e.g., '1y', '5y').

  Returns:
    Annualized alpha as a percentage float.
  """
  return _provider.get_alpha(
    symbol,
    benchmark_symbol=benchmark_symbol,
    risk_free_rate=risk_free_rate,
    period=period,
  )


# Expose root_agent for ADK CLI (adk run / adk web)
root_agent = Agent(
  name="finance_agent",
  model="gemini-3.5-flash",
  description="Financial stock data agent providing stock info, ROE, Beta, and Alpha analysis.",
  instruction=(
    "You are a helpful financial assistant capable of querying stock market data, "
    "evaluating ROE, and calculating financial metrics like Beta and Alpha. "
    "Always use the provided tools to retrieve real-time and historical financial data."
  ),
  tools=[get_stock_info, get_latest_roe, get_beta, get_alpha],
)


class FinanceAgent:
  """Wrapper class managing an ADK Agent instance and its provider."""

  def __init__(self, provider: BaseProvider | None = None) -> None:
    """Initializes FinanceAgent with a data provider.

    Args:
      provider: Optional BaseProvider instance. Defaults to YahooFinanceProvider.
    """
    self.provider: BaseProvider = (
      provider if provider is not None else YahooFinanceProvider()
    )

    def _get_stock_info(symbol: str | int) -> StockInfo:
      return self.provider.get_stock_info(symbol)

    def _get_latest_roe(symbol: str | int) -> float:
      return self.provider.get_latest_roe(symbol)

    def _get_beta(
      symbol: str | int,
      benchmark_symbol: str = TW_BENCHMARK_SYMBOL,
      period: str = "5y",
    ) -> float:
      return self.provider.get_beta(
        symbol, benchmark_symbol=benchmark_symbol, period=period
      )

    def _get_alpha(
      symbol: str | int,
      benchmark_symbol: str = TW_BENCHMARK_SYMBOL,
      risk_free_rate: float = 0.015,
      period: str = "5y",
    ) -> float:
      return self.provider.get_alpha(
        symbol,
        benchmark_symbol=benchmark_symbol,
        risk_free_rate=risk_free_rate,
        period=period,
      )

    self.root_agent = Agent(
      name="finance_agent",
      model="gemini-3.5-flash",
      description="Financial stock market data agent.",
      instruction=(
        "You are a helpful financial assistant. Use provided tools for queries."
      ),
      tools=[_get_stock_info, _get_latest_roe, _get_beta, _get_alpha],
    )


ADKAgent = FinanceAgent

__all__ = [
  "root_agent",
  "FinanceAgent",
  "ADKAgent",
  "get_stock_info",
  "get_latest_roe",
  "get_beta",
  "get_alpha",
]
