# CS 122 Final Project

## Project Title: Python-Based Stock Data Explorer

## Authors: Nishit Oberoi & Kuldeep Singh

## Project Description
The Python-Based Stock Data Explorer is a web-based application that allows users to retrieve and explore historical stock market data. Users can input a stock ticker, select a date range, and visualize trends in stock prices over time. The interface is built using Flask and includes interactive widgets like dropdowns and buttons. The app fetches data from a freely available stock data API, organizes it locally, and performs meaningful statistical analysis. It is designed for beginner investors, students, and anyone curious about financial trends.

## Project Outline
1. Design a user-friendly Flask web interface with at least two screens (Home & Visualization).

2. Create functionality for users to input stock ticker and date range.

3. Fetch real-time or historical stock data using an open API (e.g., Yahoo Finance via yfinance).

4. Organize data into structured CSV files locally for reuse and reproducibility.

5. Perform basic analysis (e.g., price changes, moving averages).

6. Generate visualizations such as line plots for stock trends.

7. Ensure good version control with Git and collaboration via GitHub.

### Interface Plan
The interface for this project will be developed in Python using the Flask framework. It will include a home page where users can enter a stock ticker and select a date range. After submission, the app will fetch and process the data, displaying results on a separate page with a summary table and key metrics like daily returns and moving averages. A visualization page will show charts generated with Python, such as time series plots and trend overlays. Flask routing and Jinja2 templating will be used to dynamically render content and embed charts into the web pages.

### Data Collection and Storage Plan (written by Nishit Oberoi)
We will use the yfinance Python library to collect stock market data from Yahoo Finance. When a user submits a stock ticker and date range, the application fetches the relevant data and stores it as a CSV file in a local data/ directory. This allows us to reuse data without repeatedly querying the API and keeps a local record for analysis. The data is organized with headers such as Date, Open, High, Low, Close, and Volume.

### Data Analysis and Visualization Plan (written by Kuldeep Singh)
The analysis and visualization component of this project focuses on identifying trends and insights within the collected stock data. Key metrics such as daily returns, moving averages, and volatility will be calculated using pandas and numpy. The data will be visualized using matplotlib, providing users with clear, interactive charts including line graphs for closing prices, moving average overlays, and histograms of daily returns.
