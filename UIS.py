# -*- coding: utf-8 -*-
"""
Created on Sat May 15 18:13:13 2021

@author: wujor
"""

import pandas as pd
import pandas_datareader.data as web
import statistics
import numpy as np
import matplotlib.pyplot as plt

#send this function only the subarray you want the sharpe for. root(252) is set up for daily returns
#TODO
#all these ratios are supposed to use geometric mean for calculation. use risk-free rate of 1%
def getSharpe(frame, factor): 
    dailyR = np.zeros(frame.shape[0]-1)
    for i in range(1,frame.shape[0]):
        dailyR[i-1] = (frame.iloc[i] / frame.iloc[i-1] - 1)
    mean = statistics.mean(dailyR)
    stdev = statistics.pstdev(dailyR)
    return (mean / (stdev**factor)) * pow(252,0.5) 


def getSortino(frame, factor): #TODO
    #this calculation is incorrect - see red rock capital white paper
    dailyR = np.zeros(frame.shape[0]-1)
    for i in range(1,frame.shape[0]):
        temprtn = (frame.iloc[i] / frame.iloc[i-1] - 1)
        if temprtn >= 0:
            dailyR[i-1] = 0
        else:
            dailyR[i-1] = temprtn
        #print(str(temprtn) + " " + str(bool(temprtn >= 0 )))
    mean = statistics.mean(dailyR)
    stdev = statistics.pstdev(dailyR)
    #print(mean, stdev, (mean / (stdev**factor)) * pow(252,0.5))
    return (mean / (stdev**factor)) * pow(252,0.5) 





#simulate portfolio
def sharpePortfolio(frame1, frame2, lookBack,f):
    if frame1.shape != frame2.shape:
        return -999
    
    P = pd.DataFrame(np.nan, index=frame1.index, columns=['Asset 1', 'Asset 2', 'Allocation', 'Split'])
    #initial portfolio amount is $10k
    a = .5 #initial allocation to frame 1
    
    i = lookBack  
    last_i = 0
    while i < frame1.shape[0]:
        pastMonth = frame1.iloc[i-1].name.month
        nowMonth = frame1.iloc[i].name.month
        if pastMonth != nowMonth:
            P.iloc[last_i:i]['Asset 1'] = frame1.iloc[last_i:i]['Close']
            P.iloc[last_i:i]['Asset 2'] = frame2.iloc[last_i:i]['Close']
            P.iloc[last_i:i]['Allocation'] = a
            sharpe_max = -9999999999
            for j in range(0,105,5):
                qq = (j)*frame1.iloc[i-lookBack:i]['Close']/frame1.iloc[last_i]['Close'] + (100-j)*frame2.iloc[i-lookBack:i]['Close']/frame2.iloc[last_i]['Close']
                temp = getSharpe(qq , f)
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



def sortinoPortfolio(frame1, frame2, lookBack,f):
    if frame1.shape != frame2.shape:
        return -999
    
    P = pd.DataFrame(np.nan, index=frame1.index, columns=['Asset 1', 'Asset 2', 'Allocation', 'Split'])
    #initial portfolio amount is $10k
    a = .5 #initial allocation to frame 1
    
    i = lookBack  
    last_i = 0
    while i < frame1.shape[0]:
        pastMonth = frame1.iloc[i-1].name.month
        nowMonth = frame1.iloc[i].name.month
        if pastMonth != nowMonth:
            P.iloc[last_i:i]['Asset 1'] = frame1.iloc[last_i:i]['Close']
            P.iloc[last_i:i]['Asset 2'] = frame2.iloc[last_i:i]['Close']
            P.iloc[last_i:i]['Allocation'] = a
            sortino_max = -9999999999
            for j in range(0,105,5):
                qq = (j)*frame1.iloc[i-lookBack:i]['Close']/frame1.iloc[last_i]['Close'] + (100-j)*frame2.iloc[i-lookBack:i]['Close']/frame2.iloc[last_i]['Close']
                temp = getSortino(qq , f)
                #print(j, temp)
                if temp > sortino_max:
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