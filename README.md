# CS 122 Final Project

## Project Title: Python-Based Stock Data Explorer

## Authors: Nishit Oberoi & Kuldeep Singh

## Project Description
Type Here

## Project Outline
1. Design a user-friendly Flask web interface with at least two screens (Home & Visualization).

2. Create functionality for users to input stock ticker and date range.

3. Fetch real-time or historical stock data using an open API (e.g., Yahoo Finance via yfinance).

4. Organize data into structured CSV files locally for reuse and reproducibility.

5. Perform basic analysis (e.g., price changes, moving averages).

6. Generate visualizations such as line plots for stock trends.

7. Ensure good version control with Git and collaboration via GitHub.

### Interface Plan
Type Here

### Data Collection and Storage Plan (written by Nishit Oberoi)
We will use the yfinance Python library to collect stock market data from Yahoo Finance. When a user submits a stock ticker and date range, the application fetches the relevant data and stores it as a CSV file in a local data/ directory. This allows us to reuse data without repeatedly querying the API and keeps a local record for analysis. The data is organized with headers such as Date, Open, High, Low, Close, and Volume.



### Data Analysis and Visualization Plan (written by Kuldeep Singh)
Type Here
