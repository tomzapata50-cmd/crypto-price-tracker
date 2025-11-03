# 💰 Crypto Price Tracker - Real-Time Terminal Dashboard

A powerful Python terminal application that tracks cryptocurrency prices in real-time with beautiful formatting, historical logging, and extensive customization options.

## ✨ Features

- 🔄 **Real-Time Tracking**: Live cryptocurrency prices from CoinGecko API
- 🎨 **Beautiful Terminal UI**: Colorized output with proper formatting and alignment
- 📊 **Symbol Mapping**: Use common symbols (BTC, ETH, DOGE) or full CoinGecko IDs
- 📈 **Change Tracking**: Shows price changes between polling intervals
- 💾 **CSV Logging**: Historical price data logging with timestamps
- ⚙️ **Configurable**: Customizable coins, refresh intervals, and output options
- 🛡️ **Robust**: Graceful error handling for network issues and API failures
- 🎯 **CLI Interface**: Full command-line argument support for automation

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Internet connection for API access

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tomzapata50-cmd/crypto-price-tracker.git
   cd crypto-price-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the tracker**
   ```bash
   python crypto_price_tracker.py
   ```

## 📖 Usage Examples

### Basic Usage
```bash
# Track default coins (BTC, ETH, DOGE, SOL, LTC) with 30-second intervals
python crypto_price_tracker.py
```

### Custom Coins
```bash
# Track specific cryptocurrencies
python crypto_price_tracker.py --coins BTC,ETH,ADA,DOT

# Use full CoinGecko IDs for precise matching
python crypto_price_tracker.py --coins bitcoin,ethereum,cardano
```

### One-Time Check
```bash
# Get current prices without continuous monitoring
python crypto_price_tracker.py --once
```

### Custom Configuration
```bash
# Custom refresh interval and CSV file
python crypto_price_tracker.py --coins LTC,DOGE,SOL --interval 60 --csv my_prices.csv

# Disable CSV logging and colors
python crypto_price_tracker.py --no-csv --no-color
```

## 💻 Sample Output

```
--------------------------------------------------------------
Crypto           Price (USD)        Change
--------------------------------------------------------------
Bitcoin     $110,694.0000   +2.34%
Ethereum    $3,912.9000    -1.12%
Dogecoin        $0.1866    +5.67%
Solana        $187.5500    +0.89%
Litecoin       $99.5300    -0.45%
--------------------------------------------------------------
Last updated: 2025-11-02 18:59:13
```

## 🔧 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--coins` | Comma-separated list of symbols or IDs | bitcoin,ethereum,dogecoin,solana,litecoin |
| `--interval` | Refresh interval in seconds | 30 |
| `--csv` | CSV file path for logging | crypto_prices.csv |
| `--once` | Run once and exit | False |
| `--no-csv` | Disable CSV logging | False |
| `--no-color` | Disable colored output | False |
| `--timeout` | API request timeout | 10 |

## 📊 Supported Cryptocurrencies

The tracker includes built-in symbol mapping for popular cryptocurrencies:

| Symbol | Cryptocurrency | CoinGecko ID |
|--------|----------------|--------------|
| BTC | Bitcoin | bitcoin |
| ETH | Ethereum | ethereum |
| LTC | Litecoin | litecoin |
| DOGE | Dogecoin | dogecoin |
| SOL | Solana | solana |
| ADA | Cardano | cardano |
| XRP | Ripple | ripple |
| BCH | Bitcoin Cash | bitcoin-cash |
| DOT | Polkadot | polkadot |
| LINK | Chainlink | chainlink |
| BNB | Binance Coin | binancecoin |
| USDT | Tether | tether |
| USDC | USD Coin | usd-coin |
| MATIC | Polygon | matic-network |
| AVAX | Avalanche | avalanche-2 |
| SHIB | Shiba Inu | shiba-inu |

*You can also use any valid CoinGecko ID directly.*

## 📁 Project Structure

```
crypto-price-tracker/
├── crypto_price_tracker.py    # Main application
├── crypto_prices.csv         # Generated price history (CSV)
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── .gitignore               # Git ignore rules
```

## 🛠️ Technical Features

- **API Integration**: CoinGecko API for reliable cryptocurrency data
- **Error Handling**: Comprehensive network and API error management
- **Data Persistence**: CSV logging with append mode for historical analysis
- **Terminal Formatting**: Colorama for cross-platform colored output
- **Type Safety**: Full type hints for better code maintainability
- **CLI Framework**: Argparse for robust command-line interface

## 🔄 Automation Ideas

### Scheduled Monitoring
```bash
# Run every hour using cron (Linux/Mac)
0 * * * * /usr/bin/python3 /path/to/crypto_price_tracker.py --once --csv hourly_prices.csv

# Run every 15 minutes using Windows Task Scheduler
python crypto_price_tracker.py --once --csv regular_monitoring.csv
```

### Data Analysis
The CSV output is perfect for:
- Price trend analysis
- Historical performance tracking
- Integration with data visualization tools
- Building trading algorithms

## 🤝 Contributing

Contributions are welcome! Ideas for enhancement:
- Additional cryptocurrency exchanges
- Price alerts and notifications
- Chart visualization
- Portfolio tracking
- Price prediction models

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This tool is for educational and informational purposes only. Cryptocurrency markets are highly volatile. Always do your own research before making investment decisions.

## 🙏 Acknowledgments

- [CoinGecko](https://www.coingecko.com/) for providing free cryptocurrency data API
- [Colorama](https://pypi.org/project/colorama/) for cross-platform colored terminal output

---
Made with ❤️ for the crypto community