---

name: get-stock-info
description: Use this skill when the user wants to retrieve stock information from a stock ID or Yahoo Finance stock symbol.
----------------------------------------------------------------------------------------------------------------------------

# Get Stock Information

Use this skill when the user wants stock information for a Taiwan stock ID (e.g. `2330`) or a Yahoo Finance symbol (e.g. `2330.TW`).

## Usage

```shell
get-stock-info STOCK
```

Examples:

```shell
get-stock-info 2330
```

```shell
get-stock-info 2330.TW
```

## What this skill does

1. Validates the input stock identifier.
2. Uses `YahooFinanceProvider` from `financial-stock-agent`.
3. Retrieves stock information.
4. Displays the result as a markdown table.

## Implementation

Ensure the package is installed:

```shell
pip install financial-stock-agent
```

Execute:

```shell
python .agents/skills/get-stock-info/get_stock_info.py STOCK
```

Example:

```shell
python .agents/skills/get-stock-info/get_stock_info.py 2330
```

Expected output:

| Field                | Value                                              |
| -------------------- | -------------------------------------------------- |
| Company Name         | Taiwan Semiconductor Manufacturing Company Limited |
| Currency             | TWD                                                |
| Current Price        | 2385.0                                             |
| Previous Close Price | 2400.0                                             |
| Market Cap           | 61,848,703,467,520                                 |

## Error Handling

If the stock cannot be retrieved:

```text
Failed to retrieve stock information: <error>
```

## Notes

* Supports both stock IDs and Yahoo Finance symbols.
* Market capitalization is formatted with thousands separators.
* Output is always rendered as a markdown table.
* Do not display the raw `StockInfo` object.
* Exit code 0 indicates success.
* Exit code 1 indicates failure.
