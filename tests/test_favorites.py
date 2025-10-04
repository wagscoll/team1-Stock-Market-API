import pytest
import json

from unittest.mock import mock_open, patch, ANY
from ui.favorites import save_to_my_stocks, load_my_stocks, remove_from_my_stocks,has_stocks

@pytest.mark.parametrize(
    "file_exists, mock_stocks, expected_result",
    [
        (True, ["AAPL", "GOOG"], True),   # File exists and contains stocks
        (True, [], False),                # File exists but is empty
        (False, None, False),             # File does not exist
    ]
)

def test_has_stocks_parametrized(file_exists, mock_stocks, expected_result):
    # Set up mock file content
    mock_file = mock_open(read_data=json.dumps(mock_stocks) if mock_stocks is not None else "")

    with patch("ui.favorites.os.path.exists", return_value=file_exists), \
         patch("builtins.open", mock_file), \
         patch("ui.favorites.json.load", return_value=mock_stocks if mock_stocks is not None else []):
        
        result = has_stocks(filepath="dummy_file.json")
        assert result == expected_result



@pytest.mark.parametrize(
    "selected_tickers, existing_file_data, json_load_result, file_exists, expected_output",
    [
        # File exists with some stocks
        (["AAPL", "TSLA"], json.dumps(["GOOG"]), ["GOOG"], True, ["GOOG", "AAPL", "TSLA"]),
        
        # File exists but is empty (treat as no stocks)
        (["AAPL", "TSLA"], "", [], True, ["AAPL", "TSLA"]),
        
    ]
)
def test_save_to_my_stocks(
    selected_tickers, existing_file_data, json_load_result, file_exists, expected_output
):
    # Setup mocked file open
    dummy_file = "dummy_file.json"
    mock_file = mock_open(read_data=existing_file_data if existing_file_data is not None else "")
    
    with patch("ui.favorites.os.path.exists", return_value=file_exists), \
         patch("builtins.open", mock_file) as mocked_file, \
         patch("ui.favorites.json.load", return_value=json_load_result):

        save_to_my_stocks(selected_tickers, filepath=dummy_file)

        # Make sure file was opened correctly

        assert mocked_file.call_count == 2
        mocked_file.assert_any_call("dummy_file.json", "r")
        mocked_file.assert_any_call("dummy_file.json", "w")


        # Get the data written to the file
        handle = mocked_file()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)

        assert json.loads(written_data) == expected_output

@pytest.mark.parametrize(
    "file_exists, mock_stocks, expected_output_lines",
    [
        # Case 1: File exists with tickers
        (True, ["AAPL", "TSLA"], ["Your stocks:", "- AAPL", "- TSLA"]),

        # Case 2: File exists but is empty
        (True, [], ["You have no stocks saved."]),

        # Case 3: File does not exist
        (False, None, ["You have no stocks saved."]),
    ]
)

def test_load_my_stocks(file_exists, mock_stocks, expected_output_lines, capfd):

    # Prepare mock file handler
    
    mock_file = mock_open(read_data=json.dumps(mock_stocks) if mock_stocks is not None else "")

    with patch("ui.favorites.os.path.exists", return_value=file_exists), \
         patch("builtins.open", mock_file), \
         patch("ui.favorites.json.load", return_value=mock_stocks if mock_stocks is not None else []):
        
        load_my_stocks(filepath="dummy_file.json")

        # Capture printed output
        out, _ = capfd.readouterr()# allows us to be sure the right output is printed

        for line in expected_output_lines:
            assert line in out


@pytest.mark.parametrize(
    "file_exists, initial_stocks, ticker_to_remove, expected_output_lines, expected_final_stocks",
    [
        # Ticker is present and should be removed
        (
            True,
            ["AAPL", "GOOG", "TSLA"],"GOOG",["The ticker GOOG has been removed from your stocks."],["AAPL", "TSLA"]
        ),
        # Ticker is not in list
        (
            True,
            ["AAPL", "TSLA"],"GOOG",["The ticker GOOG is not in your stocks."],["AAPL", "TSLA"]
        ),
        # File does not exist
        (
            False, None,"AAPL",["You have no stocks saved."], None   
        )
    ]
)
def test_remove_from_my_stocks(
    file_exists, initial_stocks, ticker_to_remove, expected_output_lines, expected_final_stocks, capfd
):
    mock_data = json.dumps(initial_stocks) if initial_stocks is not None else ""
    mock_file = mock_open(read_data=mock_data)

    if not file_exists:
        mock_file().read.return_value = ""

    with patch("ui.favorites.os.path.exists", return_value=file_exists), \
         patch("builtins.open", mock_file) as mocked_file, \
         patch("ui.favorites.json.load", return_value=initial_stocks if initial_stocks else []), \
         patch("ui.favorites.json.dump") as mock_json_dump:

        remove_from_my_stocks(ticker_to_remove, filepath="dummy_file.json")
        out, _ = capfd.readouterr()

        for line in expected_output_lines:
            assert line in out

        if expected_output_lines[0].startswith("The ticker") and "has been removed" in expected_output_lines[0]:
            mock_json_dump.assert_called_once_with(expected_final_stocks, ANY, indent=4)
        else:
            mock_json_dump.assert_not_called()
