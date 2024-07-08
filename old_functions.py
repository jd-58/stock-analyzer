# Author: Jacob Deaton
# GitHub username: jd-58
# Date:
# Description: A file for currently un-used functions that I want to keep around

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


def get_stock_information(selected_ticker):
    """Downloads the chosen stock data from Yahoo Finance - HERE TO MAKE GRAPH FUNCTION WORK"""
    stock_data = yf.download(tickers=selected_ticker, period="1mo")
    stock_data = stock_data.reset_index(drop=False)
    stock_data.columns = stock_data.columns.str.replace(' ', '_')  # replaces space in a column title with an underscore
    stock_data['Date'] = stock_data['Date'].astype(str)  # Prevents a warning when trying to compare dates
    stock_data["%_Change"] = np.round(stock_data["Adj_Close"].pct_change() * 100, 2)
    new_column_names = {"Date": "date", "Open": "open_price", "High": "high", "Adj_Close": "adj_close",
                        "Volume": "volume", "%_Change": "percent_change"}
    stock_data.rename(columns=new_column_names, inplace=True)
    return stock_data


def create_graph(stock_for_graph):
    """Creates a basic line chart - REMOVED B/C I need to use MatPlotLib for the GUI implementation"""
    stock_df = get_stock_information(stock_for_graph)
    graph_title = str(stock_for_graph) + " price"
    fig = px.line(stock_df, x="Date", y="Close", title=graph_title, hover_data=["Date", "Adj_Close", "%_Change"])
    return fig.show()
