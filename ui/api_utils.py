import requests
from bs4 import BeautifulSoup
import pandas as pd

# This code snippet is the same as the one in main.py. The only difference is that this code is in a separate file called api.py. This file is in the api directory. 
# This code snippet is a function that scrapes the S&P 500 and NASDAQ-100 stock tickers from Wikipedia and returns a list of all the stock tickers. 
# The function get_all_stocks() calls the functions get_sp500_stocks() and get_nasdaq_stocks() to get the stock tickers for the S&P 500 and NASDAQ-100, respectively. 
# It then combines the two lists and removes any duplicate entries to get a list of all the stock tickers.
# The use of this file in the code allows us to limit our API calls to Alpha Vantage 

def get_sp500_stocks():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable sortable"})
    rows = table.find_all("tr")
    data = []
    
    for row in rows[1:]:  # Skip header row
        cols = row.find_all("td")
        
        # Ensure the row has the expected number of columns (2)
        if len(cols) > 0:
            data.append(cols[0].text.strip())  # Extract the stock symbol
    
    return data

def get_nasdaq_stocks():
    url = "https://en.wikipedia.org/wiki/NASDAQ-100"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable sortable"})
    rows = table.find_all("tr")
    data = []
    
    for row in rows[1:]:  # Skip header row
        cols = row.find_all("td")
        
        # Ensure the row has the expected number of columns
        if len(cols) > 1:
            data.append(cols[1].text.strip())  # Extract the stock symbol
    
    return data


def get_all_stocks():
    sp500 = get_sp500_stocks()
    nasdaq = get_nasdaq_stocks()
    
    # Remove duplicates and return all stocks
    all_stocks = list(set(sp500 + nasdaq))
    return all_stocks

def filter_valid_tickers(stocks):
    """Filters out valid ticker symbols from the list of stocks."""
    valid_tickers = []
    for stock in stocks:
        # Check if the stock symbol is alphanumeric and not empty
        if stock.isalpha():
            valid_tickers.append(stock)
    return valid_tickers

#stocks = get_all_stocks()
#tickers=filter_valid_tickers(stocks)

#print(tickers)