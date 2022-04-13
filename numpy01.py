import pandas as pd
import time
stocks=[]
#显示所有列
stock_codes = []
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows',None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

df = pd.read_csv('stocks_name.csv')
for x,y in df.iterrows():
    for i in y:
        if i != "nan":
            stocks.append(i)
        else:
            stocks.pop(i)


    #print("waiting 30 scends")
    #time.sleep(10)
print(stocks)


