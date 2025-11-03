# Copilot Instructions for Crypto Price Tracker

## Project Overview
This is a real-time cryptocurrency price tracking terminal application that fetches data from CoinGecko API and displays it with beautiful formatting, historical logging, and extensive CLI customization.

## Key Files & Architecture
- `crypto_price_tracker.py` - Main application with API integration, CLI handling, and terminal formatting
- `requirements.txt` - Minimal dependencies: requests + colorama
- `crypto_prices.csv` - Generated historical data (gitignored)

## Critical Dependencies
```python
import requests      # API calls to CoinGecko
from colorama import Fore, Style, init  # Cross-platform terminal colors
import argparse     # CLI argument parsing
import csv          # Historical data logging
```

Install command: `pip install requests colorama`

## API Integration Patterns
- **Endpoint**: `https://api.coingecko.com/api/v3/simple/price`
- **Rate limiting**: Respectful delays, error handling for 429 responses
- **Data structure**: Returns `{coin_id: {"usd": price, "usd_24h_change": percent}}`
- **Symbol mapping**: `SYMBOL_TO_ID` dict converts BTC->bitcoin, ETH->ethereum, etc.
- **Error handling**: Network timeouts, API failures, invalid coin IDs

## Code Conventions
- **Type hints**: All functions use proper typing annotations
- **CLI patterns**: Argparse with sensible defaults and help text
- **Error handling**: Try/catch with graceful degradation and user feedback
- **Data logging**: CSV append mode with timestamps for historical tracking
- **Terminal formatting**: Colorama with proper alignment and reset

## Development Workflow
1. **Testing API calls**: Use `--once` flag for single-run testing
2. **Adding coins**: Update `SYMBOL_TO_ID` mapping for new symbols
3. **CLI testing**: Test all argument combinations and edge cases
4. **Output validation**: Check terminal formatting across different platforms

## CLI Argument Patterns
```python
# Standard usage patterns to maintain
parser.add_argument("--coins", default="bitcoin,ethereum,dogecoin,solana,litecoin")
parser.add_argument("--interval", type=int, default=30)
parser.add_argument("--once", action="store_true")
parser.add_argument("--no-csv", action="store_true")
parser.add_argument("--no-color", action="store_true")
```

## Error Handling Patterns
```python
# API request pattern
try:
    response = requests.get(url, timeout=args.timeout)
    response.raise_for_status()
    data = response.json()
except requests.RequestException as e:
    print(f"API Error: {e}")
    return None

# Graceful exit pattern
try:
    while True:
        # main loop
except KeyboardInterrupt:
    print("\nGracefully shutting down...")
```

## Terminal Formatting Standards
- **Price alignment**: Right-aligned with 4 decimal places for consistency
- **Color coding**: Green for positive changes, red for negative
- **Table format**: Fixed-width columns with proper spacing
- **Status messages**: Clear success/error indicators with emojis when appropriate

## Data Persistence
- **CSV format**: timestamp,coin_id,price_usd,change_24h
- **Append mode**: Never overwrite existing historical data
- **File handling**: Check write permissions, create directories if needed

## When Extending
- **New exchanges**: Add new API endpoints following the same error handling pattern
- **Additional data**: Extend the data structure while maintaining CSV compatibility
- **Visualization**: Consider adding simple ASCII charts or integration with plotting libraries
- **Alerts**: Add price threshold notifications using the existing polling structure

## Performance Considerations
- **API limits**: CoinGecko allows generous free tier usage, but implement backoff for 429 errors
- **Memory usage**: Clear old data structures in long-running sessions
- **Network efficiency**: Batch API calls when possible, cache static data like coin lists

## Testing Approach
- **API testing**: Use `--once` with known coin IDs to verify API integration
- **CLI testing**: Test all argument combinations and validate help text
- **Error simulation**: Test network failures, invalid coins, and Ctrl+C handling
- **Output validation**: Check formatting across Windows/Mac/Linux terminals