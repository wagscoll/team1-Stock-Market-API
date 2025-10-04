import pytest
from aioresponses import aioresponses
from api.stock_fetcher import get_all_stocks, fetch_and_parse_stock, BASE_URL
import os


@pytest.mark.asyncio
async def test_get_all_stocks_success(monkeypatch):
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "demo")

    with aioresponses() as mock:
        mock.get(BASE_URL.format(symbol="QQQ", apikey="demo"), payload={"Global Quote": {"05. price": "370.00"}})
        mock.get(BASE_URL.format(symbol="NDAQ", apikey="demo"), payload={"Global Quote": {"05. price": "60.00"}})
        mock.get(BASE_URL.format(symbol="GOOGL", apikey="demo"), payload={"Global Quote": {"05. price": "2800.00"}})

        result = await get_all_stocks()

        assert "QQQ" in result and result["QQQ"]["Global Quote"]["05. price"] == "370.00"
        assert "NDAQ" in result and result["NDAQ"]["Global Quote"]["05. price"] == "60.00"
        assert "GOOGL" in result and result["GOOGL"]["Global Quote"]["05. price"] == "2800.00"

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "symbol, mocked_response, expected_result",
    [
        # Successful stock lookup
        (
            "AAPL",
            {"Global Quote": {"05. price": "150.00"}},
            {"05. price": "150.00"},
        ),

        # Invalid ticker
        (
            "XXXX",
            {},
            {"error": "Invalid ticker or empty response for XXXX"},
        ),

        # Rate limit
        (
            "GOOG",
            {"Note": "You have exceeded the rate limit."},
            {"error": "Rate limit reached"},
        )
    ]
)
async def test_fetch_and_parse_stock(symbol, mocked_response, expected_result, monkeypatch):
    #  Force the API key to match what the mock expects
    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "demo")

    url = BASE_URL.format(symbol=symbol, apikey="demo")

    with aioresponses() as mock:
        mock.get(url, payload=mocked_response)

        result = await fetch_and_parse_stock(symbol)

        assert result == expected_result
