# -*- coding: utf-8 -*-
"""
Created on Tue May 18 19:02:24 2021

@author: wujor
"""

from UIS import *

import pandas as pd
import pandas_datareader.data as web
import statistics
import numpy as np
import matplotlib.pyplot as plt

#start_date = None
start_date = '1-1-2020'
#start_date = '1-1-2006'
#end = '12-20-2019'



SPYdata = web.DataReader('SPY', 'stooq', start=start_date) # stooq 
TLTdata = web.DataReader('TLT', 'stooq', start=start_date)


#SPYdata = web.DataReader('SPY', 'yahoo', start)
#TLTdata = web.DataReader('TLT', 'yahoo', start)

SPYdata = SPYdata.reindex(index=SPYdata.index[::-1]) #if using stooq
TLTdata = TLTdata.reindex(index=TLTdata.index[::-1])

#begin executable code
period = 50
sharpe_factor = 2

periodsortino = 60
sortino_factor = 2

#best settings 
#testing from 2005 to 7/21/2021, ROR:
# 50/1: 40.465
# 50/1.25: 39.518
# 50/1.5: 38.614
# 50/2: 37.449


z = sharpePortfolio(SPYdata,TLTdata,period,sharpe_factor)
z1 = sortinoPortfolio(SPYdata,TLTdata,periodsortino,sortino_factor)


plt.figure(1)
plt.plot(z.loc[:,"Asset 1"]/z.iloc[0]["Asset 1"])
plt.plot(z.loc[:,"Asset 2"]/z.iloc[0]["Asset 2"])
plt.plot(z.loc[:,"Allocation"])

last_a=0.5
last_q=0
total = 1
for q in range(0,z.shape[0]):
    a = z.iloc[q]["Allocation"]
    if a != last_a:
        last_q=q-1
        total = z.iloc[q-1]['Split']
        last_a = a
    z.iloc[q]['Split'] = total*(a * z.iloc[q]["Asset 1"]/z.iloc[last_q]["Asset 1"] + (1-a)*z.iloc[q]["Asset 2"]/z.iloc[last_q]["Asset 2"])

plt.title("UIS w/ Sharpe Ratio")
plt.plot(z.loc[:,'Split'])
plt.legend(["SPY", "TLT", "ALLOCATION",  "COMBINED"])

RR_SPY = ((SPYdata.iloc[-1,3]/SPYdata.iloc[0,3]) - 1)*100
RR_TLT = ((TLTdata.iloc[-1,3]/TLTdata.iloc[0,3]) - 1)*100
RR_SPLIT = ((z.iloc[-1]['Split']/z.iloc[0]['Split']) - 1)*100

x=getSharpe(SPYdata.loc[:,'Close'], 1)
y=getSharpe(TLTdata.loc[:,'Close'], 1)
zz=getSharpe(z.loc[:,"Split"], 1)

print()
print("BEGIN SHARPE RATIO DATA")
print("SPY RoR: ", RR_SPY, "  SPY Sharpe Ratio: ", x)
print("TLT RoR: ", RR_TLT, "  TLT Sharpe Ratio: ", y)
print("Sharpe Adaptive Allocation RoR: ", RR_SPLIT, "  Adaptive Allocation Sharpe Ratio: ", zz)
print("Current Portfolio Allocation to SPY: ", str(z.iloc[-1]["Allocation"]*100) + "%")
print()




plt.figure(2)
plt.plot(z1.loc[:,"Asset 1"]/z1.iloc[0]["Asset 1"])
plt.plot(z1.loc[:,"Asset 2"]/z1.iloc[0]["Asset 2"])
plt.plot(z1.loc[:,"Allocation"])

last_a1=0.5
last_q1=0
total1 = 1
for q1 in range(0,z1.shape[0]):
    a1 = z1.iloc[q1]["Allocation"]
    if a1 != last_a1:
        last_q1=q1-1
        total1 = z1.iloc[q1-1]['Split']
        last_a1 = a1
    z1.iloc[q1]['Split'] = total1*(a1 * z1.iloc[q1]["Asset 1"]/z1.iloc[last_q1]["Asset 1"] + (1-a1)*z1.iloc[q1]["Asset 2"]/z1.iloc[last_q1]["Asset 2"])

plt.title("UIS w/ Sortino Ratio")
plt.plot(z1.loc[:,'Split'])
plt.legend(["SPY", "TLT", "ALLOCATION",  "COMBINED"])

RR_SPY1 = ((SPYdata.iloc[-1,3]/SPYdata.iloc[0,3]) - 1)*100
RR_TLT1 = ((TLTdata.iloc[-1,3]/TLTdata.iloc[0,3]) - 1)*100
RR_SPLIT1 = ((z1.iloc[-1]['Split']/z1.iloc[0]['Split']) - 1)*100

x1=getSharpe(SPYdata.loc[:,'Close'], 1)
y1=getSharpe(TLTdata.loc[:,'Close'], 1)
zz1=getSharpe(z1.loc[:,"Split"], 1)

print()
print("BEGIN SORTINO RATIO DATA")
print("SPY RoR: ", RR_SPY1, "  SPY Sharpe Ratio: ", x1)
print("TLT RoR: ", RR_TLT1, "  TLT Sharpe Ratio: ", y1)
print("Sortino Adaptive Allocation RoR: ", RR_SPLIT1, "  Adaptive Allocation Sharpe Ratio: ", zz1)
print("Current Portfolio Allocation to SPY: ", str(z1.iloc[-1]["Allocation"]*100) + "%")
print()