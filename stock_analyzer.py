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
import finplot as fplt
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta
from tkinter import *
from tkinter import ttk

# The main window
window = Tk()
window.title("Stock Analyzer")


# Creates an entry field using Tkinter
stock_entry = Entry(window, width=20, borderwidth=5)
stock_entry.pack()
stock_entry.insert(0, "Enter a stock ticker:")


def click():
    user_stock = stock_entry.get()
    user_stock_information = get_stock_information(user_stock)
    user_stock_price = user_stock_information.Adj_Close[18]
    stock_price_label = Label(window, text=user_stock_price)
    stock_price_label.pack()
    user_stock_graph = create_graph(user_stock)
    stock_graph_label = Label(window, )



def get_stock_information(selected_ticker):
    """Downloads the chosen stock data from Yahoo Finance"""
    stock_data = yf.download(tickers=selected_ticker, period="1mo")
    stock_data = stock_data.reset_index(drop=False)
    stock_data.columns = stock_data.columns.str.replace(' ', '_')  # replaces space in a column title with an underscore
    stock_data['Date'] = stock_data['Date'].astype(str)  # Prevents a warning when trying to compare dates
    stock_data["%_Change"] = np.round(stock_data["Adj_Close"].pct_change() * 100, 2)
    return stock_data


def create_graph(stock_for_graph):
    """Creates a basic line chart"""
    stock_df = get_stock_information(stock_for_graph)
    graph_title = str(stock_for_graph) + " price"
    fig = px.line(stock_df, x="Date", y="Close", title=graph_title, hover_data=["Date", "Adj_Close", "%_Change"])
    return fig.show()


def create_candlestick(stock_for_candlestick):
    """Creates a candlestick chart for the chosen stock."""
    stock_data_for_graph = yf.download(tickers=stock_for_candlestick, start="2019-09-10", end="2020-10-09")
    ax, axv = fplt.create_plot('Apple Inc.', rows=2)
    cplot = fplt.candlestick_ochl(stock_data_for_graph[['Open', 'Close', 'High', 'Low']], ax=ax)
    vplot = fplt.volume_ocv(stock_data_for_graph[['Open', 'Close', 'Volume']], ax=axv)

    cplot.colors.update(
        dict(bull_frame='#000', bull_body='#fff', bull_shadow='#000', bear_frame='#000', bear_body='#000',
             bear_shadow='#000'))
    vplot.colors.update(dict(bull_frame='#000', bull_body='#fff', bear_frame='#000', bear_body='#000'))
    return fplt.show()


# Creating a button
get_stock_price_button = Button(window, text="Get current stock price", command=click)
get_stock_price_button.pack()

# Creates the GUI
window.mainloop()

# print("Enter a stock ticker:")
#  = str(input())
# print(get_stock_information(user_ticker))
# print(create_graph(user_ticker))
