import time
from  Market_baipan import Getbaipan
import pandas as pd

while True:
    ORDERSIOE = False
    STOCK_CODE = 'HK.00388'
    stock_askprice=[]
    stock_askvol=[]
    stock_bidprice = []
    stock_bidvol = []
    for i in range(0,5):
        df = Getbaipan(STOCK_CODE)
        """监控卖盘，发现做多机会"""
        aski_vol = df.ask_vol[i]
        askiprice= df.ask_price[i]
        aski_sumvol =sum(df.ask_vol[(i+1):(i+3)])
        print(f"卖{i+1}的价格是{df.ask_price[i]}  "
              f"卖{i+1}的挂单量：{df.ask_vol[i]} "
              f"后面卖{i+2}与卖{i+4}挂单量的总合{aski_sumvol}")
        if aski_vol >= 2*aski_sumvol:
            print("发现机会")
            stock_askprice.append(askiprice)
            stock_askvol.append(aski_vol)
            startTreadvol=0.3*stock_askvol[0]
            print(f"锁定价格{stock_askprice[0]} 锁定监控量{stock_askvol[0]} 设置触发30%买入挂单量{startTreadvol} ")
            print("______________________")
            time.sleep(2)
            ORDERSIOE=True

    while ORDERSIOE:
        print("=======================")
        print("进入下单程序")
        df1 = Getbaipan(STOCK_CODE)  # 获取股票摆盘数据
        Ask1_Price = stock_askprice[0]  # 提前寻找的价格机会
        ask1_price = df1.ask_price[0]  # 获取预设价格
        ask1_vol = df1.ask_vol[0]  # 获取预设数据
        x = df['ask_price'] != Ask1_Price
        print(f"实施监控数据{stock_askprice[0]}  股票 {STOCK_CODE}:卖1价格{df1.ask_price[0]}")
        if Ask1_Price == ask1_price:  # 对比盘面数据
            """满足基本成交条件"""
            print("满足价格相等条件")
            if startTreadvol < ask1_vol:  # 不满足预设信号
                print(f"不满足触发买入条件:{startTreadvol}<={ask1_vol}")
                print("------------------------------")
                continue
        if (x.iloc[:5].all()==False) == False:
            for i in range(len(stock_askprice)):
                del stock_askprice[i]
            for i in range(len(stock_askvol)):
                del stock_askprice[i]
            print("交易完成,清空缓存数据买1挂单量")
            break



        """监控买盘，发现做空机会"""
        # bidi_vol = df.bid_vol[i]
        # bidiprice = df.bid_price[i]
        # bidi_sumvol = sum(df.bid_vol[(i + 1):(i + 3)])
        # print(f"买{i + 1}的价格是{df.bid_price[i]}  "
        #       f"买{i + 1}的挂单量：{df.bid_vol[i]} "
        #       f"后面买{i + 2}与买{i + 4}挂单量的总合{aski_sumvol}")
        # if bidi_vol >= 3 * bidi_sumvol:
        #     print("发现机会")
        #     stock_bidprice.append(bidiprice)
        #     stock_bidvol.append(bidi_vol)
        #     startTreadvol=0.3*stock_bidvol[0]
        #     print(f"锁定价格{stock_bidprice[0]} 锁定监控量{stock_bidvol[0]} 设置触发30%买入挂单量 {startTreadvol}")
        #     print("______________________")
        #     time.sleep(3)