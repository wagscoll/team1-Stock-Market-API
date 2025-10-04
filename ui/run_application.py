import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api_utils import filter_valid_tickers, get_all_stocks
from functions import display_tickers, print_help, welcome, stock_search, locally_validate_ticker
from favorites import save_to_my_stocks, load_my_stocks, remove_from_my_stocks, has_stocks

if __name__ == "__main__":
    stocks = get_all_stocks()
    tickers = filter_valid_tickers(stocks)

    welcome()

    while True:
        command = input("Enter a command: ").strip().lower()
        if command == "help":
            print_help()
        elif command == "search":
            stock_search()        
            

        elif command == "view_favs":
            load_my_stocks()

        elif command == "add_favs":
            do_again=True
            while do_again:
                stock = input("Enter the stock you'd like to add to your favorites: ").strip().upper()
                # Validate the ticker symbol
                if not locally_validate_ticker(stock):
                    print("Invalid ticker. Please enter a valid stock ticker.")
                else:
                    save_to_my_stocks([stock])
                    print(f"{stock} has been added to your favorites.")
                    do_again=False

        elif command == "remove_favs":
            if has_stocks():
               stock_to_remove = input("Enter the stock ticker you'd like to remove from your favorites: ").strip().upper()  
               remove_from_my_stocks(stock_to_remove)
            else:
                print("\nYou have no stocks saved. Please add some first.")          

        elif command == "all":
            display_tickers(tickers)

        elif command == "exit":
            print("Exiting the application...")
            break
        else:
            print("Unknown command. Type 'help' for a list of commands.")

