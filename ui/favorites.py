import os
import json

DEFAULT_FILEPATH = os.path.join("user_data", "my_stocks.json")

def save_to_my_stocks(selected_tickers, filepath=None):
    """Saves the selected tickers to the my stocks JSON file."""
    filepath = filepath or DEFAULT_FILEPATH
    dir_path = os.path.dirname(filepath)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    if not os.path.exists(filepath):
        with open(filepath, "w") as file:
            json.dump([], file)

    with open(filepath, "r") as file:
        my_stocks = json.load(file)

    for ticker in selected_tickers:
        if ticker not in my_stocks:
            my_stocks.append(ticker)

    with open(filepath, "w") as file:
        json.dump(my_stocks, file, indent=4)

    print(f"\nThe following tickers have been added to your stocks: {', '.join(selected_tickers)}")


def load_my_stocks(filepath=None):
    """Loads and displays the user's stocks from the JSON file."""
    filepath = filepath or DEFAULT_FILEPATH

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            my_stocks = json.load(file)
        if my_stocks:
            print("\nYour stocks:")
            for ticker in my_stocks:
                print(f"- {ticker}")
        else:
            print("\nYou have no stocks saved.")
    else:
        print("\nYou have no stocks saved.")


def remove_from_my_stocks(ticker, filepath=None):
    """Removes a ticker from the user's stocks in the JSON file."""
    filepath = filepath or DEFAULT_FILEPATH

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            my_stocks = json.load(file)

        if ticker in my_stocks:
            my_stocks.remove(ticker)
            with open(filepath, "w") as file:
                json.dump(my_stocks, file, indent=4)
            print(f"\nThe ticker {ticker} has been removed from your stocks.")
        else:
            print(f"\nThe ticker {ticker} is not in your stocks.")
    else:
        print("\nYou have no stocks saved.")


def has_stocks(filepath=None):
    """Checks if the my_stocks JSON file contains any stocks."""
    filepath = filepath or DEFAULT_FILEPATH

    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            my_stocks = json.load(file)
        return len(my_stocks) > 0
    return False