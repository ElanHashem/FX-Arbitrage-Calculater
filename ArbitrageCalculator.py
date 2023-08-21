import csv
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

ticker_names = ['USD',"EUR","GBP","JPY","CAD","AUD","MXN","SEK","SGD"]
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
    def __init__(self,name,values=[]):
        self.name = name
        self.values = values
        for comp in ticker_names:
            if name != comp:
                word = f"{comp}{name}=X"
                data = yf.download(tickers = word,period='1d',interval='1d')
                values.append(data['Close'][0])
        
data = yf.download(tickers = 'USDJPY=X',period='1d',interval='1d')
print(data)
print(data['Close'][0])
USD = Currency('USD')
print(USD.values[0])
