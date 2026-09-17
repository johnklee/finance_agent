"""Search utilities for querying top stocks by financial metrics."""

from collections.abc import Sequence

from finance_agent.tools import (
  BaseProvider as BaseProvider,
  StockInfo as StockInfo,
  SymbolInfo as SymbolInfo,
  TW_BENCHMARK_SYMBOL as TW_BENCHMARK_SYMBOL,
  get_twse_symbols,
)


def get_top_n_dividend_yield(
  data_provider: BaseProvider,
  n: int = 5,
) -> Sequence[StockInfo]:
  """Get top N TWSE stocks sorted by dividend yield in descending order.

  Iterates all `SymbolInfo` returned by `get_twse_symbols` and collects
  the top N `StockInfo` items sorted by `dividend_yield` descending.

  Args:
    data_provider: Finance data provider implementing `BaseProvider`.
    n: Number of top stocks to return (default: 5).

  Returns:
    Sequence of top N `StockInfo` instances sorted by `dividend_yield` desc.
  """
  if n <= 0:
    return []

  symbols: Sequence[SymbolInfo] = get_twse_symbols()
  stock_infos: list[StockInfo] = []

  for symbol_info in symbols:
    try:
      info = data_provider.get_stock_info(symbol_info)
    except Exception:
      continue

    if info.dividend_yield is not None:
      stock_infos.append(info)

  stock_infos.sort(
    key=lambda stock: (
      stock.dividend_yield if stock.dividend_yield is not None else float("-inf")
    ),
    reverse=True,
  )
  return stock_infos[:n]
