# Author: Jacob Deaton
# GitHub username: jd-58
# Date: 7/2/2024
# Description: An app that will show various information about any stock the user chooses.
# Suggested features: showing highest % gains from previous day along with basic start and close values.
# Search bar to find stocks, and ability to favorite stocks.

# Importing Libraries
import numpy as np
import yfinance as yf
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.dates import WeekdayLocator, DayLocator, MonthLocator, YearLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import matplotlib.ticker as ticker


# TO-DO: Add a dropdown menu to pick date ranges for the graph,
# add section for volume or % change, pick from days listed, fix date format at button of graph

class User:
    """Stores user's selected stock ticker and the date range for the stock."""

    def __init__(self, stock_ticker="AAPL", date_range="1mo", stock1_price=0, graph_canvas_1=None):
        """Creates a User object with their specified stock ticker and date range."""
        self._stock_ticker = stock_ticker
        self._date_range = date_range
        self._stock1_price = stock1_price
        self._graph_canvas_1 = graph_canvas_1

    def download_stock_information(self):
        """Downloads stock information from YFinance
        Returns:
        pandas.DataFrame: A dataframe containing the processed stock data with columns for date, open price, high,
        adjusted close, volume, and percentage change.
        """
        stock_ticker = self.get_stock_ticker()
        stock_data = yf.download(tickers=stock_ticker, period=user1._date_range)
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

    def set_stock1_price(self, new_stock1_price):
        """Changes the stock price for stock 1"""
        self._stock1_price = new_stock1_price
        return self._stock1_price

    def set_graph_canvas_1(self, new_graph1):
        """Sets the graph for stock 1"""
        self._graph_canvas_1 = new_graph1
        return self._graph_canvas_1

    def get_stock_ticker(self):
        """Returns the current selected stock ticker"""
        return self._stock_ticker

    def get_date_range(self):
        """Returns the current date range"""
        return self._date_range

    def get_stock1_price(self):
        """Returns the current price for stock 1"""
        return self._stock1_price

    def get_graph_canvas_1(self):
        """Returns the current graph for stock 1"""
        return self._graph_canvas_1


user1 = User("AAPL", "1mo")


"""def clear_canvas():
    # Clears the current graph canvas.
    existing_canvas = user1.get_graph_canvas_1()
    existing_canvas.delete('all')"""


def clear_canvas():
    """Clears the current graph canvas."""
    existing_canvas = user1.get_graph_canvas_1()
    for item in existing_canvas.get_tk_widget().find_all():
        existing_canvas.get_tk_widget().delete(item)


def click():
    """Creates the graph on button click"""
    retrieve_date_range()
    user_stock = stock_entry.get()
    if str(user_stock) == "":
        messagebox.showerror("Error", "Please enter a stock.")
        return
    if check_stock_existence(user_stock) == 1:  # Check if the entered stock ticker exists.
        # If not (check_stock_existence returns 1), exit the function early.
        return
    user1.set_stock_ticker(user_stock)
    user_stock_information = user1.download_stock_information()
    current_date_index = len(user_stock_information) - 1
    current_user_stock_price = user_stock_information.adj_close[current_date_index]
    current_user_stock_price = round(current_user_stock_price, 2)
    user1.set_stock1_price(current_user_stock_price)
    update_stock_price_label()
    if user1.get_graph_canvas_1() is not None:
        clear_canvas()
        create_stock_graph(user_stock)
    else:
        create_stock_graph(user_stock)
    return


