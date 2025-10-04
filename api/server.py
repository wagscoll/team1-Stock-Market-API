import aiohttp
import asyncio
from quart import Quart, jsonify
from api.stock_fetcher import get_all_stocks, fetch_stock_for_symbol

app = Quart(__name__)


# Endpoint 1: Get all stocks
@app.route('/stocks', methods=['GET'])
async def get_stocks():
    stocks = await get_all_stocks()
    return jsonify(stocks)


# Endpoint 2: Get one stock (by symbol)
@app.route('/stocks/<symbol>', methods=['GET'])
async def get_single_stock(symbol):
    result = await fetch_stock_for_symbol(symbol)

    if "error" in result:
        return jsonify({"error": result["error"]}), 404

    return jsonify({symbol.upper(): result})


# Endpoint 3: Health check
@app.route('/health', methods=['GET'])
async def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

