import streamlit as st
import yfinance as yf
import datetime as dt
import pandas as pd
s = "2008-06-26"
e = "2015-04-30"
t = "AAPL"



def calculate_with_reinvesting(start_amount, start_date, end_date, stock):
    # stock.dividends
    # print(stock.dividends)
    # print()

    start_series = stock.dividends.index[stock.dividends.index >= start_date][0]
    end_series = stock.dividends.index[stock.dividends.index <= end_date][-1]
    print(start_series)
    # print(end_series)
    arr = stock.dividends.loc[start_series:end_series]

    price_data = stock.history(start=start_date, end=end_date)['Close']

    starting_share = start_amount / price_data[0]
    print("Starting with $10000, I have", starting_share, "shares")
    # print(price_data)
    # for date, payout in arr.items:
    # print(date,payout)
    d = {}
    d["Date"] = []
    d["Dividends"] = []
    d["Amount"] = []
    for date, payout in arr.items():

        d["Date"].append(date)
        d["Dividends"].append(payout)

        current_stock_price_at_closing = price_data[date]
        starting_share += (starting_share * payout) / current_stock_price_at_closing
        d["Amount"].append(starting_share *current_stock_price_at_closing)
    current_value = starting_share * current_stock_price_at_closing

    return current_value,d


def displayApp(ticker,start_date,end_date,starting_amount):
    st.header("Welcome to Toan Le longrun data")
    st.write(f"""Starting with \${starting_amount} of stock:""", ticker)
    stock = yf.Ticker(ticker)
    #data = yf.download(ticker, start=s, end=e)
    current_value,d = calculate_with_reinvesting(starting_amount, start_date,end_date,stock)
    st.write("I have", current_value,"$")
    #print(d)
    df = pd.DataFrame(d)
    st.line_chart(df, x="Date", y="Amount")

def main():
    st.title = ("")
    t = "AAPL"
    st.sidebar.header("Enter your stock symbol:")
    ticker = st.sidebar.text_input("Stock symbol", t)
    starting_amount = st.sidebar.number_input("Starting amount", value=10000)
    start_date = str(st.sidebar.date_input("Start date", s))
    end_date = str(st.sidebar.date_input("End date", e))
    print(start_date,"***")
    displayApp(ticker,start_date,end_date,starting_amount)


main()
