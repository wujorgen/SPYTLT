# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 23:23:03 2022

@author: wujor
"""

import AdaptiveAllocBacktest as AAB

import pandas as pd
import pandas_datareader.data as web
import statistics as stat
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import copy

from dateutil.relativedelta import relativedelta
from datetime import date

#start/end date Y-m-d
startDate = '2022-1-1'
endDate = '2021-5-1'

#lookback and volatility factors
period = 50
fsharpe = 1
fsortino = 1

#BEGIN EXECUTABLE CODE
#get data on the tickers
spyData = yf.Ticker('spy')
tltData = yf.Ticker('tlt')
#uproData = yf.Ticker('upro')
#tmfData = yf.Ticker('tmf')

#get the historical prices for this ticker, daily time frame
spyDf = spyData.history(period='1d', start=startDate)
tltDf = tltData.history(period='1d', start=startDate)
#uproDf = uproData.history(period='1d', start=startDate)
#tmfDf = tmfData.history(period='1d', start=startDate)

#chopped frames containing current data only
spyDcurrent = spyDf[-(period):]
tltDcurrent = tltDf[-(period):]
#uproDcurrent = uproDf[-(period):]
#tmfDcurrent = tmfDf[-(period):]

print(spyDcurrent.tail(5))

#make portfolios
uiSharpePort = AAB.calcPortfolio(spyDf, tltDf, period, fsharpe, "sharpe")
AAB.findSplit(uiSharpePort)
#print(uiSharpePort)
#uiSortinoPort = calcPortfolio(spyDf, tltDf, period, fsortino, "sortino")
#findSplit(uiSortinoPort)
#uprotmfSharpePort = AAB.calcPortfolio(uproDf, tmfDf, period, fsharpe, "sharpe")
#AAB.findSplit(uprotmfSharpePort)

#display information
plt.figure(1)
AAB.showPortfolio(uiSharpePort, "UIS w/ Sharpe", ["SPY", "TLT", "ALLOCATION",  "COMBINED"]) 
#TODO - the program hangs after this line unless you close all plots - make this threaded in main
#plt.figure(2)
#showPortfolio(uiSortinoPort, "UIS w/ Sortino", ["SPY", "TLT", "ALLOCATION",  "COMBINED"])
#plt.figure(3)
#showPortfolio(uprotmfSharpePort, "UPRO/TMF w/ Sharpe", ["UPRO", "TMF", "ALLOCATION",  "COMBINED"])


AAB.portfolioStatistics(uiSharpePort, "UIS w/ Sharpe")
#portfolioStatistics(uiSortinoPort, "UIS w/ Sortino")
#AAB.portfolioStatistics(uprotmfSharpePort, "UPRO/TMF w/ Sharpe")

AAB.getCurrentSplit(spyDcurrent, tltDcurrent, period, fsharpe, "sharpe")
#getCurrentSplit(spyDcurrent, tltDcurrent, period, fsortino, "sortino")
#AAB.getCurrentSplit(uproDcurrent, tmfDcurrent, period, fsharpe, "sharpe")
#todo: why do these frames take the period but not use it LOL


#uiSharpeDailyR = getDailyR(uiSharpePort.iloc[:]["Split"])*100
#spyDailyR = getDailyR(spyDf.iloc[:]["Close"])*100
uiSharpeDailyR = uiSharpePort['Split'].pct_change()*100
spyDailyR = spyDf['Close'].pct_change()*100
uiSharpeDailyR = uiSharpeDailyR.tail(-1)
spyDailyR = spyDailyR.tail(-1)
print()
print(str(AAB.var_historic(uiSharpeDailyR, level=5)))
print(str(AAB.var_historic(spyDailyR, level=5)))
print()
print(str(AAB.var_gaussian(uiSharpeDailyR, level=5, modified=True)))
print(str(AAB.var_gaussian(spyDailyR, level=5, modified=True)))
