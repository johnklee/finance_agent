import os
import csv
import functools
from pathlib import Path
import twstock

from finance_agent.tools.exceptions import StockNotFoundError


def get_cache_path() -> Path:
    """Get the path to the CSV cache file."""
    cache_path_str = os.environ.get("TW_STOCK_CACHED_CSV_PATH")
    if cache_path_str:
        return Path(cache_path_str)
    return Path(os.getcwd()) / "tw_stock_info_listed.csv"


def csv_cache(func):
    """
    Cache stock ID to Yahoo Finance symbol mappings in a CSV file.

    The CSV file is loaded once when the decorator is applied.
    Newly discovered mappings are immediately persisted back
    to disk.
    """
    cache_path = get_cache_path()

    # Ensure the CSV cache file exists and is initialized
    if not cache_path.exists():
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["stock_id", "stock_symbol"])

    # Load existing cache once when decorator is applied
    cache = {}
    with open(cache_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        _ = next(reader, None)  # Skip header row
        for row in reader:
            if len(row) >= 2:
                cache[str(row[0])] = str(row[1])

    @functools.wraps(func)
    def wrapper(stock_id):
        stock_id_str = str(stock_id)
        if stock_id_str in cache:
            return cache[stock_id_str]

        symbol = func(stock_id)

        # Cache in memory
        cache[stock_id_str] = symbol

        # Append to CSV cache file immediately
        with open(cache_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([stock_id_str, symbol])

        return symbol

    return wrapper


@csv_cache
def stock_id_to_symbol(stock_id: str | int) -> str:
    """
    Convert a Taiwan stock ID into a Yahoo Finance symbol.

    Examples:
        >>> stock_id_to_symbol(2330)
        '2330.TW'

        >>> stock_id_to_symbol('6488')
        '6488.TWO'

    Args:
        stock_id:
            Taiwan stock ID.

    Returns:
        Yahoo Finance stock symbol.

    Raises:
        StockNotFoundError:
            If the stock ID does not exist in twstock.
    """
    stock_id_str = str(stock_id)
    try:
        stock = twstock.codes[stock_id_str]
    except KeyError as e:
        raise StockNotFoundError(
            f"Stock ID {stock_id_str} not found in twstock."
        ) from e

    if stock.market == "上市":
        return f"{stock_id_str}.TW"
    else:
        return f"{stock_id_str}.TWO"
