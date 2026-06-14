"""Package to keep tools/utilities used in the repo."""

import dataclasses
from typing import Protocol, runtime_checkable

from finance_agent.tools.stock_info import (
    csv_cache as csv_cache,
    stock_id_to_symbol as stock_id_to_symbol,
)


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

    company_name: str
    currency: str
    current_price: float
    previous_close_price: float
    market_cap: float


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
