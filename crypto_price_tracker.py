#!/usr/bin/env python3
"""The Three Amigos Crypto Price Tracker.

A friendly terminal dashboard for live cryptocurrency prices. The tracker can
search CoinGecko's current coin catalog, so users are not limited to a short
hard-coded list of symbols.

Examples:
  python crypto_price_tracker.py
  python crypto_price_tracker.py --interactive
  python crypto_price_tracker.py --search doge
  python crypto_price_tracker.py --coins BTC,ETH,SOL --once
  python crypto_price_tracker.py --coins bitcoin,ethereum --interval 60
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from colorama import Fore, Style, init

init(autoreset=True)

APP_NAME = "THE THREE AMIGOS • CRYPTO PRICE TRACKER"
API_BASE = "https://api.coingecko.com/api/v3"
PRICE_URL = f"{API_BASE}/simple/price"
COIN_LIST_URL = f"{API_BASE}/coins/list"

DEFAULT_COINS = ["bitcoin", "ethereum", "dogecoin", "solana", "litecoin"]
DEFAULT_INTERVAL = 30
DEFAULT_TIMEOUT = 10
DEFAULT_CSV = "crypto_prices.csv"
CATALOG_CACHE = ".coingecko_coin_catalog.json"
CATALOG_CACHE_SECONDS = 24 * 60 * 60
MAX_TRACKED_COINS = 50

# Popular symbols get a dependable result even when several coins share a symbol.
SYMBOL_TO_ID: Dict[str, str] = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "LTC": "litecoin",
    "DOGE": "dogecoin",
    "SOL": "solana",
    "ADA": "cardano",
    "XRP": "ripple",
    "BCH": "bitcoin-cash",
    "DOT": "polkadot",
    "LINK": "chainlink",
    "BNB": "binancecoin",
    "USDT": "tether",
    "USDC": "usd-coin",
    "AVAX": "avalanche-2",
    "SHIB": "shiba-inu",
    "TRX": "tron",
    "UNI": "uniswap",
    "XLM": "stellar",
    "HBAR": "hedera-hashgraph",
    "TON": "the-open-network",
    "SUI": "sui",
    "PEPE": "pepe",
    "NEAR": "near",
    "APT": "aptos",
    "ICP": "internet-computer",
    "ETC": "ethereum-classic",
    "FIL": "filecoin",
    "ATOM": "cosmos",
    "AAVE": "aave",
    "CRO": "crypto-com-chain",
    "ALGO": "algorand",
    "VET": "vechain",
}

CatalogEntry = Dict[str, str]


def print_banner() -> None:
    width = 68
    print(Fore.CYAN + "=" * width)
    print(Style.BRIGHT + APP_NAME.center(width))
    print("Live prices • flexible coin search • CSV history".center(width))
    print(Fore.CYAN + "=" * width)


def _valid_catalog(data: object) -> bool:
    if not isinstance(data, list) or not data:
        return False
    sample = data[0]
    return isinstance(sample, dict) and all(key in sample for key in ("id", "symbol", "name"))


def _read_catalog_cache(path: Path, allow_stale: bool = False) -> Optional[List[CatalogEntry]]:
    try:
        if not path.exists():
            return None
        age = time.time() - path.stat().st_mtime
        if not allow_stale and age > CATALOG_CACHE_SECONDS:
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if _valid_catalog(data) else None
    except (OSError, ValueError, TypeError):
        return None


def fetch_coin_catalog(timeout: int, refresh: bool = False) -> List[CatalogEntry]:
    """Return CoinGecko's active coin catalog, cached locally for one day."""
    cache_path = Path(CATALOG_CACHE)
    if not refresh:
        cached = _read_catalog_cache(cache_path)
        if cached:
            return cached

    try:
        response = requests.get(
            COIN_LIST_URL,
            params={"include_platform": "false"},
            timeout=timeout,
        )
        response.raise_for_status()
        data = response.json()
        if not _valid_catalog(data):
            raise ValueError("CoinGecko returned an unexpected catalog format")

        temp_path = cache_path.with_suffix(".tmp")
        temp_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        os.replace(temp_path, cache_path)
        return data
    except (requests.RequestException, OSError, ValueError) as error:
        stale = _read_catalog_cache(cache_path, allow_stale=True)
        if stale:
            print(Fore.YELLOW + f"Catalog refresh failed; using the saved catalog ({error}).")
            return stale
        raise RuntimeError(f"Unable to load CoinGecko's coin catalog: {error}") from error


