# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 18:54:41 2021

@author: wujor
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
from scipy import stats
import seaborn as sns

# Create a list of tickers and weights
tickers = ['BND', 'VB', 'VEA', 'VOO', 'VWO']
wts = [0.1,0.2,0.25,0.25,0.2]

price_data = web.get_data_yahoo(tickers,
                               start = '2013-01-01',
                               end = '2018-03-01')
price_data = price_data['Adj Close']

ret_data = price_data.pct_change()[1:]

port_ret = (ret_data * wts).sum(axis = 1)


benchmark_price = web.get_data_yahoo('SPY',
                               start = '2013-01-01',
                               end = '2018-03-01')
                               
benchmark_ret = benchmark_price["Adj Close"].pct_change()[1:]


sns.regplot(benchmark_ret.values,
port_ret.values)
plt.xlabel("Benchmark Returns")
plt.ylabel("Portfolio Returns")
plt.title("Portfolio Returns vs Benchmark Returns")
plt.show()

(beta, alpha) = stats.linregress(benchmark_ret.values,
                port_ret.values)[0:2]
                
print("The portfolio beta is", round(beta, 4))
print("The portfolio alpha is", round(alpha,5))