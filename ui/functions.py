import asyncio
from api.stock_fetcher import fetch_and_parse_stock as get_stock_data

#Functions for displaying information to the user, handeling command calls and other functions not related to favorites
#These functions are used in run_application.py.

def display_tickers(tickers):
    """Displays the list of ticker symbols to the user in rows of 7 with uniform spacing."""
    print("\nAvailable Ticker Symbols:")
    for i, ticker in enumerate(tickers, start=1):
        print(f"{str(i).rjust(2)}. {ticker.ljust(8)}", end="  ")
        if i % 7 == 0:
            print()
    print()

def print_help():
    """Displays a list of available commands to the user."""
    print("Commands:\n")
    print("all - Display all available stocks")
    print("add_favs <stock> - Add a stock to your favorites")
    print("view_favs - Display your saved stocks")
    print("remove_favs <stock> - Remove a stock from your favorites")
    print("search - Search for a particular stock")
    print("exit - Exit the application")
    print("help - Display this help message\n\n")

def welcome():
    """Displays a welcome message to the user."""
    print("\n" * 100)
    print("Welcome to the stock information app!")
    print("\nType 'help' for a list of commands.\n\n")

def stock_search():
    """Handles the stock search functionality."""
    print("\n" * 100)
    print("You've selected the stock search option.\n")
    no_ticker=True
    while no_ticker:
        symbol = input("Enter the stock ticker: ").strip().upper()
        # Validate the ticker symbol
        if not locally_validate_ticker(symbol):
            print("Invalid ticker. Please enter a valid stock ticker.")
        else:
            no_ticker=False
        
    #print(f"DEBUG: Looking up stock: {symbol}")

    data = asyncio.run(get_stock_data(symbol))
    #print("DEBUG: Raw data returned from API:")
    #print(data)

    if data:
        print(f"\nStock: {symbol}")
        print("-" * 30)
        for key, value in data.items():
            print(f"{key}: {value}")
        print("-" * 30)
        print(f"\nprices shown are in US dollars")
        print("\n")
    else:
        print(f"Stock information not found for {symbol}. Please try again.")

def locally_validate_ticker(ticker):
    """Validates the ticker symbol locally. Operates under the assumption that the ticker symbol must be a valid US stock ticker.
    With no numbers or special characters, and is no longer than 5 characters. 
    Potential improvement would be verifying that it is a ticker symbol that is actually in use. 
    Returns True if valid, False otherwise.
    """
    if not ticker:
        print("Ticker symbol cannot be empty.")
        return False

    if len(ticker) > 5:
        print("Ticker symbol cannot be longer than 5 characters.")
        return False

    if not ticker.isalpha():
        print("Ticker symbol can only contain uppercase letters (no numbers or special characters).")
        return False
    
    #Potential future improvement: call alphavantage API to verify that the ticker symbol is actually in use.

    return True
    