def search_catalog(catalog: List[CatalogEntry], query: str, limit: int = 20) -> List[CatalogEntry]:
    """Find and rank catalog matches by id, symbol, or full coin name."""
    needle = query.strip().lower()
    if not needle:
        return []

    preferred_id = SYMBOL_TO_ID.get(needle.upper())

    ranked: List[Tuple[int, str, CatalogEntry]] = []
    for entry in catalog:
        coin_id = str(entry.get("id", "")).lower()
        symbol = str(entry.get("symbol", "")).lower()
        name = str(entry.get("name", "")).lower()

        score: Optional[int] = None
        if coin_id == preferred_id:
            score = -1
        elif coin_id == needle:
            score = 0
        elif symbol == needle:
            score = 1
        elif name == needle:
            score = 2
        elif symbol.startswith(needle):
            score = 3
        elif name.startswith(needle):
            score = 4
        elif needle in symbol:
            score = 5
        elif needle in name:
            score = 6
        elif needle in coin_id:
            score = 7

        if score is not None:
            ranked.append((score, name, entry))

    ranked.sort(key=lambda item: (item[0], item[1], item[2].get("id", "")))
    return [entry for _, _, entry in ranked[: max(1, limit)]]


def print_catalog_matches(matches: List[CatalogEntry]) -> None:
    if not matches:
        print(Fore.YELLOW + "No matching cryptocurrencies found.")
        return

    print()
    print(f"{'#':>3}  {'Name':<28} {'Symbol':<10} CoinGecko ID")
    print("-" * 72)
    for number, entry in enumerate(matches, start=1):
        name = str(entry.get("name", ""))[:28]
        symbol = str(entry.get("symbol", "")).upper()[:10]
        print(f"{number:>3}  {name:<28} {symbol:<10} {entry.get('id', '')}")
    print()


def choose_coins_interactively(
    catalog: List[CatalogEntry],
    max_coins: int = MAX_TRACKED_COINS,
) -> List[str]:
    """Let the user search the full catalog and build a readable watch list."""
    selected: List[str] = []
    print(Fore.CYAN + f"Search more than {len(catalog):,} CoinGecko listings.")
    print("Press Enter on an empty search when your watch list is ready.")

    while True:
        if selected:
            print(Fore.GREEN + "Selected: " + ", ".join(selected))
        query = input("Search by coin name or symbol: ").strip()
        if not query:
            return selected or DEFAULT_COINS.copy()

        matches = search_catalog(catalog, query, limit=15)
        print_catalog_matches(matches)
        if not matches:
            continue

        choice = input("Choose number(s), separated by commas; or Enter to search again: ").strip()
        if not choice:
            continue

        indexes: List[int] = []
        for part in choice.split(","):
            part = part.strip()
            if part.isdigit():
                indexes.append(int(part))

        added = 0
        for index in indexes:
            if 1 <= index <= len(matches):
                coin_id = str(matches[index - 1]["id"])
                if coin_id not in selected:
                    selected.append(coin_id)
                    added += 1
                if len(selected) >= max_coins:
                    print(Fore.YELLOW + f"Watch list limit reached ({max_coins} coins).")
                    return selected

        if added == 0:
            print(Fore.YELLOW + "No valid selection was entered. Try the number shown at left.")


