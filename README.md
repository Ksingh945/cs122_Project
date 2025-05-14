# CS 122 Final Project

## Project Title: Python-Based Stock Data Explorer  
**Authors:** Nishit Oberoi & Kuldeep Singh  

---

## Project Description

The Python-Based Stock Data Explorer is a web-based Flask application that allows users to retrieve, analyze, and visualize historical stock market data. Users can input a stock ticker, select a date range, and view insights like price trends, moving averages, volume, and volatility indicators.

The app is designed for beginner investors, students, and anyone curious about financial markets. It emphasizes simplicity, visual clarity, and lightweight performance — with all computations and visualizations handled on the backend using Python libraries like Pandas and Matplotlib.

---

## Project Outline

1. Build a user-friendly Flask web interface with two main pages:  
   - Home (input form + recent searches)  
   - Visualization (charts + data summary)

2. Create functionality for users to input:
   - Stock ticker
   - Date range
   - Moving average (3, 5, 10, 20, or 50-day)

3. Fetch historical stock data from the **Alpha Vantage API**

4. Cache data locally in compressed `.csv.gz` files in a `data/` folder

5. Perform backend analysis including:
   - Daily returns
   - Moving averages
   - Bollinger Bands

6. Generate dynamic charts using Matplotlib:
   - Price chart with MA
   - Daily return histogram
   - Volume bar chart
   - Bollinger Bands visualization

7. Track recent user queries using Flask’s session object (no database required)

8. Ensure version control and team collaboration using GitHub

---

## Interface Plan

The frontend is built using Jinja2 templating and Bootstrap 5. Users land on a clean homepage where they can submit a stock ticker, date range, and select a moving average window. When submitted, the app fetches and analyzes data and renders it in a structured and visually engaging format.

The visualization page presents four different charts, along with a recent stock data table. A session-based history system on the home page allows users to easily revisit past searches during their session.

---

## Data Collection and Storage Plan  
*(written by Nishit Oberoi)*

We use the **Alpha Vantage API** (instead of yfinance) to fetch historical stock data based on user input. The API returns JSON, which is processed into a Pandas DataFrame with standard headers like `Date`, `Open`, `High`, `Low`, `Close`, and `Volume`.

To optimize performance and reduce redundant API calls, we cache each query as a **compressed CSV file (`.csv.gz`)** in a local `data/` directory. The filenames are named dynamically using the ticker and date range, and are reused unless stale (older than one day).

---

## Data Analysis and Visualization Plan  
*(written by Kuldeep Singh)*

After data collection, the app performs several backend computations:

- **Daily Return**: Percentage change in close price
- **Moving Average**: Rolling average over user-selected window
- **Bollinger Bands**: Price envelope based on moving average ± 2 standard deviations

Visualizations are generated using **Matplotlib**, including:

- A price line chart with moving average overlay
- A histogram showing the distribution of daily returns
- A volume bar chart (with green/red bars indicating price direction)
- A Bollinger Bands chart to visualize volatility

All charts are dynamically saved to the `static/` directory and displayed in the interface.

---
