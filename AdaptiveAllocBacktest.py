# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 22:30:59 2022

@author: wujor
"""

from asyncio.windows_events import NULL
import pandas as pd
import pandas_datareader.data as web
import statistics as stat
from scipy.stats import norm, skew, kurtosis
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import copy

from dateutil.relativedelta import relativedelta
from datetime import date

#start/end date Y-m-d
startDate = '2019-1-1'
endDate = '2022-1-1'

#lookback and volatility factors
period = 50
fsharpe = 1
fsortino = 1

#Risk Free Rate, conversion from yearly yield to daily
MAR = 0

#Redo of sharpe and sortino
# volatility varies with the square root of time. convert daily returns to yearly with daily x root(252).

# SHARPE FORMULA: (RETURN - RISKFREE) / STDEV OF EXCESS RETURNS
# SORTINO FORMULA: (RETURN - RISKFREE) / STDEV OF DOWNSIDE ONLY
# USE ARITHMETIC AVERAGES

def getDailyR(frame):
    dR = np.zeros(frame.shape[0]-1)
    for i in range(1,frame.shape[0]):
        dR[i-1] = frame.iloc[i] / frame.iloc[i-1] - 1
    #dRpd = pd.DataFrame(dR, columns=["Daily Returns"])
    return dR
    
def sharpeRatio(frame, f):
    dR = np.zeros(frame.shape[0]-1)
    for i in range(1,frame.shape[0]):
        dR[i-1] = frame.iloc[i] / frame.iloc[i-1] - 1
    mean = stat.mean(dR)
    sigma = stat.stdev(dR)
    return (mean / (sigma**f)) * pow(252,0.5)

def sortinoRatio(frame, f):
    dR = np.zeros(frame.shape[0]-1)
    for i in range(1,frame.shape[0]):
        dR[i-1] = frame.iloc[i] / frame.iloc[i-1] - 1
    dRd = copy.deepcopy(dR)
    for q in range(1,len(dRd)):
        if dRd[q] >= 0.0:
            dRd[q] = 0
    mean = stat.mean(dR)
    sigma = stat.stdev(dRd)
    return (mean / (sigma**f)) * pow(252,0.5)

def sTest(arg,f):
    dR = np.zeros(len(arg)-1)
    for i in range(1,len(arg)):
        dR[i-1] = arg[i] / arg[i-1] - 1
    #print(dR)
    dRd = copy.deepcopy(dR)
    for q in range(1,len(dRd)):
        if dRd[q] >= 0.0:
            dRd[q] = 0
    #print(dR)
    #print(dRd)
    mean = stat.mean(dR)
    sigma = stat.stdev(dRd)
    return (mean / (sigma**f)) * pow(252,0.5)

def GSharpeRatio():
    pass

def GSortinoRatio():
    pass

def calcPortfolio(frame1, frame2, period, f, ratio):
    if frame1.shape != frame2.shape:
        return -999

    #only checking close price of frame1 for now bc it is assumed that the frames have the same column indexes
    #TODO - fix that so we check both frames?
    if 'Close' in frame1:
        #print(frame1.iloc[0].index)
        #print([frame1.columns.get_loc(c) for c in frame1.iloc[0].index if c in frame1])
        cc = frame1.columns.get_loc('Close')
        #print(f'Closing price is at index {cc}')
    else:
        return -999

    P = pd.DataFrame(np.nan, index=frame1.index, columns=['Asset 1', 'Asset 2', 'Allocation', 'Split'])
    a = .5 #initial allocation to frame 1
    i = period
    last_i = 0
    while i < frame1.shape[0]:
        pastMonth = frame1.iloc[i-1].name.month
        nowMonth = frame1.iloc[i].name.month
        if pastMonth != nowMonth:
            P.iloc[last_i:i,0] = frame1.iloc[last_i:i,cc]
            P.iloc[last_i:i,1] = frame2.iloc[last_i:i,cc]
            P.iloc[last_i:i,2] = a
            #The code below appears to throw an issue with copy assignment warnings in the obb env
            #NEVERMIND THE COMMENTED OUT CODE DOESNT WORK BUT WHAT IS WRITTEN BELOW DOES
            #BELOW, THIS ISSUE IS CIRCUMVENTED USING ASSIGNMENT IN A FOR LOOP lol :sob:
            """P.iloc[last_i:i]['Asset 1'] = frame1.iloc[last_i:i]['Close']
            P.iloc[last_i:i]['Asset 2'] = frame2.iloc[last_i:i]['Close']
            P.iloc[last_i:i]['Allocation'] = a"""
            sharpe_max = -999
            for j in range(0,105,5):
                qq = (j)*frame1.iloc[i-period:i]['Close']/frame1.iloc[last_i]['Close'] \
                    + (100-j)*frame2.iloc[i-period:i]['Close']/frame2.iloc[last_i]['Close']
                if ratio == "sharpe":
                    temp = sharpeRatio(qq, f)
                elif ratio == "sortino":
                    temp = sortinoRatio(qq, f)
                #print(j, temp)
                if temp > sharpe_max:
                    sharpe_max = temp
                    a = j/100
                pass
            #print("Processing data for ", frame1.iloc[i].name)
            last_i = i
        i+=1
    for x in range(last_i,frame1.shape[0]):
        P.iloc[x]['Asset 1'] = frame1.iloc[x]['Close']
        P.iloc[x]['Asset 2'] = frame2.iloc[x]['Close']
        P.iloc[x]['Allocation'] = a
        #print("Processing data for ", frame1.iloc[x].name)
    return P

def findSplit(portfolio):
    last_a=portfolio.iloc[0]["Allocation"]
    last_q=0
    total = 1
    for q in range(0,portfolio.shape[0]):
        a = portfolio.iloc[q]["Allocation"]
        if a != last_a:
            last_q=q-1
            total = portfolio.iloc[q-1]['Split']
            last_a = a
        portfolio.iloc[q]['Split'] = \
            total*(a * portfolio.iloc[q]["Asset 1"]/portfolio.iloc[last_q]["Asset 1"] \
                   + (1-a)*portfolio.iloc[q]["Asset 2"]/portfolio.iloc[last_q]["Asset 2"])
    pass

def showPortfolio(portfolio, title, legend):
    plt.plot(portfolio.loc[:,"Asset 1"]/portfolio.iloc[0]["Asset 1"])
    plt.plot(portfolio.loc[:,"Asset 2"]/portfolio.iloc[0]["Asset 2"])
    plt.plot(portfolio.loc[:,"Allocation"])
    plt.plot(portfolio.loc[:,'Split'])
    plt.title(title)
    plt.legend(legend)
    plt.show() #TODO - the program hangs after this line unless you close all plots - make this threaded in main

def portfolioStatistics(portfolio, title):
    #FIND ROI
    A1ROI = (portfolio.iloc[-1]["Asset 1"] - portfolio.iloc[0]["Asset 1"]) / portfolio.iloc[0]["Asset 1"] * 100
    A2ROI = (portfolio.iloc[-1]["Asset 2"] - portfolio.iloc[0]["Asset 2"]) / portfolio.iloc[0]["Asset 2"] * 100
    splitROI = (portfolio.iloc[-1]["Split"] - portfolio.iloc[0]["Split"]) / portfolio.iloc[0]["Split"] * 100

    #find time difference in years
    elapsedTime = portfolio.iloc[-1].name - portfolio.iloc[0].name
    elapsedTime = elapsedTime / np.timedelta64(1, 'Y')
    #print(elapsedTime)
    
    #FIND CAGR
    A1CAGR = (pow(portfolio.iloc[-1]["Asset 1"] / portfolio.iloc[0]["Asset 1"], 1/elapsedTime) - 1) * 100
    A2CAGR = (pow(portfolio.iloc[-1]["Asset 2"] / portfolio.iloc[0]["Asset 2"], 1/elapsedTime) - 1) * 100
    splitCAGR = (pow(portfolio.iloc[-1]["Split"] / portfolio.iloc[0]["Split"], 1/elapsedTime) - 1) * 100
    #FIND SHARPE AND SORTINO RATIOS
    A1Sharpe = sharpeRatio(portfolio.loc[:,"Asset 1"],1)
    A1Sortino = sortinoRatio(portfolio.loc[:,"Asset 1"],1)
    A2Sharpe = sharpeRatio(portfolio.loc[:,"Asset 2"],1)
    A2Sortino = sortinoRatio(portfolio.loc[:,"Asset 2"],1)
    SplitSharpe = sharpeRatio(portfolio.loc[:,"Split"],1)
    SplitSortino = sortinoRatio(portfolio.loc[:,"Split"],1)
    
    #FIND MAX DRAWDOWN
    #TODO
    
    #FIND BEST/WORST YEAR
    #TODO
    
    #DISPLAY RESULTS
    print()
    print("BEGIN STATISTICS: " + title)
    print()
    print("------ROI------")
    print("Asset 1 ROI: " + "{:6.4f}".format(A1ROI) + "%")
    print("Asset 2 ROI: " + "{:6.4f}".format(A2ROI) + "%")
    print("Split ROI:   " + "{:6.4f}".format(splitROI) + "%")
    print()
    print("------CAGR-----")
    print("Asset 1 CAGR: " + "{:6.4f}".format(A1CAGR) + "%")
    print("Asset 2 CAGR: " + "{:6.4f}".format(A2CAGR) + "%")
    print("Split CAGR:   " + "{:6.4f}".format(splitCAGR) + "%")
    print()
    print("-Sharpe Ratios-")
    print("Asset 1: " + "Sharpe: {:6.4f} | ".format( A1Sharpe ) \
          + "Sortino: {:6.4f}".format( A1Sortino ))
    print("Asset 2: " + "Sharpe: {:6.4f} | ".format( A2Sharpe ) \
          + "Sortino: {:6.4f}".format( A2Sortino ))
    print("Split:   " + "Sharpe: {:6.4f} | ".format( SplitSharpe ) \
          + "Sortino: {:6.4f}".format( SplitSortino ))
    print()
    pass

def var_historic(r, level=1): #convert daily var to monthy: x root(days)
    """
    Takes in a series of returns (r), and the percentage level(level)
    Returns the historic Value at Risk at a specified level
    i.e. returns the number such that "level" percent of the returns
    fall below that number, and the (100-level) percent are above
    """
    if isinstance(r, pd.DataFrame):
        return r.aggregate(var_historic, level=level)
    elif isinstance(r, pd.Series) or isinstance(r, np.ndarray):
        return np.percentile(r, level, interpolation="lower")
    else:
        raise TypeError("Expected r to be a Series or DataFrame")
        
def var_gaussian(r, level=5, modified=False):
    """
    Returns the Parametric Gauusian VaR of a Series or DataFrame
    If "modified" is True, then the modified VaR is returned,
    using the Cornish-Fisher modification
    """
    # compute the Z score assuming it was Gaussian
    z = norm.ppf(level/100)
    if modified:
        # modify the Z score based on observed skewness and kurtosis
        s = skew(r)
        k = kurtosis(r)
        z = (z +
                (z**2 - 1)*s/6 +
                (z**3 -3*z)*(k-3)/24 -
                (2*z**3 - 5*z)*(s**2)/36
            )
    return (r.mean() + z*r.std(ddof=0))

def varCovar(): #TODO
    pass

def getCurrentSplit(frame1, frame2, period, f, ratio):
    sharpe_max = -999
    for i in range(0,105,5):
        q = (i)*frame1.iloc[:]['Close']/frame1.iloc[0]['Close']\
            + (100-i)*frame2.iloc[:]['Close']/frame2.iloc[0]['Close']
        #print(q)
        if ratio == "sharpe":
            temp = sharpeRatio(q, f)
        elif ratio == "sortino":
            temp = sortinoRatio(q, f)
        #print(i, temp)
        if temp > sharpe_max:
            sharpe_max = temp
            a = i/100
            #print("found " + str(a))
            
    print(ratio + " ALLOCATION IS " + str(a*100) + "%")
    pass
