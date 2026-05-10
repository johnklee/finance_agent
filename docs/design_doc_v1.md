# finance_agent — System Design Document

## 1. Overview

`finance_agent` is a Python-based financial data agent built using an Agent Development Kit (ADK) architecture.

The repository is designed primarily as an intelligent agent system rather than a standalone application. Its core responsibility is to collect, cache, analyze, and query financial market data using modular agent skills and tools.

The initial implementation focuses on Taiwan stock market data sourced from Yahoo Finance.

Although the repository is agent-centric, all core modules are designed with clean separation and loose coupling so they can also be reused independently as Python libraries.

---

# 2. Design Goals

## Primary Goals

- Provide an ADK-compatible financial data agent
- Support natural language financial queries
- Cache historical market data locally
- Build modular and reusable components
- Support future multi-provider expansion

---

## Secondary Goals

- Reusable Python library modules
- Easy integration with other agents
- Easy migration from SQLite to PostgreSQL
- Extensible analytics framework

---

## Non-Goals (Phase 1)

- Real-time trading
- High-frequency streaming
- Broker integration
- Portfolio optimization engine
- Production-grade distributed system

---

# 3. System Architecture

```text
+------------------------------------------------------+
|                    User / Caller                     |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
|                    ADK Agent Layer                   |
|------------------------------------------------------|
| finance_agent                                        |
|                                                      |
| - Intent Handling                                    |
| - Tool Routing                                       |
| - Reasoning                                           |
| - Response Generation                                |
+------------------------------------------------------+
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
+----------------------+      +--------------------------+
|   Tool / Skill APIs  |      |    Reusable Libraries    |
|----------------------|      |--------------------------|
| sync_stock_data()    |      | analytics module         |
| screen_stocks()      |      | database module          |
| query_stock()        |      | providers module         |
| get_price_history()  |      | indicators module        |
+----------------------+      +--------------------------+
                           |
                           v
+------------------------------------------------------+
|                  Service Layer                       |
|------------------------------------------------------|
| Sync Service                                         |
| Analytics Service                                    |
| Screening Service                                    |
| Query Service                                        |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
|                Provider Abstraction                  |
|------------------------------------------------------|
| Yahoo Finance Provider                               |
| Future Providers                                     |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
|                  Persistence Layer                   |
|------------------------------------------------------|
| SQLite                                               |
| SQLAlchemy ORM                                       |
+------------------------------------------------------+
```

---

# 4. Architectural Principles

## 4.1 Agent-First Design

The repository is primarily designed to function as an intelligent financial agent.

The agent is responsible for:

- Understanding user intent
- Selecting appropriate tools
- Executing analytics workflows
- Returning human-readable responses

---

## 4.2 Library Reusability

All major components should remain independently reusable.

Example:

```python
from finance_agent.analytics.screening import screen_top_gainers
from finance_agent.providers.yahoo_finance import YahooFinanceProvider
```

This enables:

- Independent scripting
- Jupyter notebook usage
- API integration
- Reuse by other agents

---

## 4.3 Provider Abstraction

External data providers should be isolated behind a common interface.

This avoids tight coupling to Yahoo Finance.

---

## 4.4 Clean Separation of Concerns

| Layer | Responsibility |
|---|---|
| Agent Layer | Intent + orchestration |
| Tools | Executable capabilities |
| Services | Business logic |
| Providers | External APIs |
| Database | Persistence |
| Analytics | Financial calculations |

---

# 5. ADK Agent Design

## 5.1 Agent Responsibilities

The ADK-based agent should:

- Interpret natural language requests
- Decide which tools to invoke
- Aggregate analytical results
- Generate structured responses

---

## 5.2 Example User Queries

```text
Stocks that increased over 5% today
```

```text
Top gaining Taiwan stocks this week
```

```text
Show historical price trend for TSMC
```

```text
Stocks with dividend yield over 5%
```

---

## 5.3 Example Tool Invocation Flow

```text
User Query
    |
    v
finance_agent
    |
    v
Intent Parsing
    |
    v
Tool Selection
    |
    v
Analytics / Database Query
    |
    v
Response Formatting
```

