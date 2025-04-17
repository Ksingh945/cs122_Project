from flask import Blueprint, render_template, request
import yfinance as yf
import pandas as pd
import os

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/visualize', methods=['POST'])
def visualize():
    ticker = request.form['ticker']
    start_date = request.form['start']
    end_date = request.form['end']
    
    # Fetch and save data
    data = yf.download(ticker, start=start_date, end=end_date)
    filepath = f"data/{ticker}_{start_date}_{end_date}.csv"
    os.makedirs("data", exist_ok=True)
    data.to_csv(filepath)

    # Basic stats
    data['Daily Return'] = data['Close'].pct_change()
    data['Moving Average'] = data['Close'].rolling(window=20).mean()

    
    # Save cleaned data (if needed)
    data.to_csv(filepath)

    return render_template('visualize.html', tables=[data.tail().to_html(classes='data')], ticker=ticker)



#Test commit from nishit-14
