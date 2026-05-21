from finance_agent.tools import BaseProvider, StockInfo


def test_base_provider_protocol():
    class DummyProvider(BaseProvider):
        def get_stock_info(self, symbol: str) -> StockInfo:
            return StockInfo(
                company_name="Test",
                currency="USD",
                current_price=100.0,
                previous_close_price=90.0,
                market_cap=1000.0,
            )

    provider = DummyProvider()
    assert isinstance(provider, BaseProvider)
