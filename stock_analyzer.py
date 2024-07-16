# Author: Jacob Deaton
# GitHub username: jd-58
# Date: 7/2/2024
# Description: An app that will show various information about any stock the user chooses.
# Suggested features: showing highest % gains from previous day along with basic start and close values.
# Search bar to find stocks, and ability to favorite stocks.
import customtkinter
# Importing Libraries
import numpy as np
import yfinance as yf
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter import messagebox
from customtkinter import *
from customtkinter import ctk_tk
from matplotlib.dates import DayLocator
from datetime import datetime

# Sets the default customtkinter theme to a custom theme
customtkinter.set_default_color_theme("C:/apps/ctk_theme_builder/user_themes/Cobalt.json")


class User:
    """Stores user's selected stock ticker and the date range for the stock."""

    def __init__(self, stock_ticker=None, date_range=None, stock1_price=0, graph_canvas_1=None, stock_volume=None,
                 stock_high=None, stock_open=None, stock_perct_change=None):
        """Creates a User object with their specified stock ticker and date range."""
        self._stock_ticker = stock_ticker
        self._date_range = date_range
        self._stock1_price = stock1_price
        self._graph_canvas_1 = graph_canvas_1
        self._stock_volume = stock_volume
        self._stock_high = stock_high
        self._stock_open = stock_open
        self._stock_perct_change = stock_perct_change

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
        stock_data['Date'] = stock_data['Date'].dt.strftime('%m/%d/%Y')  # m/d/yyy displays as d/m/yyyy, unsure why
        stock_data["%_Change"] = np.round(stock_data["Adj_Close"].pct_change() * 100, 2)
        stock_data["Open"] = np.round(stock_data["Open"], 2)
        stock_data["High"] = np.round(stock_data["High"], 2)
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

    def set_stock_volume(self, new_stock_volume):
        """Sets the stock volume"""
        self._stock_volume = new_stock_volume
        return self._stock_volume

    def set_stock_open(self, new_stock_open):
        """Sets the stock opening value"""
        self._stock_open = new_stock_open
        return self._stock_open

    def set_stock_perct_change(self, new_stock_perct_change):
        """Sets the stock percentage change"""
        self._stock_perct_change = new_stock_perct_change
        return self._stock_perct_change

    def set_stock_high(self, new_stock_high):
        """Sets the stock high value"""
        self._stock_high = new_stock_high
        return self._stock_high

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

    def get_stock_open(self):
        """Returns the stock opening value"""
        return self._stock_open

    def get_stock_volume(self):
        """Returns the stock volume"""
        return self._stock_volume

    def get_stock_perct_change(self):
        """Returns the stock percentage change"""
        return self._stock_perct_change

    def get_stock_high(self):
        """Returns the stock high value"""
        return self._stock_high


user1 = User(None, None)


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
    current_stock_volume = user_stock_information.volume[current_date_index]
    current_stock_open = user_stock_information.open_price[current_date_index]
    current_stock_perct_change = str(user_stock_information.percent_change[current_date_index]) + " %"
    current_stock_high = user_stock_information.high[current_date_index]
    current_user_stock_price = round(current_user_stock_price, 2)
    user1.set_stock1_price(current_user_stock_price)
    user1.set_stock_open(current_stock_open)
    user1.set_stock_volume(current_stock_volume)
    user1.set_stock_perct_change(current_stock_perct_change)
    user1.set_stock_high(current_stock_high)
    update_stock_information_labels()
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
    fig.set_facecolor('#002240')  # Set background of Figure to match the frame
    ax = fig.add_subplot()
    ax.plot(x_axes, y_axes, color='white')
    ax.set_facecolor('#284A68')  # Set background color of graph to a grey-blue color
    ax.set_xlabel("Date", color='#DBDBDB')
    ax.set_ylabel("Adj. Close (USD)", color='#DBDBDB')

    # Configure tick marks. Intervals are in number of business days
    if user1.get_date_range() == "5d":
        # Set major ticks to every day. No minor ticks.
        ax.xaxis.set_major_locator(DayLocator())
        ax.grid(True, linestyle=':')
    elif user1.get_date_range() == "1mo":
        # Set major ticks to weekly, and minor ticks to daily.
        ax.xaxis.set_major_locator(DayLocator(interval=5))
        ax.xaxis.set_minor_locator(DayLocator())
        ax.grid(True, linestyle=':')
    elif user1.get_date_range() == "3mo":
        # Set major ticks to bi-weekly, and minor ticks to daily.
        ax.xaxis.set_major_locator(DayLocator(interval=10))
        ax.xaxis.set_minor_locator(DayLocator())
        ax.grid(True, linestyle=':')
    elif user1.get_date_range() == "6mo":
        # Major ticks to each monthly , minor ticks to weekly
        ax.xaxis.set_major_locator(DayLocator(interval=20))
        ax.xaxis.set_minor_locator(DayLocator(interval=5))
        ax.grid(True, linestyle=':')
    elif user1.get_date_range() == "1y":
        # Major ticks to every other month, minor to every other week
        ax.xaxis.set_major_locator(DayLocator(interval=41))
        ax.xaxis.set_minor_locator(DayLocator(interval=10))
        ax.grid(True, linestyle=':')
    elif user1.get_date_range() == "2y":
        # Major ticks to every 4 months, minor to monthly
        ax.xaxis.set_major_locator(DayLocator(interval=80))
        ax.xaxis.set_minor_locator(DayLocator(interval=20))
        ax.grid(True, linestyle=':')
    elif user1.get_date_range() == "5y":
        # Major ticks to yearly, minor ticks to monthly
        ax.xaxis.set_major_locator(DayLocator(interval=250))
        ax.xaxis.set_minor_locator(DayLocator(interval=20))
        ax.grid(True, linestyle=':')
    ax.spines['bottom'].set_color('#DBDBDB')
    ax.spines['left'].set_color('#DBDBDB')
    ax.spines['top'].set_color('#DBDBDB')
    ax.spines['right'].set_color('#DBDBDB')
    ax.tick_params(axis='x', which='both', colors='#DBDBDB')
    ax.tick_params(axis='y', colors='#DBDBDB')
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
    fig.suptitle(graph_title, color='#DBDBDB')

    if user1.get_graph_canvas_1() is None:
        # Creating canvas and embedding graph to Tkinter. Adds the toolbar to the graph.
        canvas = FigureCanvasTkAgg(fig, master=stock_graph_frame)
        canvas.get_tk_widget().grid(row=0, column=0)
        canvas.draw_idle()
        toolbar = NavigationToolbar2Tk(canvas, frame, pack_toolbar=False)
        # toolbar.config(background='#DBDBDB')
        # toolbar._message_label.config(background='#002240')
        # for button in toolbar.winfo_children():
            # button.config(background='blue')
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


