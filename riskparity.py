# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 23:20:05 2022

@author: wujor
"""

import pandas as pd
import pandas_datareader.data as web
import statistics as stat
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import copy

from dateutil.relativedelta import relativedelta
from datetime import date

import AdaptiveAllocBacktest as AAB

#UPRO/TMF 40/60

#start/end date Y-m-d
startDate = '2015-1-1'
endDate = '2022-1-1'

#lookback and volatility factors
period = 50
fsharpe = 1
fsortino = 1

#BEGIN EXECUTABLE CODE
#get data on the tickers
uproData = yf.Ticker('upro')
tmfData = yf.Ticker('tmf')

uproDf = uproData.history(period='1d', start=startDate)
tmfDf = tmfData.history(period='1d', start=startDate)

uproDf.pct_change()