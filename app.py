from flask import Flask, render_template, request
import pandas as pd
from data_retrieval import get_stock_data, get_news_data
import plotly.graph_objects as go

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/', methods=['GET', 'POST'])
def main_dashboard():
    news_data = get_news_data()
    if request.method == 'POST':
        # Get the stock ticker entered by the user from the form
        stock_symbol = request.form['stock_ticker']
        stock_data = get_stock_data(stock_symbol)
        if stock_data is not None and not stock_data.empty:
            # Calculate the stock overview metrics
            stock_overview = calculate_stock_overview(stock_data)
            # Call the function to create the candlestick chart
            candlestick_fig = create_candlestick_chart(stock_data, stock_symbol)
            # Convert the Plotly chart to JSON format
            chart_json = candlestick_fig.to_json()
            # Pass the stock data, stock overview, and chart filename to the template
            return render_template('dashboard.html', stock_overview=stock_overview, stock_data=stock_data,
                                   chart_json=chart_json, stock_symbol=stock_symbol, news_data=news_data)
        else:
            # If data retrieval fails or stock_data is empty, display an error message
            return render_template('dashboard.html', error_msg="Error fetching stock data.")
    # If it's a GET request or no stock ticker entered yet, display the initial page
    return render_template('dashboard.html', stock_data=None, stock_overview=None, news_data=news_data)


def calculate_stock_overview(stock_data):
    # Assuming the date column is the first column (index 0) in the DataFrame
    date_column_index = 0
    stock_data.iloc[:, date_column_index] = pd.to_datetime(stock_data.iloc[:, date_column_index])

    # Calculate stock overview metrics
    current_price = stock_data.iloc[-1]['close']
    previous_close = stock_data.iloc[-2]['close']
    daily_change = current_price - previous_close
    percentage_change = (daily_change / previous_close) * 100

    # Round the values for better display
    current_price = round(current_price, 2)
    daily_change = round(daily_change, 2)
    percentage_change = round(percentage_change, 2)

    # Create a dictionary with the overview metrics
    stock_overview = {
        'date': stock_data.iloc[-1]['date'].strftime('%Y-%m-%d'),
        'current_price': current_price,
        'daily_change': daily_change,
        'percentage_change': percentage_change
    }

    return stock_overview


def create_candlestick_chart(dataframe, symbol):
    fig = go.Figure(data=[go.Candlestick(x=dataframe["date"],
                                        open=dataframe["open"],
                                        high=dataframe["high"],
                                        low=dataframe["low"],
                                        close=dataframe["close"])])

    start_date = dataframe.iloc[0, 0].strftime("%Y-%m-%d")
    end_date = dataframe.iloc[-1, 0].strftime("%Y-%m-%d")
    fig.update_layout(
        title=f"Candlestick Chart - {symbol} ({start_date} to {end_date})",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        width = 1200,  # Set the width to 1200 pixels (4 times the default)
        height = 600  # Set the height to 600 pixels (2 times the default)
    )

    return fig


if __name__ == "__main__":
    app.run()
