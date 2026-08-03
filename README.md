# The Three Amigos Crypto Price Tracker

A friendly Python terminal dashboard for checking live cryptocurrency prices,
building custom watch lists, and saving price history to CSV.

The tracker uses CoinGecko's live catalog, so it can search thousands of current
cryptocurrency listings instead of being limited to a short hard-coded list.

## What it does

- Tracks Bitcoin, Ethereum, Dogecoin, Solana, and Litecoin by default.
- Searches the live CoinGecko catalog by coin name or symbol.
- Builds an interactive watch list of up to 50 coins.
- Accepts common symbols such as `BTC`, `ETH`, `SOL`, `DOGE`, and `LTC`.
- Displays live USD prices and movement since the previous check.
- Refreshes automatically every 30 seconds.
- Saves timestamped price history to a CSV file.
- Handles network errors and closes cleanly with `Ctrl+C`.
- Runs on Windows, macOS, and Linux.

## Quick start on Windows

### 1. Download the project

On the repository page, select **Code**, then **Download ZIP**. Extract the ZIP
and open the `crypto-price-tracker` folder in Visual Studio Code.

You can also clone it with Git:

```powershell
git clone https://github.com/tomzapata50-cmd/crypto-price-tracker.git
cd crypto-price-tracker
```

### 2. Install the two dependencies

Open the VS Code terminal in the project folder and enter:

```powershell
py -m pip install -r requirements.txt
```

If the `py` command is unavailable, use:

```powershell
python -m pip install -r requirements.txt
```

### 3. Run the tracker

```powershell
py crypto_price_tracker.py
```

Press `Ctrl+C` to stop it.

## Choose from thousands of cryptocurrencies

The interactive mode is the easiest way to make your own watch list:

```powershell
py crypto_price_tracker.py --interactive
```

Type a name or symbol, such as `doge`, `xrp`, `shiba`, or `cardano`. The tracker
shows matching listings and asks which numbered result you want. Press Enter on
an empty search when the watch list is complete.

The catalog is saved locally for one day to make later searches faster. Refresh
it immediately with:

```powershell
py crypto_price_tracker.py --interactive --refresh-catalog
```

## Useful commands

Run one price check and exit:

```powershell
py crypto_price_tracker.py --once
```

Search the catalog without starting the tracker:

```powershell
py crypto_price_tracker.py --search doge
```

Track selected symbols:

```powershell
py crypto_price_tracker.py --coins BTC,ETH,XRP,SOL,DOGE
```

Refresh every 60 seconds:

```powershell
py crypto_price_tracker.py --interval 60
```

Run without creating a CSV file:

```powershell
py crypto_price_tracker.py --once --no-csv
```

Choose a different CSV filename:

```powershell
py crypto_price_tracker.py --csv my_crypto_history.csv
```

## Command reference

| Option | Purpose | Default |
| --- | --- | --- |
| `--coins`, `-c` | Comma-separated symbols or CoinGecko IDs | BTC, ETH, DOGE, SOL, LTC |
| `--interactive`, `-I` | Search and select coins interactively | Off |
| `--search TEXT` | Search the full catalog and exit | Off |
| `--search-limit NUMBER` | Maximum search results shown | 20 |
| `--refresh-catalog` | Download the latest coin catalog | Off |
| `--interval`, `-i` | Seconds between price checks | 30 |
| `--timeout`, `-t` | Network timeout in seconds | 10 |
| `--csv`, `-o` | CSV history filename | `crypto_prices.csv` |
| `--no-csv` | Disable CSV history | Off |
| `--once` | Check prices once and exit | Off |
| `--no-color` | Disable terminal colors | Off |

See the built-in help at any time:

```powershell
py crypto_price_tracker.py --help
```

## Example output

```text
====================================================================
             THE THREE AMIGOS • CRYPTO PRICE TRACKER
           Live prices • flexible coin search • CSV history
====================================================================
Tracking: bitcoin, ethereum, dogecoin, solana, litecoin

Cryptocurrency                         Price (USD)  Since last check
--------------------------------------------------------------------
Bitcoin (BTC)                          $64,787.00               N/A
Ethereum (ETH)                          $1,873.28               N/A
Dogecoin (DOGE)                         $0.072400               N/A
Solana (SOL)                             $76.2000               N/A
Litecoin (LTC)                           $47.7400               N/A
--------------------------------------------------------------------
```

The movement column begins showing changes after the second price check.

## Project files

```text
crypto-price-tracker/
├── crypto_price_tracker.py  # Main application
├── requirements.txt         # Python dependencies
├── README.md                # Setup and usage guide
└── .gitignore               # Excludes generated and local files
```

Generated CSV files and the downloaded catalog cache are intentionally excluded
from Git so normal use does not clutter the repository.

## Technology

- Python 3.9+
- `requests` for CoinGecko API calls
- `colorama` for cross-platform terminal colors
- `argparse`, `csv`, and `json` from the Python standard library

## Data source and disclaimer

Market data comes from the CoinGecko API. A returned price can be delayed,
missing, or temporarily unavailable. This project is an educational price
tracker, not financial advice or an automated trading system.

---

Built by **Tom, Argon & Echosync — The Three Amigos**.
