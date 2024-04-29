# flaskFinancial
Flask Financial Web Application
Overview
This is a web application built using Python FLask that allows users to submit a stock ticker and view market data and financial news articles
Features
Enter a stock ticker to get stock data, including open price, high price, low price, close price, and volume.
View a candlestick chart fot he stock's price movement over a selected time period.
Fetch and display financial news headlines.

Getting Started
To run the web application locally, follow these steps:
1. Clone the repository to your local machine:
     git clone https://github.com/nateawest/flaskFinancial.git
     cd flaskFinancial
2. pip install -r requirements.txt
3. Set up your API key:

    Create a .env file in the root directory of the project.
    Add your API key to the .env file (e.g., API_KEY=your_api_key_here).
    Make sure to add .env to your .gitignore file to keep it private.

4. Run the Flask application:
   flask run
5. Open your web browser and visit http://127.0.0.1:5000/ to access the application.

Technologies Used

Python 3.5+
Flask micro web framework
Plotly library for creating interactive visualizations
Pandas library for data manipulation
Jinja2 templating engine for HTML templates

