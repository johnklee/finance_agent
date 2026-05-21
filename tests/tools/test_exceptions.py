import pytest
from finance_agent.tools.exceptions import FinanceDataError


def test_finance_data_error():
    with pytest.raises(FinanceDataError) as exc_info:
        raise FinanceDataError("Test error message")
    assert str(exc_info.value) == "Test error message"
