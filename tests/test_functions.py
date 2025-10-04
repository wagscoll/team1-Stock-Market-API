import pytest

from unittest.mock import patch
from ui.functions import print_help, welcome, stock_search, locally_validate_ticker, display_tickers

@pytest.mark.parametrize(
    "ticker, expected_result, expected_message",
    [
        ("785T", False, "Ticker symbol can only contain uppercase letters (no numbers or special characters)."),   #invalid ticker
        ("appl", True, None),    #valid ticker (case insensitive)
        ("APPL", True, None),  #valid ticker (case insensitive)
        ("", False, "Ticker symbol cannot be empty."),  #Empty ticker
        ("TOOLONG", False, "Ticker symbol cannot be longer than 5 characters."),
    ]
)
def test_locally_validate_ticker(capsys, ticker, expected_result, expected_message):
    #Call the function
    result = locally_validate_ticker(ticker)
    #Assert the result matches the expected result
    assert result == expected_result
    #If an error message is expected, capture the output and check it
    if expected_message:
        captured = capsys.readouterr()
        assert expected_message in captured.out

def test_print_help(capsys):
    #Test that print_help outputs the correct help message
    print_help()
    captured = capsys.readouterr()
    assert "Commands:" in captured.out
    assert "all - Display all available stocks" in captured.out

def test_welcome(capsys):
    #Test that welcome outputs the correct welcome message
    welcome()
    captured = capsys.readouterr()
    assert "Welcome to the stock information app!" in captured.out.strip()

@pytest.mark.parametrize(
    "user_input, mocked_response, expected_keywords",
    [
        (
            "AAPL",
            {"01. symbol": "AAPL", "05. price": "150.00"},
            ["You've selected the stock search option.", "Stock: AAPL", "01. symbol: AAPL"],
        ),
        (
            "META",
            {"01. symbol": "META", "05. price": "200.00"},
            ["You've selected the stock search option.", "Stock: META", "01. symbol: META"],
        ),
        (
            "FAKE",
            False,
            ["Stock information not found for FAKE. Please try again."],
        ),
        (
            "",
            None,
            ["Invalid ticker. Please enter a valid stock ticker."],
        )
    ],
)

@patch("ui.functions.get_stock_data")
@patch("builtins.input")
@patch("builtins.print")
def test_stock_search( mock_print, mock_input, mock_get_stock_data, user_input, mocked_response, expected_keywords):
    #Mock user input
    mock_input.side_effect = [user_input, "AAPL"]
    #Mock the API response
    mock_get_stock_data.return_value = mocked_response
    #Call the function
    stock_search()
    #Capture the printed output
    printed_output = "\n".join(call.args[0] for call in mock_print.call_args_list)
    #Assert that all expected keywords are in the printed output
    for keyword in expected_keywords:
        assert keyword in printed_output

@pytest.mark.parametrize(
    "tickers, expected_output",
    [
        (
            ["AAPL", "GOOGL", "MSFT", "TSLA", "META", "NVDA", "AMZN", "IBM"],
            "\nAvailable Ticker Symbols:\n" + 
            " 1. AAPL       2. GOOGL      3. MSFT       4. TSLA       5. META       6. NVDA       7. AMZN      \n" +
            " 8. IBM       \n"
        ),
        (
            ["AAPL", "IBM", "META"],
            "\nAvailable Ticker Symbols:\n" +
            " 1. AAPL       2. IBM        3. META      \n"
        ),
        (
            [],
            "\nAvailable Ticker Symbols:\n\n"
        )
    ]
)
def test_display_tickers(capsys, tickers, expected_output):
    # Call the function with test data
    display_tickers(tickers)
    
    # Capture the printed output
    captured = capsys.readouterr()
    
    # Assert the output matches the expected format
    assert captured.out == expected_output