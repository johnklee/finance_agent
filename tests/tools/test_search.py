import pytest
from unittest.mock import MagicMock, patch

from finance_agent.tools import BaseProvider, StockInfo, SymbolInfo
from finance_agent.tools.exceptions import FinanceDataError
from finance_agent.tools.search import get_top_n_dividend_yield


def _make_stock(
  name: str,
  price: float = 100.0,
  annual_dividend: float | None = None,
  stock_symbol: str = "2330.TW",
) -> StockInfo:
  return StockInfo(
    company_name=name,
    currency="TWD",
    current_price=price,
    previous_close_price=price,
    market_cap=1_000_000.0,
    stock_symbol=stock_symbol,
    annual_dividend=annual_dividend,
  )


def test_get_top_n_dividend_yield_basic():
  symbols = [
    SymbolInfo(symbol="1101.TW", industrial_group="水泥工業"),
    SymbolInfo(symbol="2330.TW", industrial_group="半導體業"),
    SymbolInfo(symbol="2412.TW", industrial_group="通信網路業"),
    SymbolInfo(symbol="2881.TW", industrial_group="金融保險業"),
  ]
  stock_map = {
    "1101.TW": _make_stock("Taiwan Cement", price=100.0, annual_dividend=4.0),  # 4%
    "2330.TW": _make_stock("TSMC", price=100.0, annual_dividend=2.0),  # 2%
    "2412.TW": _make_stock(
      "Chunghwa Telecom", price=100.0, annual_dividend=6.5
    ),  # 6.5%
    "2881.TW": _make_stock("Fubon Financial", price=100.0, annual_dividend=8.0),  # 8%
  }

  provider = MagicMock(spec=BaseProvider)
  provider.get_stock_info.side_effect = lambda s: stock_map[
    s.symbol if isinstance(s, SymbolInfo) else str(s)
  ]

  with patch("finance_agent.tools.search.get_twse_symbols", return_value=symbols):
    top_2 = get_top_n_dividend_yield(provider, n=2)

  assert len(top_2) == 2
  assert top_2[0].company_name == "Fubon Financial"
  assert top_2[0].dividend_yield == pytest.approx(8.0)
  assert top_2[1].company_name == "Chunghwa Telecom"
  assert top_2[1].dividend_yield == pytest.approx(6.5)


def test_get_top_n_dividend_yield_default_n():
  symbols = [
    SymbolInfo(symbol=f"{1000 + i}.TW", industrial_group="Group") for i in range(7)
  ]
  stock_map = {
    f"{1000 + i}.TW": _make_stock(
      f"Stock {i}", price=100.0, annual_dividend=float(i + 1)
    )
    for i in range(7)
  }

  provider = MagicMock(spec=BaseProvider)
  provider.get_stock_info.side_effect = lambda s: stock_map[
    s.symbol if isinstance(s, SymbolInfo) else str(s)
  ]

  with patch("finance_agent.tools.search.get_twse_symbols", return_value=symbols):
    result = get_top_n_dividend_yield(provider)

  assert len(result) == 5
  assert [s.dividend_yield for s in result] == pytest.approx([7.0, 6.0, 5.0, 4.0, 3.0])


def test_get_top_n_dividend_yield_skips_none_and_errors():
  symbols = [
    SymbolInfo(symbol="1101.TW", industrial_group="水泥工業"),
    SymbolInfo(symbol="2330.TW", industrial_group="半導體業"),
    SymbolInfo(symbol="9999.TW", industrial_group="其他"),
    SymbolInfo(symbol="2412.TW", industrial_group="通信網路業"),
  ]

  def side_effect(s: SymbolInfo | str | int) -> StockInfo:
    sym = s.symbol if isinstance(s, SymbolInfo) else str(s)
    if sym == "1101.TW":
      return _make_stock("No Dividend Stock", price=100.0, annual_dividend=None)
    if sym == "2330.TW":
      return _make_stock("TSMC", price=100.0, annual_dividend=3.5)
    if sym == "9999.TW":
      raise FinanceDataError("Failed to fetch stock data")
    return _make_stock("Chunghwa Telecom", price=100.0, annual_dividend=5.0)

  provider = MagicMock(spec=BaseProvider)
  provider.get_stock_info.side_effect = side_effect

  with patch("finance_agent.tools.search.get_twse_symbols", return_value=symbols):
    result = get_top_n_dividend_yield(provider, n=5)

  assert len(result) == 2
  assert result[0].company_name == "Chunghwa Telecom"
  assert result[1].company_name == "TSMC"


def test_get_top_n_dividend_yield_non_positive_n():
  provider = MagicMock(spec=BaseProvider)
  with patch("finance_agent.tools.search.get_twse_symbols") as mock_symbols:
    assert get_top_n_dividend_yield(provider, n=0) == []
    assert get_top_n_dividend_yield(provider, n=-1) == []
    mock_symbols.assert_not_called()
