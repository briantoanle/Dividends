import streamlit as st

def displayApp(ticker):

    st.write("""Starting with $10,0000 of stock:""", ticker)


def main():
    st.title = ("Welcome to Toan Le longrun data")
    st.header("HI there")
    t = "AAPL"
    st.sidebar.header("Enter your stock symbol:")
    ticker = st.sidebar.text_input("Stock symbol", t)
    displayApp(ticker)


main()
