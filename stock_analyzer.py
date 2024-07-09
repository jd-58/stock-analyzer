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
import datetime
from tkinter import *
from tkinter import ttk
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import matplotlib.units as munits


class User:
    """Stores user's selected stock ticker and the date range for the stock."""

    def __init__(self, stock_ticker="AAPL", date_range=30):
        """Creates a User object with their specified stock ticker and date range."""
        self._stock_ticker = stock_ticker
        self._date_range = date_range

    def download_stock_information(self):
        """Downloads stock information from YFinance"""
        stock_ticker = self.get_stock_ticker()
        stock_data = yf.download(tickers=stock_ticker, period="1mo")
        stock_data = stock_data.reset_index(drop=False)
        stock_data.columns = stock_data.columns.str.replace(' ', '_')  # replaces space in a column title with _
        stock_data['Date'] = stock_data['Date'].astype(str)  # Prevents a warning when trying to compare dates
        stock_data["%_Change"] = np.round(stock_data["Adj_Close"].pct_change() * 100, 2)
        new_column_names = {"Date": "date", "Open": "open_price", "High": "high", "Adj_Close": "adj_close",
                            "Volume": "volume", "%_Change": "percent_change"}
        stock_data.rename(columns=new_column_names, inplace=True)
        return stock_data

    def set_stock_ticker(self, new_stock_ticker):
        """Changes the user's stock ticker"""
        self._stock_ticker = new_stock_ticker
        return self._stock_ticker

    def set_date_range(self, new_date_range):
        """Changes the user's date range for their stock"""
        self._date_range = new_date_range
        return self._date_range

    def get_stock_ticker(self):
        """Returns the current selected stock ticker"""
        return self._stock_ticker

    def get_date_range(self):
        """Returns the current date range"""
        return self._date_range


user1 = User("AAPL", 30)


def click():
    """Creates the graph on button click"""
    # NEED TO FIX: separate the axis and graph stuff into separate functions to clean this up
    user_stock = stock_entry.get()
    user1.set_stock_ticker(user_stock)
    user_stock_information = user1.download_stock_information()
    current_user_stock_price = user_stock_information.adj_close[18]
    current_user_stock_price = round(current_user_stock_price, 2)
    current_stock_price_text = "Current stock price: " + str(current_user_stock_price)
    stock_price_label = Label(window, text=current_stock_price_text)
    stock_price_label.pack()
    x_axes = user_stock_information['date']
    y_axes = user_stock_information['adj_close']
    fig = Figure(figsize=(12, 4.8), dpi=100)
    ax = fig.add_subplot()
    ax.plot(x_axes, y_axes, **{'color': 'blue', 'marker': 'o'})
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    locator = mdates.AutoDateLocator(minticks=7, maxticks=8)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.grid(True)
    graph_title = user_stock + " Graph"
    fig.suptitle(graph_title)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw_idle()
    toolbar = NavigationToolbar2Tk(canvas, window, pack_toolbar=False)
    toolbar.update()
    toolbar.pack()


# The main window
window = Tk()
window.title("Stock Analyzer")

# Creates an entry field using Tkinter
stock_entry = Entry(window, width=20, borderwidth=5)
stock_entry.pack()
stock_entry.insert(0, "Enter a stock ticker:")

# Creating a button
get_stock_price_button = Button(window, text="Get current stock price", command=click)
get_stock_price_button.pack()


def _quit():
    window.quit()  # stops mainloop
    window.destroy()  # this is necessary on Windows to prevent Fatal Python Error: PyEval_RestoreThread: NULL state


button = Button(master=window, text="Quit", command=_quit)  # Creates "Quit" button
button.pack(side=BOTTOM)

# Creates the GUI
window.mainloop()

# print("Enter a stock ticker:")
# user_ticker = str(input())
# print(get_stock_information(user_ticker))
# print(create_graph(user_ticker))