---

# 6. Core Modules

---

# 6.1 Provider Layer

Responsible for retrieving external financial data.

## Initial Provider

- Yahoo Finance
- Python package: `yfinance`

---

## Provider Interface

```python
class BaseProvider:
    def get_historical_prices(self, symbol, start, end):
        pass

    def get_stock_info(self, symbol):
        pass

    def get_dividend_history(self, symbol):
        pass
```

---

## Yahoo Finance Provider

```python
class YahooFinanceProvider(BaseProvider):
    ...
```

Responsibilities:

- Historical OHLCV retrieval
- Dividend retrieval
- Metadata retrieval
- Data normalization

---

# 6.2 Database Layer

Responsible for local caching and persistence.

---

## Initial Backend

- SQLite

---

## Future Backends

- PostgreSQL
- MySQL

---

## ORM

- SQLAlchemy

---

## Design Goals

- Database abstraction
- Minimal provider coupling
- Easy migration support

---

# 6.3 Analytics Layer

Responsible for financial calculations and stock screening.

---

## Supported Metrics (Phase 1)

| Metric | Description |
|---|---|
| Daily Return | Percentage increase/decrease |
| Weekly Return | 7-day performance |
| Dividend Yield | Dividend vs current price |
| Volume Ranking | Trading volume ranking |

---

## Future Metrics

- RSI
- MACD
- Moving Average
- Bollinger Bands
- Volatility
- Sharpe Ratio

---

# 6.4 Service Layer

Encapsulates business logic.

---

## Sync Service

Responsible for:

- Full synchronization
- Incremental synchronization
- Retry handling
- Validation

---

## Query Service

Responsible for:

- Query execution
- Filtering
- Sorting
- Aggregation

---

## Analytics Service

Responsible for:

- Financial calculations
- Ranking
- Screening logic

---

# 6.5 Tool Layer

Agent-accessible executable capabilities.

---

## Example Tools

| Tool | Description |
|---|---|
| sync_stock_data | Synchronize market data |
| query_stock | Retrieve stock information |
| get_price_history | Retrieve historical prices |
| screen_stocks | Run stock screening |
| calculate_indicator | Technical analysis |

---

## Example Tool Signature

```python
def screen_stocks(
    metric: str,
    operator: str,
    value: float
):
    pass
```

---

# 7. Database Design

---

# 7.1 stocks

Stores stock metadata.

| Column | Type |
|---|---|
| id | INTEGER |
| symbol | TEXT |
| name | TEXT |
| market | TEXT |
| sector | TEXT |
| currency | TEXT |
| created_at | DATETIME |

---

# 7.2 historical_prices

Stores OHLCV historical data.

| Column | Type |
|---|---|
| id | INTEGER |
| stock_id | INTEGER |
| trade_date | DATE |
| open_price | FLOAT |
| high_price | FLOAT |
| low_price | FLOAT |
| close_price | FLOAT |
| adjusted_close | FLOAT |
| volume | BIGINT |
| dividend | FLOAT |
| stock_split | FLOAT |
| created_at | DATETIME |

---

## Recommended Index

```sql
CREATE INDEX idx_stock_date
ON historical_prices(stock_id, trade_date);
```

---

# 7.3 dividend_history

| Column | Type |
|---|---|
| id | INTEGER |
| stock_id | INTEGER |
| ex_dividend_date | DATE |
| dividend_amount | FLOAT |

---

# 8. Suggested Repository Structure

```text
finance_agent/
│
├── finance_agent/
│   │
│   ├── agent/
│   │   ├── finance_agent.py
│   │   ├── intent_parser.py
│   │   └── response_generator.py
│   │
│   ├── tools/
│   │   ├── sync_tools.py
│   │   ├── screening_tools.py
│   │   └── query_tools.py
│   │
│   ├── services/
│   │   ├── sync_service.py
│   │   ├── analytics_service.py
│   │   └── query_service.py
│   │
│   ├── providers/
│   │   ├── base_provider.py
│   │   └── yahoo_finance.py
│   │
│   ├── analytics/
│   │   ├── indicators.py
│   │   ├── screening.py
│   │   └── calculations.py
│   │
│   ├── database/
│   │   ├── models.py
│   │   ├── repository.py
│   │   └── session.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   └── utils/
│       └── logging.py
│
├── tests/
│
├── scripts/
│   ├── sync_all.py
│   └── bootstrap_db.py
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# 9. Data Flow

---

## Historical Sync Flow

```text
Scheduler / Agent Tool
        |
        v
