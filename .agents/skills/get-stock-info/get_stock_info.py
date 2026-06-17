#!/usr/bin/env python3
"""Retrieve stock information and display it as a markdown table."""

import sys

from finance_agent.tools import yfinance_finance


def format_market_cap(value: int | None) -> str:
    """Format market cap with thousands separators."""
    if value is None:
        return "N/A"

    return f"{value:,}"


def main() -> int:
    """Main entry point."""
    if len(sys.argv) != 2:
        print(
            "Usage: python get_stock_info.py <stock_id_or_symbol>",
            file=sys.stderr,
        )
        return 1

    stock = sys.argv[1]

    try:
        provider = yfinance_finance.YahooFinanceProvider()
        info = provider.get_stock_info(stock)

        print("| Field | Value |")
        print("|-------|-------|")
        print(f"| Company Name | {info.company_name} |")
        print(f"| Currency | {info.currency} |")
        print(f"| Current Price | {info.current_price} |")
        print(f"| Previous Close Price | {info.previous_close_price} |")
        print(f"| Market Cap | {format_market_cap(info.market_cap)} |")

        return 0

    except Exception as exc:
        print(
            f"Failed to retrieve stock information: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
