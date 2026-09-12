from finance_agent.tools import BaseProvider, StockInfo, SymbolInfo


def test_base_provider_protocol():
  class DummyProvider(BaseProvider):
    def get_stock_info(self, symbol: str | int | SymbolInfo) -> StockInfo:
      return StockInfo(
        company_name="Test",
        currency="USD",
        current_price=100.0,
        previous_close_price=90.0,
        market_cap=1000.0,
      )

  provider = DummyProvider()
  assert isinstance(provider, BaseProvider)


def test_symbol_info_export():
  info = SymbolInfo(symbol="2330.TW", industrial_group="半導體業")
  assert info.symbol == "2330.TW"
  assert info.industrial_group == "半導體業"
