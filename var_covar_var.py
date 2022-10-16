# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 14:30:15 2022

@author: wujor
"""

#TODO: make this into a callable function to use as an import file

import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import numpy as np
import datetime as dt
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import scipy

# Create our portfolio of equities
tickers = ['AAPL','FB', 'C', 'DIS']
 
# Set the investment weights (I arbitrarily picked for example)
weights = np.array([.25, .3, .15, .3])
 
# Set an initial investment level
initial_investment = 1000000
 
# Download closing prices
data = pdr.get_data_yahoo(tickers, start="2018-01-01", end=dt.date.today())['Close']
 
# From the closing prices, calculate periodic returns
returns = data.pct_change()
returns = returns.tail(-1)

# Generate Var-Cov matrix
cov_matrix = returns.cov()


# Calculate mean returns for each stock
avg_rets = returns.mean()
 
# Calculate mean returns for portfolio overall, 
# using dot product to 
# normalize individual means against investment weights
# https://en.wikipedia.org/wiki/Dot_product#:~:targetText=In%20mathematics%2C%20the%20dot%20product,and%20returns%20a%20single%20number.
port_mean = avg_rets.dot(weights)
 
# Calculate portfolio standard deviation
port_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))
 
# Calculate mean of investment
mean_investment = (1+port_mean) * initial_investment
             
# Calculate standard deviation of investmnet
stdev_investment = initial_investment * port_stdev

# Select our confidence interval (I'll choose 95% here)
conf_level1 = 0.05

# Using SciPy ppf method to generate values for the
# inverse cumulative distribution function to a normal distribution
# Plugging in the mean, standard deviation of our portfolio
# as calculated above
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html
cutoff1 = scipy.stats.norm.ppf(conf_level1, mean_investment, stdev_investment)

# Finally, we can calculate the VaR at our confidence interval
var_1d1 = initial_investment - cutoff1
# var_1d1
# output
# 22347.7792230231

# Calculate n Day VaR
var_array = []
num_days = int(15)
for x in range(1, num_days+1):    
    var_array.append(np.round(var_1d1 * np.sqrt(x), 2))
    print(str(x) + " day VaR @ 95% confidence: " + str(np.round(var_1d1 * np.sqrt(x), 2)))

# Build plot
plt.figure(1)
plt.xlabel("Day #")
plt.ylabel("Max portfolio loss (USD)")
plt.title("Max portfolio loss (VaR) over 15-day period")
plt.plot(var_array, "r")
plt.grid()

# Repeat for each equity in portfolio
plt.figure(2)
returns['AAPL'].hist(bins=40, density=True, histtype="stepfilled", alpha=0.5)
#returns['AAPL'].hist(bins=40, normed=True, histtype="stepfilled", alpha=0.5)
x = np.linspace(port_mean - 3*port_stdev, port_mean + 3*port_stdev, 100)
plt.plot(x, scipy.stats.norm.pdf(x, port_mean, port_stdev), "r")
plt.title("AAPL returns (binned) vs. normal distribution")
plt.show()

plt.figure(3)
returns['FB'].hist(bins=40, density=True, histtype="stepfilled", alpha=0.5)
#returns['AAPL'].hist(bins=40, normed=True, histtype="stepfilled", alpha=0.5)
x = np.linspace(port_mean - 3*port_stdev, port_mean + 3*port_stdev, 100)
plt.plot(x, scipy.stats.norm.pdf(x, port_mean, port_stdev), "r")
plt.title("FB returns (binned) vs. normal distribution")
plt.show()

plt.figure(4)
returns['C'].hist(bins=40, density=True, histtype="stepfilled", alpha=0.5)
#returns['AAPL'].hist(bins=40, normed=True, histtype="stepfilled", alpha=0.5)
x = np.linspace(port_mean - 3*port_stdev, port_mean + 3*port_stdev, 100)
plt.plot(x, scipy.stats.norm.pdf(x, port_mean, port_stdev), "r")
plt.title("C returns (binned) vs. normal distribution")
plt.show()

plt.figure(5)
returns['DIS'].hist(bins=40, density=True, histtype="stepfilled", alpha=0.5)
#returns['AAPL'].hist(bins=40, normed=True, histtype="stepfilled", alpha=0.5)
x = np.linspace(port_mean - 3*port_stdev, port_mean + 3*port_stdev, 100)
plt.plot(x, scipy.stats.norm.pdf(x, port_mean, port_stdev), "r")
plt.title("DIS returns (binned) vs. normal distribution")
plt.show()