import csv
import dataclasses
import functools
from io import StringIO
import os
from pathlib import Path
import re
from typing import Callable, ParamSpec, TypeVar
import twstock

from datetime import timedelta
import pandas as pd
import requests

from finance_agent.tools.exceptions import StockNotFoundError

P = ParamSpec("P")
T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class SymbolInfo:
  """Information about a stock symbol and its industry.

  Attributes:
    symbol: Yahoo Finance symbol (e.g. '2330.TW').
    industrial_group: Industrial group name (e.g. '半導體業').
  """

  symbol: str
  industrial_group: str


def cache(
  *,
  life_time: timedelta,
  cache_file: str | Path,
  loader: Callable[[pd.DataFrame], T],
  dumper: Callable[[T], pd.DataFrame],
):
  """Cache the result of a function in a CSV file with an expiration lifetime.

  Args:
    life_time: Time duration after which the cached CSV is considered expired.
    cache_file: Path to the CSV cache file.
    loader: Callable converting a pandas DataFrame into target type T.
    dumper: Callable converting target type T into a pandas DataFrame.
  """
  cache_path = Path(cache_file)

  def decorator(func: Callable[P, T]) -> Callable[P, T]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
      force_refresh = kwargs.pop("force_refresh", False)

      # Return cached data when the cache is still valid
      if not force_refresh and cache_path.exists():
        modified_at = cache_path.stat().st_mtime
        age = pd.Timestamp.now() - pd.Timestamp.fromtimestamp(modified_at)

        if age < life_time:
          df = pd.read_csv(cache_path)
          return loader(df)

      # Fetch fresh data and save to cache CSV
      result = func(*args, **kwargs)

      cache_path.parent.mkdir(parents=True, exist_ok=True)
      dumper(result).to_csv(cache_path, index=False)

      return result

    return wrapper

  return decorator


TWSE_URL = "https://isin.twse.com.tw/isin/e_C_public.jsp?strMode=2"


def _load_symbol_info(df: pd.DataFrame) -> list[SymbolInfo]:
  """Load list of SymbolInfo dataclasses from a DataFrame."""
  return [
    SymbolInfo(
      symbol=str(row["symbol"]),
      industrial_group=str(row["industrial_group"]),
    )
    for _, row in df.iterrows()
  ]


def _dump_symbol_info(symbols: list[SymbolInfo]) -> pd.DataFrame:
  """Convert list of SymbolInfo dataclasses to a DataFrame."""
  return pd.DataFrame([dataclasses.asdict(symbol) for symbol in symbols])


@cache(
  life_time=timedelta(days=10),
  cache_file="cache/twse_stock_list.csv",
  loader=_load_symbol_info,
  dumper=_dump_symbol_info,
)
def get_twse_symbols() -> list[SymbolInfo]:
  """Crawl all TWSE-listed stock symbols from TWSE ISIN directory.

  Returns:
    List of SymbolInfo objects representing TWSE-listed equities.
  """
  response = requests.get(
    TWSE_URL,
    timeout=30,
    headers={"User-Agent": "Mozilla/5.0"},
  )
  response.raise_for_status()

  # TWSE uses Big5 encoding
  html = response.content.decode("big5")

  dfs = pd.read_html(StringIO(html))
  if not dfs:
    return []

  df = dfs[0]
  results: list[SymbolInfo] = []

  for _, row in df.iterrows():
    security = str(row.iloc[0]).strip()

    match = re.match(r"^(\d{4})\b", security)
    if not match:
      continue

    # Column index 4 corresponds to Industrial Group in TWSE table
    industrial_group = str(row.iloc[4]).strip() if len(row) > 4 else ""

    results.append(
      SymbolInfo(
        symbol=f"{match.group(1)}.TW",
        industrial_group=industrial_group,
      )
    )

  return results


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
  cache_dict = {}
  with open(cache_path, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    _ = next(reader, None)  # Skip header row
    for row in reader:
      if len(row) >= 2:
        cache_dict[str(row[0])] = str(row[1])

  @functools.wraps(func)
  def wrapper(stock_id):
    stock_id_str = str(stock_id)
    if stock_id_str in cache_dict:
      return cache_dict[stock_id_str]

    symbol = func(stock_id)

    # Cache in memory
    cache_dict[stock_id_str] = symbol

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
    raise StockNotFoundError(f"Stock ID {stock_id_str} not found in twstock.") from e

  if stock.market == "上市":
    return f"{stock_id_str}.TW"
  else:
    return f"{stock_id_str}.TWO"
