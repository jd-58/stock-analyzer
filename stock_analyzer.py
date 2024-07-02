# Author: Jacob Deaton
# GitHub username: jd-58
# Date: 7/2/2024
# Description: An app that will show various information about any stock the user chooses.
# Suggested features: showing highest % gains from previous day along with basic start and close values.
# Search bar to find stocks, and ability to favorite stocks.

# Importing Libraries
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf


# A function to get the user to select a ticker, and display a simple graph
def get_stock_information(selected_ticker):
    stock_data = yf.download(tickers=selected_ticker, start="2019-09-10", end="2020-10-09")
    return stock_data


def create_graph(stock_for_graph):
    stock_data_for_graph = yf.download(tickers=stock_for_graph, start="2019-09-10", end="2020-10-09")
    plt.figure(figsize=(14, 5))
    sns.set_style("ticks")
    sns.lineplot(data=stock_data_for_graph, x="Date", y="Close", color="firebrick")
    sns.despine()
    plt.title("Stock Price", size='x-large', color='blue')
    return plt.show()


print("Enter a stock ticker:")
user_ticker = str(input())
print(get_stock_information(user_ticker))
print(create_graph(user_ticker))

