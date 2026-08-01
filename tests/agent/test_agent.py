"""Tests for ADK root_agent and tools in finance_agent.agent."""

from unittest.mock import MagicMock, patch
from google.adk.agents import Agent
from finance_agent.agent import (
  ADKAgent,
  FinanceAgent,
  get_alpha,
  get_beta,
  get_latest_roe,
  get_stock_info,
  root_agent,
)
from finance_agent.tools import StockInfo


def test_root_agent_definition():
  assert isinstance(root_agent, Agent)
  assert root_agent.name == "finance_agent"
  assert root_agent.model == "gemini-3.5-flash"
  assert root_agent.tools is not None
  tool_names = [tool.__name__ for tool in root_agent.tools]
  assert "get_stock_info" in tool_names
  assert "get_latest_roe" in tool_names
  assert "get_beta" in tool_names
  assert "get_alpha" in tool_names


def test_agent_aliases():
  assert ADKAgent is FinanceAgent


@patch("finance_agent.agent._provider.get_stock_info")
def test_get_stock_info_tool(mock_get_info):
  expected_info = StockInfo(
    company_name="TSMC",
    currency="TWD",
    current_price=600.0,
    previous_close_price=590.0,
    market_cap=15000000.0,
  )
  mock_get_info.return_value = expected_info

  result = get_stock_info("2330")

  assert result == expected_info
  mock_get_info.assert_called_once_with("2330")


@patch("finance_agent.agent._provider.get_latest_roe")
def test_get_latest_roe_tool(mock_get_roe):
  mock_get_roe.return_value = 25.5

  result = get_latest_roe("2330")

  assert result == 25.5
  mock_get_roe.assert_called_once_with("2330")


@patch("finance_agent.agent._provider.get_beta")
def test_get_beta_tool(mock_get_beta):
  mock_get_beta.return_value = 1.2

  result = get_beta("2330", benchmark_symbol="^TWII", period="1y")

  assert result == 1.2
  mock_get_beta.assert_called_once_with("2330", benchmark_symbol="^TWII", period="1y")


@patch("finance_agent.agent._provider.get_alpha")
def test_get_alpha_tool(mock_get_alpha):
  mock_get_alpha.return_value = 3.5

  result = get_alpha("2330", risk_free_rate=0.02)

  assert result == 3.5
  mock_get_alpha.assert_called_once_with(
    "2330", benchmark_symbol="^TWII", risk_free_rate=0.02, period="5y"
  )


def test_finance_agent_class():
  mock_provider = MagicMock()
  agent = FinanceAgent(provider=mock_provider)
  assert agent.root_agent is not None
  assert isinstance(agent.root_agent, Agent)
  assert agent.root_agent.model == "gemini-3.5-flash"


@patch("finance_agent.agent._provider.get_stock_info")
def test_get_stock_info_tool_exception(mock_get_info):
  mock_get_info.side_effect = Exception("Not found")

  result = get_stock_info("INVALID")

  assert isinstance(result, str)
  assert "Error fetching stock info for symbol 'INVALID': Not found" in result


@patch("finance_agent.agent._provider.get_latest_roe")
def test_get_latest_roe_tool_exception(mock_get_roe):
  mock_get_roe.side_effect = Exception("ROE unavailable")

  result = get_latest_roe("INVALID")

  assert isinstance(result, str)
  assert "Error fetching ROE for symbol 'INVALID': ROE unavailable" in result


@patch("finance_agent.agent._provider.get_beta")
def test_get_beta_tool_exception(mock_get_beta):
  mock_get_beta.side_effect = Exception("Insufficient data")

  result = get_beta("INVALID")

  assert isinstance(result, str)
  assert "Error calculating beta for symbol 'INVALID': Insufficient data" in result


@patch("finance_agent.agent._provider.get_alpha")
def test_get_alpha_tool_exception(mock_get_alpha):
  mock_get_alpha.side_effect = Exception("Insufficient data")

  result = get_alpha("INVALID")

  assert isinstance(result, str)
  assert "Error calculating alpha for symbol 'INVALID': Insufficient data" in result


def test_finance_agent_class_exception_handling():
  mock_provider = MagicMock()
  mock_provider.get_stock_info.side_effect = Exception("Stock error")
  mock_provider.get_latest_roe.side_effect = Exception("ROE error")
  mock_provider.get_beta.side_effect = Exception("Beta error")
  mock_provider.get_alpha.side_effect = Exception("Alpha error")

  agent = FinanceAgent(provider=mock_provider)
  tools = {tool.__name__: tool for tool in agent.root_agent.tools}

  assert "Error fetching stock info for symbol '9999': Stock error" in tools[
    "_get_stock_info"
  ]("9999")
  assert "Error fetching ROE for symbol '9999': ROE error" in tools["_get_latest_roe"](
    "9999"
  )
  assert "Error calculating beta for symbol '9999': Beta error" in tools["_get_beta"](
    "9999"
  )
  assert "Error calculating alpha for symbol '9999': Alpha error" in tools[
    "_get_alpha"
  ]("9999")