Sync Service
        |
        v
Yahoo Finance Provider
        |
        v
Normalize Data
        |
        v
Store into SQLite
```

---

## Agent Query Flow

```text
User Query
    |
    v
finance_agent
    |
    v
Intent Parsing
    |
    v
Tool Invocation
    |
    v
Analytics / Database Query
    |
    v
Formatted Response
```

---

# 10. Natural Language Query Design

The agent should translate user requests into structured operations.

---

## Example

Input:

```text
Stocks that increased over 5% today
```

Internal Representation:

```json
{
  "metric": "daily_return",
  "operator": ">",
  "value": 5
}
```

---

# 11. Error Handling

| Scenario | Handling |
|---|---|
| Invalid symbol | Validation error |
| Yahoo Finance unavailable | Retry with backoff |
| Missing market data | Warning + skip |
| Database failure | Transaction rollback |

---

# 12. Logging Strategy

Use Python `logging`.

---

## Recommended Log Levels

| Level | Usage |
|---|---|
| INFO | Sync status |
| WARNING | Missing data |
| ERROR | Provider failures |
| DEBUG | SQL/debug details |

---

# 13. Scalability Strategy

---

## Current Scale

SQLite is sufficient for:

- Local development
- Single-user workflows
- Moderate historical datasets

---

## Future Migration

Planned migration path:

```text
SQLite
   ->
PostgreSQL
   ->
Distributed Analytics Stack
```

Using SQLAlchemy minimizes migration effort.

---

# 14. Testing Strategy

---

## Unit Tests

- Provider adapters
- Analytics functions
- Tool logic
- Query parsing

---

## Integration Tests

- End-to-end synchronization
- Database persistence
- Tool invocation workflows

---

## Mocking

Mock:

- Yahoo Finance responses
- Database interactions
- Agent tool outputs

---

# 15. Future Enhancements

---

## Multi-Provider Support

- Alpha Vantage
- Polygon.io
- FinMind
- TWSE APIs

---

## AI Features

- LLM-powered screening
- Earnings summarization
- Trend explanation
- Investment assistant workflows

---

## Technical Analysis

- RSI
- MACD
- Moving averages
- Candlestick analysis

---

## External Interfaces

- REST API
- Streamlit dashboard
- Web UI
- Telegram/Discord agent integration

---

# 16. Recommended Milestones

---

## Milestone 1 — Core Infrastructure

- SQLite schema
- Yahoo Finance provider
- Historical synchronization

---

## Milestone 2 — Analytics

- Screening engine
- Return calculations
- Dividend calculations

---

## Milestone 3 — Agent Integration

- ADK tool integration
- Intent handling
- Response generation

---

## Milestone 4 — Advanced Features

- LLM integration
- Technical indicators
- Multi-provider support

---

# 17. Recommended Python Packages

| Purpose | Package |
|---|---|
| Financial data | `yfinance` |
| Data processing | `pandas` |
| ORM | `sqlalchemy` |
| Scheduling | `APScheduler` |
| Validation | `pydantic` |
| Testing | `pytest` |
| Agent framework | ADK |

---

# 18. Summary

`finance_agent` is an ADK-based financial intelligence agent with modular architecture and reusable Python components.

The system is designed around:

- Agent-oriented workflows
- Reusable libraries
- Extensible provider architecture
- Local financial data caching
- Natural language financial querying

The architecture emphasizes:

- Separation of concerns
- Maintainability
- Extensibility
- Future AI integration
- Easy migration beyond SQLite and Yahoo Finance
