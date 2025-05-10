import yfinance as yf
import streamlit as st
import pandas as pd

s = "2008-06-26"
e = "2025-04-30"
t = "AAPL"

stock = yf.Ticker(t)
data = yf.download(t, start=s, end=e)

def calculate_with_reinvesting(start_date, end_date, stock):
    # stock.dividends
    # print(stock.dividends)
    # print()

    start_series = stock.dividends.index[stock.dividends.index >= start_date][0]
    end_series = stock.dividends.index[stock.dividends.index <= end_date][-1]
    print(start_series)
    # print(end_series)
    arr = stock.dividends.loc[start_series:end_series]

    price_data = stock.history(start=start_date, end=end_date)['Close']

    start_amount = 10000
    starting_share = start_amount / price_data[0]
    print("Starting with $10000, I have", starting_share, "shares")
    # print(price_data)
    # for date, payout in arr.items:
    # print(date,payout)
    for date, payout in arr.items():
        current_stock_price_at_closing = price_data[date]
        starting_share += (starting_share * payout) / current_stock_price_at_closing
        # print(date,payout)
        # print(price_data[date])
        # print("Current price at closing", current_stock_price_at_closing, 'on date', date)
        # print("I currently have", starting_share, 'shares, which is worth',
        # starting_share * current_stock_price_at_closing)


calculate_with_reinvesting(s, e, stock)


header = st.container()
with header:
    st.title = ("Welcome to Toan Le longrun data")

    st.sidebar.header("Enter your stock symbol:")
    ticker = st.sidebar.text_input("Stock symbol", t)