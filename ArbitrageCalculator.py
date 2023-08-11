import csv
print("sucsess")
filename = "ArbitrageData.csv"
ticker_names = ['USD',"EUR","GBP","JPY","CAD","AUD","MXN","SEK","SGD"]
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    for ticker in ticker_names:
        for comp in ticker_names:
            if ticker != comp:
                word = ticker+'/'+comp
                row = [word]
                csvwriter.writerow(row)
print("all done")
                