import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

# Function to fetch real-time crypto prices
def fetch_crypto_prices(symbols):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(symbols)}&vs_currencies=usd"
    response = requests.get(url).json()
    return {symbol: response.get(symbol, {}).get("usd", 0) for symbol in symbols}

# Streamlit App
st.title("Cryptocurrency Portfolio Tracker")

# User Input Section
st.sidebar.header("Enter Your Portfolio")
num_coins = st.sidebar.number_input("Number of different cryptocurrencies", min_value=1, max_value=10, step=1)
portfolio = []
crypto_ids = []

for i in range(num_coins):
    crypto_name = st.sidebar.text_input(f"Crypto {i+1} (CoinGecko ID)", key=f"crypto_{i}")
    quantity = st.sidebar.number_input(f"Quantity of {crypto_name}", min_value=0.0, step=0.01, key=f"qty_{i}")
    purchase_price = st.sidebar.number_input(f"Purchase Price of {crypto_name} (per unit in USD)", min_value=0.0, step=0.01, key=f"price_{i}")
    
    if crypto_name:
        portfolio.append({
            "crypto": crypto_name,
            "quantity": quantity,
            "purchase_price": purchase_price
        })
        crypto_ids.append(crypto_name)

# Fetch real-time prices
if portfolio:
    prices = fetch_crypto_prices(crypto_ids)
    portfolio_df = pd.DataFrame(portfolio)
    portfolio_df["Current Price"] = portfolio_df["crypto"].map(prices)
    portfolio_df["Current Value"] = portfolio_df["quantity"] * portfolio_df["Current Price"]
    portfolio_df["Total Cost"] = portfolio_df["quantity"] * portfolio_df["purchase_price"]
    portfolio_df["Profit/Loss"] = portfolio_df["Current Value"] - portfolio_df["Total Cost"]
    portfolio_df["% Change"] = (portfolio_df["Profit/Loss"] / portfolio_df["Total Cost"]) * 100
    
    st.subheader("Portfolio Summary")
    st.dataframe(portfolio_df)
    
    # Pie Chart for allocation
    st.subheader("Portfolio Allocation")
    fig_pie = px.pie(portfolio_df, values='Current Value', names='crypto', title='Portfolio Allocation')
    st.plotly_chart(fig_pie)
    
    # Profit/Loss Chart
    st.subheader("Profit/Loss Breakdown")
    fig_bar = px.bar(portfolio_df, x='crypto', y='Profit/Loss', title='Profit/Loss per Cryptocurrency', color='Profit/Loss')
    st.plotly_chart(fig_bar)
    
    # Total Portfolio Value
    total_value = portfolio_df["Current Value"].sum()
    st.subheader(f"Total Portfolio Value: ${total_value:,.2f}")