def resolve_input_coins(
    raw: str,
    catalog: Optional[List[CatalogEntry]] = None,
) -> Tuple[List[str], Dict[str, str]]:
    """Resolve comma-separated symbols, names, or CoinGecko IDs."""
    tokens = [token.strip() for token in raw.split(",") if token.strip()]
    resolved: List[str] = []
    mapping: Dict[str, str] = {}
    seen = set()

    catalog_by_id: Dict[str, CatalogEntry] = {}
    catalog_by_name: Dict[str, List[CatalogEntry]] = {}
    catalog_by_symbol: Dict[str, List[CatalogEntry]] = {}
    if catalog:
        for entry in catalog:
            coin_id = str(entry.get("id", "")).lower()
            name = str(entry.get("name", "")).lower()
            symbol = str(entry.get("symbol", "")).lower()
            catalog_by_id[coin_id] = entry
            catalog_by_name.setdefault(name, []).append(entry)
            catalog_by_symbol.setdefault(symbol, []).append(entry)

    for token in tokens:
        upper = token.upper()
        lower = token.lower()
        coin_id = SYMBOL_TO_ID.get(upper)

        if not coin_id and lower in catalog_by_id:
            coin_id = lower
        if not coin_id and len(catalog_by_name.get(lower, [])) == 1:
            coin_id = str(catalog_by_name[lower][0]["id"])
        if not coin_id and len(catalog_by_symbol.get(lower, [])) == 1:
            coin_id = str(catalog_by_symbol[lower][0]["id"])
        if not coin_id:
            coin_id = lower

        if coin_id not in seen:
            resolved.append(coin_id)
            seen.add(coin_id)
        mapping[token] = coin_id

    return resolved[:MAX_TRACKED_COINS], mapping


