import os
import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
api_key = os.getenv('ALPHA')


def get_stock_data(symbol):
    base_url = "https://www.alphavantage.co/query"
    function = "TIME_SERIES_DAILY"
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        # API response contains a key named "Time Series (Daily)
        # Captures the value associated with a key from the data dictionary
        time_series_data = data.get("Time Series (Daily)", {})
        # create a Pandas DataFrame from time_series
        # orient='index' (keys of the dictionary will be used as row indices
        df = pd.DataFrame.from_dict(time_series_data, orient='index')
        # Index is converted to Pandas' datetime objects
        df.index = pd.to_datetime(df.index)
        # remove time component
        df.index = df.index.date
        # DataFrame in ascending order, oldest first
        df.sort_index(ascending=True, inplace=True)
        # removes the word close from the column names, exp: takes 1. open, 2. high and splits column names and only uses last word. (open, high)
        df.columns = [col.split()[-1] for col in df.columns]  # Remove "close" from column names

        # Convert the 'close' column to numeric data type
        df['close'] = pd.to_numeric(df['close'])

        # A new column 'date' is added to the DataFrame, which holds the same values as the DataFrame's index. For plotting purposes
        df['date'] = df.index

        # Move the 'date' column to the first position
        df = df[['date'] + list(df.columns[:-1])]
        # processed data frame is returned from the function
        return df
    else:
        print("Error fetching stock data for", symbol)
        return None


def get_news_data():

    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    base_url = "https://www.alphavantage.co/query"
    function = "NEWS_SENTIMENT"
    params = {
        "function": function,
        "apikey": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        test_data = data.get("feed", [])
        return test_data
    else:
        print("no news data")
        return []


if __name__ == "__main__":
    symbol = "AAPL"
    trade_data = get_stock_data(symbol)
    print(trade_data)
    news_data = get_news_data()
    print(news_data)
