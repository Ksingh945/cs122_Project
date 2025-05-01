from flask import Blueprint, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import requests
import uuid
import os
import datetime
import glob
from dotenv import load_dotenv

load_dotenv()

main = Blueprint('main', __name__)

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def fetch_stock_data_alpha_vantage(ticker):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": "compact",
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (Daily)" not in data:
        print("API error:", data)
        return pd.DataFrame()

    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df.astype(float)
    df.index.name = 'Date'  # Ensure index is named 'Date'
    return df

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/visualize', methods=['POST'])
def visualize():
    ticker = request.form['ticker'].upper()
    start_date = request.form['start']
    end_date = request.form['end']
    ma_window = int(request.form.get('ma_window', 20))  # default to 20

    os.makedirs("data", exist_ok=True)
    filepath = f"data/{ticker}_{start_date}_{end_date}.csv.gz"

    if os.path.exists(filepath):
        try:
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            if (datetime.datetime.now() - modified_time).days > 1:
                data = fetch_stock_data_alpha_vantage(ticker)
                if not data.empty:
                    data.to_csv(filepath, compression='gzip')
            else:
                data = pd.read_csv(filepath, index_col='Date', parse_dates=True, compression='gzip')
        except Exception:
            return "Local CSV is corrupted. Please delete it and try again."
    else:
        data = fetch_stock_data_alpha_vantage(ticker)
        if data.empty:
            return f"Failed to fetch data for {ticker}. Try again later."
        else:
            data.to_csv(filepath, compression='gzip')

    data = data[(data.index >= start_date) & (data.index <= end_date)]
    if data.empty:
        return f"No data available for {ticker} in this date range."

    data['Daily Return'] = data['Close'].pct_change()
    data['Moving Average'] = data['Close'].rolling(window=ma_window).mean()

    static_dir = os.path.join("app", "static")
    os.makedirs(static_dir, exist_ok=True)

    for f in glob.glob(os.path.join(static_dir, "*.png")):
        os.remove(f)

    filename_price = f"{uuid.uuid4().hex}.png"
    price_filepath = os.path.join(static_dir, filename_price)

    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='Close Price')
    plt.plot(data['Moving Average'], label=f'{ma_window}-Day MA')
    if len(data) == 1:
        plt.scatter(data.index, data['Close'], color='blue', label='Single Day')
    plt.title(f"{ticker} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(price_filepath)
    plt.close()

    filename_hist = f"{uuid.uuid4().hex}.png"
    hist_filepath = os.path.join(static_dir, filename_hist)

    plt.figure(figsize=(8, 4))
    data['Daily Return'].dropna().hist(bins=20, edgecolor='black')
    plt.title(f"{ticker} Daily Return Distribution")
    plt.xlabel("Daily Return")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(hist_filepath)
    plt.close()

    return render_template(
        'visualize.html',
        tables=[data.tail(10).to_html(classes='data')],
        ticker=ticker,
        plot_url=f"static/{filename_price}",
        hist_url=f"static/{filename_hist}",
        ma_window=ma_window
    )