def fetch_prices(coins: List[str], timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Dict[str, float]]:
    """Fetch a batch of USD prices from CoinGecko."""
    response = requests.get(
        PRICE_URL,
        params={"ids": ",".join(coins), "vs_currencies": "usd"},
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise ValueError("CoinGecko returned an unexpected price format")
    return data


def ensure_csv_header(path: str, coins: List[str]) -> None:
    if not path:
        return
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp"] + [f"{coin}_usd" for coin in coins])


def append_prices_to_csv(
    path: str,
    coins: List[str],
    prices: Dict[str, Optional[float]],
) -> None:
    if not path:
        return
    with open(path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [time.strftime("%Y-%m-%d %H:%M:%S")]
            + [prices.get(coin, "") for coin in coins]
        )


def format_price(price: Optional[float]) -> str:
    if price is None:
        return "N/A"
    if price >= 1_000:
        return f"${price:,.2f}"
    if price >= 1:
        return f"${price:,.4f}"
    if price >= 0.01:
        return f"${price:,.6f}"
    return f"${price:,.8f}"


def format_pct(delta: Optional[float]) -> str:
    if delta is None:
        return "N/A"
    arrow = "▲" if delta > 0 else "▼" if delta < 0 else "•"
    return f"{arrow} {abs(delta) * 100:.2f}%"


def coin_label(coin_id: str, catalog_index: Dict[str, CatalogEntry]) -> str:
    entry = catalog_index.get(coin_id)
    if entry:
        name = str(entry.get("name", coin_id))
        symbol = str(entry.get("symbol", "")).upper()
        return f"{name} ({symbol})" if symbol else name

    reverse_symbols = {value: key for key, value in SYMBOL_TO_ID.items()}
    name = coin_id.replace("-", " ").title()
    symbol = reverse_symbols.get(coin_id)
    return f"{name} ({symbol})" if symbol else name


def print_prices(
    coins: List[str],
    data: Dict[str, Dict[str, float]],
    previous: Dict[str, float],
    catalog_index: Dict[str, CatalogEntry],
) -> Dict[str, Optional[float]]:
    """Print the dashboard and return current prices for the next comparison."""
    print(f"{'Cryptocurrency':<30}{'Price (USD)':>20}{'Since last check':>18}")
    print("-" * 68)
    current_prices: Dict[str, Optional[float]] = {}

    for coin in coins:
        raw_price = data.get(coin, {}).get("usd")
        price = float(raw_price) if isinstance(raw_price, (int, float)) else None
        current_prices[coin] = price

        old_price = previous.get(coin)
        change = None
        if price is not None and old_price not in (None, 0):
            change = (price - old_price) / old_price

        label = coin_label(coin, catalog_index)[:29]
        price_text = f"{format_price(price):>20}"
        change_text = f"{format_pct(change):>18}"

        if price is None:
            price_color = Fore.YELLOW
        else:
            price_color = Fore.WHITE

        if change is None:
            change_color = Fore.YELLOW
        elif change > 0:
            change_color = Fore.GREEN
        elif change < 0:
            change_color = Fore.RED
        else:
            change_color = Fore.CYAN

        print(f"{label:<30}{price_color}{price_text}{change_color}{change_text}")

    print("-" * 68)
    return current_prices


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Track live cryptocurrency prices or search CoinGecko's full catalog."
    )
    parser.add_argument(
        "--coins",
        "-c",
        default=",".join(DEFAULT_COINS),
        help="Comma-separated symbols or CoinGecko IDs (default: BTC, ETH, DOGE, SOL, LTC)",
    )
    parser.add_argument(
        "--interactive",
        "-I",
        action="store_true",
        help="Search CoinGecko's catalog and build a watch list interactively",
    )
    parser.add_argument(
        "--search",
        metavar="TEXT",
        help="Search the complete CoinGecko catalog, print matches, and exit",
    )
    parser.add_argument(
        "--search-limit",
        type=int,
        default=20,
        help="Maximum catalog search results to display (default: 20)",
    )
    parser.add_argument(
        "--refresh-catalog",
        action="store_true",
        help="Download a fresh coin catalog instead of using the one-day cache",
    )
    parser.add_argument("--interval", "-i", type=int, default=DEFAULT_INTERVAL)
    parser.add_argument("--timeout", "-t", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--csv", "-o", default=DEFAULT_CSV)
    parser.add_argument("--no-csv", action="store_true", help="Disable CSV logging")
    parser.add_argument("--once", action="store_true", help="Fetch prices once and exit")
    parser.add_argument("--no-color", action="store_true", help="Disable terminal colors")
    return parser.parse_args(argv)


def disable_colors() -> None:
    global Fore, Style

    class _NoColor:
        RED = GREEN = CYAN = MAGENTA = YELLOW = WHITE = BRIGHT = RESET_ALL = ""

    Fore = _NoColor()
    Style = _NoColor()


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    if args.no_color:
        disable_colors()

    interval = max(1, args.interval)
    timeout = max(1, args.timeout)
    catalog: List[CatalogEntry] = []

    print_banner()

    if args.search or args.interactive:
        try:
            print("Loading the cryptocurrency catalog...")
            catalog = fetch_coin_catalog(timeout, refresh=args.refresh_catalog)
        except RuntimeError as error:
            print(Fore.RED + str(error))
            return 1

    if args.search:
        matches = search_catalog(catalog, args.search, limit=max(1, args.search_limit))
        print_catalog_matches(matches)
        print(f"Found {len(matches)} match(es) shown from {len(catalog):,} available listings.")
        return 0

    try:
        if args.interactive:
            coins = choose_coins_interactively(catalog)
            mapping = {coin: coin for coin in coins}
        else:
            coins, mapping = resolve_input_coins(args.coins)
    except (EOFError, KeyboardInterrupt):
        print("\nSelection cancelled. Goodbye, Tom!")
        return 0

    if not coins:
        print(Fore.RED + "No coins were selected.")
        return 1

    if len(mapping) > MAX_TRACKED_COINS:
        print(Fore.YELLOW + f"Showing the first {MAX_TRACKED_COINS} selected coins.")

    catalog_index = {str(entry["id"]): entry for entry in catalog}
    csv_path = "" if args.no_csv else (args.csv or "")
    if csv_path:
        ensure_csv_header(csv_path, coins)

    print("Tracking: " + ", ".join(coins))
    print("Press Ctrl+C whenever you want to stop.\n")
    previous_prices: Dict[str, float] = {}

    try:
        while True:
            try:
                data = fetch_prices(coins, timeout=timeout)
                current_prices = print_prices(coins, data, previous_prices, catalog_index)

                if csv_path:
                    append_prices_to_csv(csv_path, coins, current_prices)

                print(Fore.CYAN + f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                missing = [coin for coin in coins if current_prices.get(coin) is None]
                if missing:
                    print(Fore.YELLOW + "No price returned for: " + ", ".join(missing))

                if args.once:
                    return 0

                print(Fore.MAGENTA + f"Next update in {interval} seconds...\n")
                previous_prices = {
                    coin: price
                    for coin, price in current_prices.items()
                    if price is not None
                }
                time.sleep(interval)

            except requests.RequestException as error:
                print(Fore.RED + "Network/API error: " + str(error))
                if args.once:
                    return 1
                print(Fore.MAGENTA + f"Retrying in {interval} seconds...")
                time.sleep(interval)
            except (OSError, ValueError) as error:
                print(Fore.RED + "Data/output error: " + str(error))
                return 1

    except KeyboardInterrupt:
        print(Style.BRIGHT + "\nTracker stopped. Goodbye, Tom!")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
