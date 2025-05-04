from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
import uuid
import os
import datetime
import glob
from dotenv import load_dotenv

from app.new_features.recent import get_recents, add_recent
from app.new_features.volume import generate_volume_chart
from app.new_features.bollinger import generate_bollinger_chart

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
        "1. open":   "Open",
        "2. high":   "High",
        "3. low":    "Low",
        "4. close":  "Close",
        "5. volume": "Volume"
    })
    df.index = pd.to_datetime(df.index)
    df = df.sort_index().astype(float)
    df.index.name = 'Date'
    return df


@main.route('/')
def home():
    recents = get_recents()
    return render_template('home.html', recents=recents)


@main.route('/visualize', methods=['GET', 'POST'])
def visualize():
    try:
        ticker    = request.values.get('ticker', '').upper()
        start_raw = request.values.get('start', '')
        end_raw   = request.values.get('end', '')
        ma_window = int(request.values.get('ma_window', 20))

        if not (ticker and start_raw and end_raw):
            flash("Please provide ticker, start date, and end date.", "warning")
            return redirect(url_for('main.home'))

        start = pd.to_datetime(start_raw)
        end   = pd.to_datetime(end_raw)

        os.makedirs("data", exist_ok=True)
        filepath = f"data/{ticker}_{start.date()}_{end.date()}.csv.gz"

        if os.path.exists(filepath):
            try:
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
                if (datetime.datetime.now() - mtime).days > 1:
                    data = fetch_stock_data_alpha_vantage(ticker)
                    if not data.empty:
                        data.to_csv(filepath, compression='gzip')
                else:
                    data = pd.read_csv(filepath, index_col='Date',
                                       parse_dates=True, compression='gzip')
            except Exception:
                flash("Local cache corrupted—delete the file and try again.", "warning")
                return redirect(url_for('main.home'))
        else:
            data = fetch_stock_data_alpha_vantage(ticker)
            if data.empty:
                flash(f"Failed to fetch data for {ticker}.", "warning")
                return redirect(url_for('main.home'))
            data.to_csv(filepath, compression='gzip')

        data = data.loc[start:end]
        if data.empty:
            flash(f"No data for {ticker} between {start.date()} and {end.date()}.", "warning")
            return redirect(url_for('main.home'))

        data['Daily Return']   = data['Close'].pct_change()
        data['Moving Average'] = data['Close'].rolling(window=ma_window).mean()

        static_dir = os.path.join("app", "static")
        os.makedirs(static_dir, exist_ok=True)
        for fpath in glob.glob(os.path.join(static_dir, "*.png")):
            os.remove(fpath)

        fname_price = f"{uuid.uuid4().hex}.png"
        fp_price = os.path.join(static_dir, fname_price)
        plt.figure(figsize=(10, 5))
        plt.plot(data['Close'], label='Close Price')
        plt.plot(data['Moving Average'], label=f'{ma_window}-Day MA')
        if len(data) == 1:
            plt.scatter(data.index, data['Close'], color='blue', label='Single Day')
        plt.title(f"{ticker} Price ({start.date()} → {end.date()})")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(fp_price)
        plt.close()

        fname_hist = f"{uuid.uuid4().hex}.png"
        fp_hist = os.path.join(static_dir, fname_hist)
        plt.figure(figsize=(8, 4))
        data['Daily Return'].dropna().hist(bins=20, edgecolor='black')
        plt.title(f"{ticker} Daily Return Distribution")
        plt.xlabel("Daily Return")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(fp_hist)
        plt.close()

        # Volume bar chart
        vol_fname = generate_volume_chart(data, static_dir)

        # Bollinger Bands chart
        bb_fname  = generate_bollinger_chart(data, static_dir, window=ma_window)

        # Record search
        add_recent({
            'ticker':    ticker,
            'start':     start.date().isoformat(),
            'end':       end.date().isoformat(),
            'ma_window': ma_window
        })

        # Render
        return render_template(
            'visualize.html',
            tables=[data.tail(10).to_html(classes='data table table-sm')],
            ticker=ticker,
            ma_window=ma_window,
            plot_url=url_for('static', filename=fname_price),
            hist_url=url_for('static', filename=fname_hist),
            vol_url=url_for('static', filename=vol_fname),
            bb_url=url_for('static', filename=bb_fname)
        )

    except Exception as e:
        flash(f"Oops, something went wrong: {e}", "danger")
        return redirect(url_for('main.home'))
