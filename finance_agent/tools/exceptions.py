"""Custom exceptions for the tools package."""


class FinanceDataError(Exception):
  """Exception raised for errors in the finance data provider."""

  pass


class StockNotFoundError(KeyError, FinanceDataError):
  """Exception raised when a stock ID is not found in twstock or the CSV cache."""

  pass
