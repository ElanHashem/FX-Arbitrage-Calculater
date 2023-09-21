import csv
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

ticker_names = ['USD',"EUR","GBP","JPY","CAD","AUD","MXN","CHF"]
print(f"Select from what currency to what currency would you like to convert too out of the following {ticker_names}. Put in form USD/EUR")
input = input()
if len(input) != 7:
    print("Incorrect format, must be in USD/EUR form")
    exit()
first = input[:3]
if first not in ticker_names:
    print(f"{first} was not one of the currencies available")
    exit()
second = input[4:]
if second not in ticker_names:
    print(f"{second} was not one of the currencies available")
    exit()
def makeAbitrageData():
    filename = "ArbitrageData.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for ticker in ticker_names:
            for comp in ticker_names:
                if ticker != comp:
                    word = ticker+'/'+comp
                    row = [word]
                    csvwriter.writerow(row)
class Currency:
    def __init__(self,name):
        self.name = name
        self.values = {}
        for comp in ticker_names:
            if name != comp:
                word = f"{name}{comp}=X"
                data = yf.download(tickers = word,period='1d',interval='1d')
                self.values[f"{name}{comp}"] = data['Close'][0]
    def __repr__(self):
        return self.name
        
first_curr = Currency(first)
second_curr = Currency(second)
currency_list = []
for name in ticker_names:
    if name != first and name != second:
        currency_list.append(Currency(name))
currency_list.append(first_curr)
currency_list.append(second_curr)


#print(currency_list)
#print(currency_list[0].values.keys())
path = []
def triangleConverserion(start: Currency,middle: Currency,end: Currency):
    first_middle = start.values[f"{start.name}{middle.name}"]
    middle_end = middle.values[f"{middle.name}{end.name}"]
    return first_middle*middle_end
#print(triangleConverserion(currency_list[1],currency_list[0],currency_list[4]))

def getArbitragePath(start,end,currency_list,path):
    path.insert(0,end)
    direct_path = start.values[f"{start.name}{end.name}"]
    greatest_arbitrage = 0
    greatest_arbitrage_curr = 0
    for curr in currency_list:
        if curr != start and curr != end:
            curr_arbitrage = triangleConverserion(start,curr,end)
            if curr_arbitrage>greatest_arbitrage:
                greatest_arbitrage = curr_arbitrage
                greatest_arbitrage_curr = curr

    if direct_path>greatest_arbitrage:
        path.insert(0,start)
        return path
    else:
        currency_list.remove(end)
        return getArbitragePath(start,greatest_arbitrage_curr,currency_list,path)
#print(getArbitragePath(currency_list[1],currency_list[4],currency_list,path))        

def getArbitrageValue(path):
    ret = 1
    for i in range(len(path)-1):
        ret = ret*path[i].values[f"{path[i].name}{path[i+1].name}"]       
    return ret
#print(getArbitrageValue(path))
direct_value = first_curr.values[f"{first_curr.name}{second_curr.name}"]
getArbitragePath(first_curr,second_curr,currency_list,path)
best_value = getArbitrageValue(path)
if best_value == direct_value:
    print(f"The best path was the direct path of {path} of a rate of {best_value}")
else:
    print(f"The best path was the path of {path} of a rate of {best_value} compared to {direct_value}")
