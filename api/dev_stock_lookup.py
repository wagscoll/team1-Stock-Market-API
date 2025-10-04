import asyncio
from api.stock_fetcher import fetch_and_parse_stock

### This script is a simple command-line interface to fetch stock data using the Alpha Vantage API.
### It allows users to input a stock ticker symbol and fetches the latest stock data.
### This is not directly run within ui/run_application.py, but is a standalone script for testing purposes.
### It is designed to be run in an environment where the API key is set as an environment variable.

async def main():
    ticker = input("Enter the stock ticker symbol: ").upper().strip()
    data = await fetch_and_parse_stock(ticker)

    if "error" in data:
        print(data["error"])
    else:
        print(f"\nStock: {ticker}")
        print("-" * 30)
        for key, value in data.items():
            print(f"{key}: {value}")
        print("\n")

if __name__ == '__main__':
    asyncio.run(main())