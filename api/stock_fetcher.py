import aiohttp
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

### This takes some of the logic from alpha_vantage_api.py, and condenses it to a more testable strutcture.

def get_api_key():
    return os.getenv("ALPHAVANTAGE_API_KEY", "demo")

BASE_URL = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={apikey}"

async def fetch_stock(session, symbol):
    url = BASE_URL.format(symbol=symbol, apikey=get_api_key())
    async with session.get(url) as response:
        if response.status != 200:
            return {"error": f"HTTP {response.status}"}
        data = await response.json()
        if "Global Quote" not in data:
            return {"error": data}
        return data

async def get_all_stocks():
    symbols = ["QQQ", "NDAQ", "GOOGL"]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_stock(session, symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks)
        return dict(zip(symbols, results))

async def fetch_stock_for_symbol(symbol):
    async with aiohttp.ClientSession() as session:
        return await fetch_stock(session, symbol)
    
async def fetch_and_parse_stock(symbol: str):
    async with aiohttp.ClientSession() as session:
        url = BASE_URL.format(symbol=symbol, apikey=get_api_key())
        try:
            async with session.get(url) as response:
                data = await response.json()
                ###print(f"DEBUG: Full API response: {data}")

                if "Note" in data:
                    return {"error": "Rate limit reached"}

                if "Global Quote" not in data or not data["Global Quote"]:
                    return {"error": f"Invalid ticker or empty response for {symbol}"}

                return data["Global Quote"]

        except Exception as e:
            return {"error": f"Exception while fetching data: {e}"}