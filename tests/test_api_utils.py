import pytest
import json

from unittest.mock import mock_open, patch, ANY
from ui.api_utils import get_sp500_stocks, get_nasdaq_stocks, get_all_stocks, filter_valid_tickers

@pytest.mark.parametrize(
    "input_stocks, expected_valid_tickers",
    [
        (["AAPL", "GOOG", "MSFT"], ["AAPL", "GOOG", "MSFT"]),  # All valid tickers
        (["AAPL", "GOOG", "1234"], ["AAPL", "GOOG", "1234"]),  # Numeric tickers are valid
        (["AAPL", "GOOG", "MSFT!"], ["AAPL", "GOOG"]),         # Invalid ticker with special character
        (["", " ", "AAPL"], ["AAPL"]),                         # Empty and whitespace strings
        ([], []),                                              # Empty list
        (["$AAPL", "GOOG@", "MSFT"], ["MSFT"]),                # Mixed valid and invalid tickers
    ],
)
def test_filter_valid_tickers(input_stocks, expected_valid_tickers):
    result = filter_valid_tickers(input_stocks)
    assert result == expected_valid_tickers

@pytest.mark.parametrize(
    "mocked_html, expected_output",
    [
        (
            """
            <table class="wikitable sortable">
                <tr>
                    <th>Symbol</th>
                    <th>Company</th>
                </tr>
                <tr>
                    <td>AAPL</td>
                    <td>Apple Inc.</td>
                </tr>
                <tr>
                    <td>MSFT</td>
                    <td>Microsoft Corp.</td>
                </tr>
            </table>
            """,
            ["AAPL", "MSFT"]
        ),
        (
            """
            <table class="wikitable sortable">
                <tr>
                    <th>Symbol</th>
                    <th>Company</th>
                </tr>
            </table>
            """,
            []  # No stock symbols in the table
        ),
    ]
)
@patch("ui.api_utils.requests.get")
def test_get_sp500_stocks(mock_get, mocked_html, expected_output):
    # Mock the HTTP response
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = mocked_html

   
    result = get_sp500_stocks()

   
    assert result == expected_output

@pytest.mark.parametrize(
    "mocked_html, expected_output",
    [
        (
            """
            <table class="wikitable sortable">
                <tr>
                    <th>Company</th>
                    <th>Symbol</th>
                </tr>
                <tr>
                    <td>Apple Inc.</td>
                    <td>AAPL</td>
                </tr>
                <tr>
                    <td>Microsoft Corp.</td>
                    <td>MSFT</td>
                </tr>
            </table>
            """,
            ["AAPL", "MSFT"]
        ),
        (
            """
            <table class="wikitable sortable">
                <tr>
                    <th>Company</th>
                    <th>Symbol</th>
                </tr>
            </table>
            """,
            []  # No stock symbols in the table
        ),
    ]
)
@patch("ui.api_utils.requests.get")
def test_get_nasdaq_stocks(mock_get, mocked_html, expected_output):
    # Mock the HTTP response
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = mocked_html

    # Call the function
    result = get_nasdaq_stocks()

    # Assert the result matches the expected output
    assert result == expected_output

@pytest.mark.parametrize(
    "mock_sp500, mock_nasdaq, expected_output",
    [
        (
            ["AAPL", "MSFT", "GOOGL"],  # Mocked S&P 500 stocks
            ["TSLA", "MSFT", "AMZN"],  # Mocked NASDAQ stocks
            ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]  # Combined unique stocks
        ),
        (
            [],  # Empty S&P 500 stocks
            ["META", "NVDA"],  # Mocked NASDAQ stocks
            ["META", "NVDA"]  # Only NASDAQ stocks
        ),
        (
            ["IBM"],  # Mocked S&P 500 stocks
            [],  # Empty NASDAQ stocks
            ["IBM"]  # Only S&P 500 stocks
        ),
        (
            [],  # Empty S&P 500 stocks
            [],  # Empty NASDAQ stocks
            []  # No stocks
        ),
    ]
)
@patch("ui.api_utils.get_sp500_stocks")
@patch("ui.api_utils.get_nasdaq_stocks")
def test_get_all_stocks(mock_get_sp500, mock_get_nasdaq, mock_sp500, mock_nasdaq, expected_output):
    # Mock the return values of get_sp500_stocks and get_nasdaq_stocks
    mock_get_sp500.return_value = mock_sp500
    mock_get_nasdaq.return_value = mock_nasdaq
    # Call the function
    result = get_all_stocks()

    # Assert the result matches the expected output
    assert sorted(result) == sorted(expected_output)

@pytest.mark.parametrize(
    "input_stocks, expected_output",
    [
        (["AAPL", "MSFT", "GOOGL", "1234", "META"], ["AAPL", "MSFT", "GOOGL", "META"]),  # Filters out numeric-only
        (["AAPL", "MSFT", "GOOGL"], ["AAPL", "MSFT", "GOOGL"]),  # All valid tickers
        (["1234", "!@#$", "META"], ["META"]),  # Filters out invalid symbols
        ([], []),  # Empty list
        (["", "   ", "AAPL"], ["AAPL"]),  # Filters out empty and whitespace strings
        (["AAPL", "GOOG@", "MSFT"], ["AAPL", "MSFT"]),  # Filters out tickers with special characters
    ]
)
def test_filter_valid_tickers(input_stocks, expected_output):
    # Call the function
    result = filter_valid_tickers(input_stocks)

    # Assert the result matches the expected output
    assert result == expected_output