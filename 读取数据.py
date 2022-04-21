import pandas as pd
import numpy as np
import talib
import mplfinance as mpf
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
"""设置格式"""
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows',None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

"""设置全局变量"""
START_TIME='2021-01-01 09:16:00'
END_TIME='2022-04-15 15:00:00'
TITLE_INFS=['open','close','low','high','volume']
HAND=5
MONEY=1_000_000
OTHER=0.000005
closeorder=0.0004575

"""导出数据"""
print("加载数据")
engine = create_engine('mysql+pymysql://root:mylove520@localhost/futures_1m?charset=utf8')
sql = 'SELECT * FROM `ih9999.ccfx`;'
df = pd.read_sql(sql,con=engine,index_col='Time')
if df is not None:
    print("数据成功导出")
df=df.loc[START_TIME:,TITLE_INFS]

"""计算数据"""
df['ema10'] = talib.EMA(df['close'],10)
df['ema20'] = talib.EMA(df['close'],20)
df['ema58'] = talib.EMA(df['close'],58)
df['ema100'] = talib.EMA(df['close'],100)
df['rsi'] = talib.RSI(df['close'],12)


"""调整坐标"""
cols=list(df)
cols.insert(1,cols.pop(cols.index('high')))
cols.insert(2,cols.pop(cols.index('low')))
df = df.loc[:,cols]

# 交易主策略
CallO_Time = []
CallO_Price = []
CallC_Time = []
CallC_Price = []
PutO_Time = []
PutO_Price = []
PutC_Time = []
PutC_Price = []
ccmoney = []
comoney=[]
index = 0  # 空仓
print(df.index)
for i in range(len(df.index)):
    price = df.close[i]
    if index == 0:
        if df.rsi[i] < 15:
            print(f"{df.rsi[i]}<15,满足条件")
            OrderTime = df.index[i]
            OrderPrice = price
            serviceCharge = OrderPrice * HAND * OTHER * 300

            dc = OrderTime.strftime("%Y-%m-%d %H:%M:%S")
            other = str(serviceCharge)
            date = str(np.float(OrderPrice))
            print("多单开仓：买开成交时间：" + dc + " 成交价格：" + date + " 开仓手数：" + str(HAND) + " 开仓手续费：" + other)

            comoney.append(serviceCharge)
            CallO_Time.append(OrderTime)
            CallO_Price.append(price)
            index = 1  # 多持仓
        elif df.rsi[i] > 85:
            OrderTime = df.index[i]
            OrderPrice = df.close[i]
            serviceCharge = OrderPrice * HAND * OTHER * 300
            dc = OrderTime.strftime("%Y-%m-%d %H:%M:%S")
            date = str(np.float(OrderPrice))
            other = str(serviceCharge)
            print("空单开仓：卖开成交时间：" + dc + " 成交价格：" + date + " 开仓手数：" + str(HAND) + " 开仓手续费：" + other)
            PutO_Time.append(OrderTime)
            PutO_Price.append(price)
            index = -1  # 空持仓
    elif index != 0:
            if index == 1:
                if OrderPrice - 5 >= price or OrderPrice + 15 <= price:
                    CoverTime = df.index[i]  # 空单平仓时间
                    CoverPirce = price  # 止损价格
                    # print(f"平仓价格{price}")
                    dc = CoverTime.strftime("%Y-%m-%d %H:%M:%S")
                    pricedata = str(np.float(CoverPirce))
                    CoverCharge = CoverPirce * HAND * closeorder * 300
                    other = str(CoverCharge)
                    print("多单平仓：卖平成交时间：" + dc + " 成交价格：" + pricedata + " 平仓手数：" + str(HAND) + " 平仓手续费：" + other)
                    if OrderPrice - 5 >= price:
                        print(f"固定止损价格：{OrderPrice - 5}>=现价：{price}")
                    elif OrderPrice + 15 <= price:
                        print(f"固定止盈价格：{OrderPrice + 15}<=现价：{price}")

                    #数据整合
                    ccmoney.append(CoverCharge)
                    CallC_Time.append(CoverTime) #获取平仓时间
                    CallC_Price.append(price)
                    index = 0
            elif index == -1:
                if OrderPrice + 5 <= price or OrderPrice - 15 >= price:
                    CoverTime = df.index[i]  # 空单平仓时间
                    CoverPirce = price  # 止损价格
                    dc = CoverTime.strftime("%Y-%m-%d %H:%M:%S")
                    pricedata = str(np.float(CoverPirce))
                    CoverCharge = CoverPirce * HAND * closeorder * 300
                    other = str(CoverCharge)
                    print("空单平仓：买平成交时间：" + dc + " 成交价格：" + pricedata + " 平仓手数：" + str(HAND) + " 平仓手续费：" + other)
                    if OrderPrice + 5 <= price:
                        print(f"满足条件固定止损价格：{OrderPrice - 5}>=现价：{price}")
                    elif OrderPrice - 15 >= price:
                        print(f"满足条件固定止盈价格：{OrderPrice + 15}<=现价：{price}")
                    PutC_Time.append(CoverTime)
                    PutC_Price.append(price)
                    index = 0

"""数据整合"""
df_new = pd.DataFrame(
    {'cotime':CallO_Time,'coprice':CallO_Price,'cctime':CallC_Time,'ccprice':CallC_Price,
     'tradehandS':HAND,'comoney':comoney,'ccmoney':ccmoney})
#print(df_new)



"""计算盈利结果"""
df_new['win/lost']=(df_new.ccprice-df_new.coprice)*300*5-df_new.comoney-df_new.ccmoney
print(df_new.sum())







#绘制行情图
add_plot = [
    mpf.make_addplot(df['ema100'],markersize=20,marker='V',color='r'),]
    #mpf.make_addplot(CallO_Time,scatter = True,markersize=20,marker='V',color='r')]
mpf.plot(df,type='candle', addplot=add_plot,volume=True)


plt.show()