def create_stock_graph(stock_ticker):
    """Creates a Matplotlib line graph for the selected user stock."""
    user1.set_stock_ticker(stock_ticker)
    user_stock_information = user1.download_stock_information()
    x_axes = user_stock_information['date']
    y_axes = user_stock_information['adj_close']
    y_min = min(y_axes)
    y_max = max(y_axes)
    y_min -= 3
    y_max += 3

    fig = Figure(figsize=(12, 4.8), dpi=100)
    ax = fig.add_subplot()
    ax.plot(x_axes, y_axes, **{'color': 'blue'})
    ax.set_xlabel("Date")
    ax.set_ylabel("Adj. Close (USD)")

    if user1.get_date_range() == "5d":
        # Set major ticks to every Monday and minor ticks to every day. Prevents error
        ax.xaxis.set_major_locator(WeekdayLocator(byweekday=MO))
        ax.xaxis.set_minor_locator(DayLocator())
        ax.grid(True, linestyle=':')
    elif user1.get_date_range() == "1mo":
        ax.xaxis.set_major_locator(WeekdayLocator(byweekday=MO))
        ax.xaxis.set_minor_locator(DayLocator())
        ax.grid(True, linestyle=':')
    elif user1.get_date_range() == "1y":
        ax.xaxis.set_major_locator(DayLocator(1, 1))
        ax.xaxis.set_minor_locator(mdates.DayLocator(interval=7))
        ax.grid(True, linestyle=':')
    elif user1.get_date_range() == "2y" or "5y":
        ax.xaxis.set_major_locator(YearLocator())
        ax.xaxis.set_minor_locator(MonthLocator())
        ax.grid(True, linestyle=':')
    else:
        ax.xaxis.set_major_locator(MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        ax.xaxis.set_minor_locator(mdates.DayLocator())
        ax.grid(True, linestyle=':')

    starting_price = float(user_stock_information.adj_close[0])
    # Set threshold for where green dots (above starting price) and red dots (below starting price) appear
    above_threshold = y_axes > starting_price
    ax.scatter(x_axes[above_threshold], y_axes[above_threshold], color='green')
    below_threshold = y_axes < starting_price
    ax.scatter(x_axes[below_threshold], y_axes[below_threshold], color='red')

    # Draws a horizontal line at the starting price
    ax.axhline(y=starting_price, color='r', linestyle='-')

    ax.set_ylim(y_min, y_max)
    graph_title = str(stock_ticker) + " Graph"
    fig.suptitle(graph_title)

    if user1.get_graph_canvas_1() is None:
        # Creating canvas and embedding graph to Tkinter. Adds the toolbar to the graph.
        canvas = FigureCanvasTkAgg(fig, master=stock_graph_frame)
        canvas.get_tk_widget().grid(row=0, column=0)
        canvas.draw_idle()
        toolbar = NavigationToolbar2Tk(canvas, frame, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(row=3, column=0)
        user1.set_graph_canvas_1(canvas)
        window.update_idletasks()
    else:
        # Creating canvas and embedding graph to Tkinter. Does not add a toolbar to the graph.
        canvas = FigureCanvasTkAgg(fig, master=stock_graph_frame)
        canvas.get_tk_widget().grid(row=0, column=0)
        canvas.draw_idle()
        toolbar_list = frame.grid_slaves(3, 0)
        old_toolbar = toolbar_list[0]
        old_toolbar.destroy()
        new_toolbar = NavigationToolbar2Tk(canvas, frame, pack_toolbar=False)
        new_toolbar.update()
        new_toolbar.grid(row=3, column=0)
        user1.set_graph_canvas_1(canvas)
        window.update_idletasks()


def update_stock_price_label():
    """Updates the stock price label to the current user1 stock price."""
    stock_price_value_text.set(str(user1.get_stock1_price()))


def check_stock_existence(stock_ticker):
    """Checks if a stock exists in Yfinance, and creates an error window if it doesn't.
    RETURNS: 1 if the stock is not found. """
    info = yf.Ticker(stock_ticker).history(
        period='1mo'
    )
    if len(info) < 1:
        messagebox.showerror("Error", "Stock not found")
        return 1


def validate_input(user_input):
    """Limits user input to 10 characters."""
    max_length = 10  # Maximum allowed length of the input
    return len(user_input) <= max_length


# The main window
window = Tk()
window.geometry("1400x1000")
window.title("Stock Analyzer")

# The frame for the main window
frame = Frame(window)
frame.pack()

# Creating the Tkinter frames
stock_info_frame = LabelFrame(frame, text="Stock Information")
stock_info_frame.grid(row=0, column=0, padx=20, pady=20)

stock_graph_frame = LabelFrame(frame, text="Graph")
stock_graph_frame.grid(row=1, column=0, padx=20, pady=20)

# Creating the Tkinter labels to go in the frames
stock_name_label = Label(stock_info_frame, text="Enter a stock ticker:")
stock_name_label.grid(row=0, column=0)

new_stock_price_label = Label(stock_info_frame, text="Current stock price:")
new_stock_price_label.grid(row=0, column=1)

# Creating stock price frame, using Tkinter StringVar to allow it to be updated on click
stock_price_value_text = StringVar(value="N/A")
stock_price_value_label = Label(stock_info_frame, textvariable=stock_price_value_text)
stock_price_value_label.grid(row=1, column=1)

# Register the validation function
validate_cmd = window.register(validate_input)

# Creates an entry field using Tkinter. Validates on each keypress that the length is not > 10
stock_entry = Entry(stock_info_frame, validate='key', validatecommand=(validate_cmd, '%P'), width=20, borderwidth=5)
stock_entry.grid(row=1, column=0)

date_range_label = Label(stock_info_frame, text="Time period")
date_range_label.grid(row=0, column=2)

date_range_selector = ttk.Combobox(stock_info_frame, values=["5 days", "1 month", "3 months", "6 months",
                                                             "1 year", "2 years", "5 years"])
date_range_selector.grid(row=1, column=2)

# Adding padding to the widgets
for widget in stock_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Creating analyze stock button
analyze_stock_button = Button(stock_info_frame, text="Analyze Stock", command=click)
analyze_stock_button.grid(row=3, column=1, pady=5)


def retrieve_date_range():
    """Retrieves user info from the date range fields, and sets the new date range in the User class."""
    date_range = date_range_selector.get()
    if date_range == "5 days":
        date_range = "5d"
    elif date_range == "1 month":
        date_range = "1mo"
    elif date_range == "3 months":
        date_range = "3mo"
    elif date_range == "6 months":
        date_range = "6mo"
    elif date_range == "1 year":
        date_range = "1y"
    elif date_range == "2 years":
        date_range = "2y"
    elif date_range == "5 years":
        date_range = "5y"
    user1.set_date_range(date_range)


def _quit():
    window.quit()  # stops mainloop
    window.destroy()  # this is necessary on Windows to prevent Fatal Python Error: PyEval_RestoreThread: NULL state


# Creating a Quit button
quit_button = Button(frame, text="Quit", command=_quit)
quit_button.config(width=50)
quit_button.grid(row=5, column=0, padx=20, pady=20)

# Creates the GUI
window.mainloop()