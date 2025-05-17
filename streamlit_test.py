import dateutil.utils
import streamlit as st
import yfinance as yf
from datetime import date,datetime,timezone

import pandas as pd

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


def displayApp(ticker,start_date,end_date,starting_amount,stock):
    st.write(f"""Starting with ${starting_amount} of stock:""", ticker)
    st.subheader(stock.info['longName'])
    st.badge(stock.info['sectorDisp'])
    st.caption(stock.info['longBusinessSummary'])

    #data = yf.download(ticker, start=s, end=e)
    current_value,d = calculate_with_reinvesting(starting_amount, start_date,end_date,stock)
    st.write("I have", current_value,"$")
    #print(d)
    df = pd.DataFrame(d)
    st.line_chart(df, x="Date", y="Amount")

def get_ipo_date(ticker):
    try:
        info = yf.Ticker(ticker).info
        timestamp = info.get("firstTradeDateMilliseconds", None)
        if timestamp:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).date()
    except:
        pass
    return date(2010, 1, 1)

def main():
    st.title("Dividend Stock Visualizer")

    # Load company list
    companies = pd.read_csv("companies.csv")  # must have 'Symbol' and 'Name'
    companies['display'] = companies['Symbol'] + " - " + companies['Name']

    # Sidebar selection
    st.sidebar.header("Select a stock symbol:")
    selected = st.sidebar.selectbox("Search and select", companies['display'], key='stock_symbol_dropdown')
    ticker = selected.split(" - ")[0]

    # Get IPO date from yfinance
    ipo_date = get_ipo_date(ticker)
    today = date.today()
    stock = yf.Ticker(ticker)
    # Sidebar inputs
    starting_amount = st.sidebar.number_input("Starting amount", value=10000, key='starting_amount_input')
    start_date = str(st.sidebar.date_input("Start date (IPO default)", ipo_date, key='start_date_input',min_value = ipo_date,max_value = "today"))
    end_date = str(st.sidebar.date_input("End date", today, key='end_date_input'))


    displayApp(ticker, start_date, end_date, starting_amount,stock)

if __name__ == "__main__":
    main()
