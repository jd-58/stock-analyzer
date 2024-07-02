# Author: Jacob Deaton
# GitHub username: jd-58
# Date: 7/2/2024
# Description: An app that will show various information about any stock the user chooses.

# Importing Libraries
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

print("Enter a stock ticker:")
user_ticker = str(input())
selected_yf_ticker = yf.Ticker(user_ticker)
data = yf.download(tickers=user_ticker, start="2019-09-10", end="2020-10-09")

# Show the data

print(data)
