"""Package to keep tools/utilities used in the repo."""

import dataclasses
from typing import Protocol


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


class BaseProvider(Protocol):
    """Provider base class to get Finance data."""

    def get_stock_info(self, symbol: str) -> StockInfo:
        """Gets stock information according to given sympol.

        Args:
          symbol: Stock symtol. e.g. `2330.TW`.

        Returns:
          Compony information as `StockInfo`.
        """
        pass
