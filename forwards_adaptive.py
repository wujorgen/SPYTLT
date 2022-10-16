# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 12:44:37 2021

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


#SPYdata = web.DataReader('SPY', 'yahoo', start) # stooq 
#TLTdata = web.DataReader('TLT', 'yahoo', start)

SPYdata = SPYdata.reindex(index=SPYdata.index[::-1]) #if using stooq
TLTdata = TLTdata.reindex(index=TLTdata.index[::-1])

#begin executable code
period = 50
sharpe_factor = 2
sortino_factor = 2

SPYd = SPYdata[-(period):]
TLTd = TLTdata[-(period):]

#SPYd = SPYdata[-(period)-1:-1]
#TLTd = TLTdata[-(period)-1:-1]

#SPYd = SPYdata[-70:-20]
#TLTd = TLTdata[-70:-20]

sharpe_max = -9999
for i in range(0,105,5):
    q = (i)*SPYd.iloc[:]['Close']/SPYd.iloc[0]['Close'] + (100-i)*TLTd.iloc[:]['Close']/TLTd.iloc[0]['Close']
    #print(q)
    temp = getSharpe( q , sharpe_factor )
    print(i, temp)
    if temp > sharpe_max:
        sharpe_max = temp
        a = i/100
        print("found " + str(a))
        
print("ALLOCATION IS " + str(a*100) + "%")

print()
'''
sortino_max = -9999999999
for i in range(0,105,5):
    r = (i)*SPYd.iloc[:]['Close']/SPYd.iloc[0]['Close'] + (100-i)*TLTd.iloc[:]['Close']/TLTd.iloc[0]['Close']
    #print(q)
    tempura = getSortino( r , sortino_factor )
    print(i, tempura)
    if tempura > sortino_max:
        sortino_max = tempura
        b = i/100
        print("found " + str(b))
        
print("ALLOCATION IS " + str(b*100) + "%")
'''