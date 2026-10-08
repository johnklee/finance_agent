"""Search utilities for querying top stocks by financial metrics."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import TYPE_CHECKING

from tqdm import tqdm

from finance_agent.tools.exceptions import FinanceDataError
from finance_agent.tools.stock_info import SymbolInfo, get_twse_symbols

if TYPE_CHECKING:
  from finance_agent.tools import BaseProvider, StockInfo

logger = logging.getLogger(__name__)


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

  for symbol_info in tqdm(symbols):
    try:
      info = data_provider.get_stock_info(symbol_info)
    except (ValueError, KeyError, FinanceDataError) as e:
      logger.debug(f"Failed to fetch info for {symbol_info}: {e}")
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
