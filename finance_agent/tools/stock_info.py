import os
import csv
import functools
from pathlib import Path


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
