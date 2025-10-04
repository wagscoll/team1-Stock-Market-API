import pytest
from quart import Quart
from quart.testing import QuartClient
from api.server import app 


#  Test 1: Check /stocks returns all stock data
@pytest.mark.asyncio
async def test_get_all_stocks():
    test_client: QuartClient = app.test_client()
    response = await test_client.get("/stocks")
    assert response.status_code == 200
    data = await response.get_json()
    assert "QQQ" in data

#  Test 2: Check /health returns OK
@pytest.mark.asyncio
async def test_health_check():
    test_client = app.test_client()
    response = await test_client.get("/health")
    assert response.status_code == 200
    assert await response.get_json() == {"status": "ok"}

#  Test 3: Mock /stocks/<symbol> to return fake data
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_single_stock_mocked():
    test_client = app.test_client()
    fake_data = {
        "01. symbol": "TEST",
        "05. price": "123.45"
        
    }

    with patch("api.server.fetch_stock_for_symbol", return_value=fake_data):
        response = await test_client.get("/stocks/TEST")
        data = await response.get_json()

        assert "TEST" in data
        assert data["TEST"]["05. price"] == "123.45"