def update_stock_information_labels():
    """Updates the stock price label to the current user1 stock price."""
    stock_price_value_text.set(str(user1.get_stock1_price()))
    stock_volume_text.set(str(user1.get_stock_volume()))
    stock_open_text.set(str(user1.get_stock_open()))
    stock_perct_change_text.set(str(user1.get_stock_perct_change()))
    stock_high_text.set(str(user1.get_stock_high()))


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
window = CTk()
window.geometry("1400x1000")
window.title("Stock Analyzer")
# Sets the background color of the graph toolbar to match the window
window.tk_setPalette(background="#002240", selectColor="#1779A6", foreground="white")

# The frame for the main window
frame = CTkFrame(window)
frame.pack()

# Variable to put the current date into a string to use for Tkinter labels.

current_date = str(datetime.today().strftime('%m/%d/%Y'))  # m/d/yyy displays as d/m/yyyy, unsure why

# Creating the Tkinter frames
stock_info_frame = CTkFrame(frame)
stock_info_frame.grid(row=0, column=0, padx=20, pady=20)

stock_graph_frame = CTkFrame(frame)
stock_graph_frame.grid(row=1, column=0, padx=20, pady=20)

# Creating the Tkinter labels to go in the frames
stock_name_label = CTkLabel(stock_info_frame, text="Enter a stock ticker:")
stock_name_label.grid(row=0, column=1)

current_stock_information_string = "Stock information for " + current_date
current_stock_information_label = CTkLabel(stock_info_frame, text=current_stock_information_string)
current_stock_information_label.grid(row=3, column=2)

stock_price_value_text = StringVar(value="")
stock_price_value_label = CTkLabel(stock_info_frame, textvariable=stock_price_value_text)
new_stock_price_label = CTkLabel(stock_info_frame, text="Adj. Close")
new_stock_price_label.grid(row=4, column=0)
stock_price_value_label.grid(row=5, column=0)

stock_open_text = StringVar(value="")
stock_open_value = CTkLabel(stock_info_frame, textvariable=stock_open_text)
stock_open_label = CTkLabel(stock_info_frame, text="Open")
stock_open_label.grid(row=4, column=1)
stock_open_value.grid(row=5, column=1)

stock_high_text = StringVar(value="")
stock_high_label = CTkLabel(stock_info_frame, text="High")
stock_high_label.grid(row=4, column=2)
stock_high_value = CTkLabel(stock_info_frame, textvariable=stock_high_text)
stock_high_value.grid(row=5, column=2)

stock_perct_change_text = StringVar(value="")
stock_perct_change_label = CTkLabel(stock_info_frame, text="Daily Pct. Change")
stock_perct_change_label.grid(row=4, column=3)
stock_perct_change_value = CTkLabel(stock_info_frame, textvariable=stock_perct_change_text)
stock_perct_change_value.grid(row=5, column=3)

stock_volume_text = StringVar(value="")
stock_volume_label = CTkLabel(stock_info_frame, text='Volume')
stock_volume_label.grid(row=4, column=4)
stock_volume_value = CTkLabel(stock_info_frame, textvariable=stock_volume_text)
stock_volume_value.grid(row=5, column=4)

# Register the validation function
validate_cmd = window.register(validate_input)

# Creates an entry field using Tkinter. Validates on each keypress that the length is not > 10
stock_entry = CTkEntry(stock_info_frame, validate='key', validatecommand=(validate_cmd, '%P'), width=100)
stock_entry.grid(row=1, column=1)

date_range_label = CTkLabel(stock_info_frame, text="Time period")
date_range_label.grid(row=0, column=3)

date_range_selector = CTkComboBox(stock_info_frame, state='readonly', values=["5 days", "1 month", "3 months",
                                                                              "6 months", "1 year", "2 years",
                                                                              "5 years"])
date_range_selector.set("5 days")
date_range_selector.grid(row=1, column=3)

# Adding padding to the widgets
for widget in stock_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Creating analyze stock button
analyze_stock_button = CTkButton(stock_info_frame, width=200, text="Analyze Stock", command=click, hover_color="green")
analyze_stock_button.grid(row=6, column=2, pady=5)


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
quit_button = CTkButton(frame, width=350, text="Quit", hover_color='red', command=_quit)
quit_button.grid(row=5, column=0, padx=20, pady=20)

# Creates the GUI
window.mainloop()
