# finance_agent

`finance_agent` is a Python-based financial data agent designed to collect, cache, analyze, and query stock market data from multiple financial data sources.

The initial implementation focuses on the Taiwan stock market using data from Yahoo Finance.

---

# Features

## Data Collection

- Pull historical stock market data from Yahoo Finance
- Support Taiwan stock symbols (e.g. `2330.TW`, `0050.TW`)
- Scheduled or on-demand data synchronization

## Local Database Cache

- Store pulled historical data locally
- Initial database backend: SQLite
- Designed for future migration to PostgreSQL or other databases

## Agent-Based Query Interface

Users can interact with the agent using natural language queries such as:

- "Stocks that increased over 5% today"
- "Stocks with dividend yield over 5%"
- "Top gaining Taiwan stocks this week"
- "Show historical price trend for TSMC"

## Extensible Architecture

Planned future support:
- Multiple financial data providers
- Additional stock markets
- LLM-powered financial analysis
- Technical indicators
- Portfolio tracking
- REST API / Web UI

---

# Tech Stack

- Python
- SQLite
- Yahoo Finance
- `yfinance`
- SQLAlchemy (planned)
- Pandas
