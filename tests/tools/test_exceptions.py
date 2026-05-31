import pytest
from finance_agent.tools.exceptions import FinanceDataError, StockNotFoundError


def test_finance_data_error():
    with pytest.raises(FinanceDataError) as exc_info:
        raise FinanceDataError("Test error message")
    assert str(exc_info.value) == "Test error message"


def test_stock_not_found_error():
    with pytest.raises(StockNotFoundError) as exc_info:
        raise StockNotFoundError("Stock ID 1111 not found")
    assert str(exc_info.value) == "'Stock ID 1111 not found'"
    assert isinstance(exc_info.value, KeyError)
    assert isinstance(exc_info.value, FinanceDataError)
