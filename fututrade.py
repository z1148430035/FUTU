"""设置导入库"""
import time

from futu import *
import pandas as pd
import datetime
import get_warrtant_code as gwc
from  Market_baipan import Getbaipan

"""设置输出格式"""
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows',None)
# pd.set_option('display.width', 1000)
# pd.set_option('display.max_colwidth', 1000)

"""设置全局变量"""
STOCK_CODE='HK.00005'
pwd_unlock = '520131'
cut_price=[]
Warrtantcode = []

"""设置数据交易账户"""
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
trd_ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.HK, host='127.0.0.1', port=11111,
                              security_firm=SecurityFirm.FUTUSECURITIES)

# 先订阅买卖摆盘类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本

"""解锁账户"""
def unlockID():
    ret, data = trd_ctx.unlock_trade(pwd_unlock)
    if ret == RET_OK:
        print('解锁账户!')
    else:
        print('unlock_trade failed: ', data)


"""下单"""
def place_order(stock):
    print("进入下单程序")
    print(f"获取卖一价格是{warrt_Price}")
    print(f"获取股票代码{Warrtantcode}")
    unlockID()
    ret,data = trd_ctx.place_order(price=warrt_Price,qty=4000,code=stock,
                                   trd_side=TrdSide.BUY,trd_env=TrdEnv.SIMULATE,acc_id=8116981)
    if ret == RET_OK:
        ordersucess=True
        print(f"已成交：{data['order_id'][0]}")
        return ordersucess
    elif ret != RET_OK:
        ordersucess=False
        return ordersucess


"""止盈止损"""
def cut_order(stock):
    print("进入止盈止损程序")
    print(f"获取卖一价格是{warrt_bidprice[0]}")

    print(f"获取股票代码{Warrtantcode}")
    #unlockID()
    ret,data = trd_ctx.place_order(price=warrt_bidprice[0],qty=4000,code=stock,
                                   trd_side=TrdSide.SELL,trd_env=TrdEnv.SIMULATE,acc_id=8116981)
    if ret == RET_OK:
        cutsucess = True
        print(f"已成交 成交编号：{data['order_id'][0]}  成交价格：{data['price']} 成交时间{datetime.datetime.now()}")
        return cutsucess

    elif ret != RET_OK:
        cutsucess = False
        return cutsucess


"""主函数"""
TIME=True
ORDER=True
while TIME:
    starttime = datetime.datetime.now()  # 计时
    CutVol = []
    while ORDER:
        print("开始执行下单策略")
        df=Getbaipan(STOCK_CODE)

        """使用数据"""
        ask1_price = df.ask_price[0]    #获取卖一价格
        askVol = df.ask_vol[0]      #获取卖一量
        askVols=sum(df.ask_vol[1:])
        # print(f"卖1的总量为：{askVol/1000}k股")
        # print(f"卖2到卖5总量为{askVols/1000}k股")
        """预设卖1价格&预设卖1量"""
        Ask1_Price =ask1_price    #预设价格
        number_vol = 500 * 1000  # 预设卖1数据值







        """进行比较下单处理"""
        print(f"预设价格{Ask1_Price}=={ask1_price}")
        if Ask1_Price == ask1_price:
            if number_vol < askVol:
                print(f"不满足触发买入条件:{number_vol}<={askVol}")
                print("------------------------------")
                continue
            elif number_vol >= askVol:
                print(f"1满足触发买入条件:{number_vol}<={askVol}")
                print("------------------------------")
                Warrtantcode = gwc.Getwarrtant_Code(STOCK_CODE)[0]#涡轮代码唯一
                df1=Getbaipan(Warrtantcode)
                warrt_Price=df1.ask_price[0]
                sucessorder = place_order(Warrtantcode)
                if sucessorder == True:
                    cut_price=df.bid_price[0]
                    for i in range(len(CutVol)):
                        del CutVol[i]
                        print("清空缓存")
                    #time.sleep(1)
                    WIN=True
                    break
    print("__________交易买入成功_____________")
    print("_________开始执行止损策略___________")
    while WIN:
        df_cutinfos = Getbaipan(STOCK_CODE) #获取标的摆盘数据
        """止损"""
        if cut_price >= df_cutinfos.bid_price[0]:
            print("进入止损准备状态")

            CutVol.append(0.6*df_cutinfos.bid_vol[0])   #读取当前满足条件下的买1的挂单量，添加至列表 设置系数
            print(f"读取添加正股买一挂单量{CutVol[0]}")
            #time.sleep(1)
            print("添加完成，进入循环")
            while CutVol[0] != 0:

                bid_vol1 =Getbaipan(STOCK_CODE).bid_vol[0]   #读取买1的挂单量重复执行
                warrt_Pricecut = Getbaipan(Warrtantcode).bid_price[0]
                print(f"预设值={CutVol[0]} 买1挂单量：{bid_vol1} 止损价{cut_price} 止损标的{Warrtantcode} "
                      f"买入价格：{warrt_Price} 现价{warrt_Pricecut} p/l:{int((warrt_Pricecut - warrt_Price)*4000)} HKD")
                #time.sleep(1)
                """止损策略"""
                if CutVol[0] >= bid_vol1:       #对比成交量,如果触发量过小，进行止损
                    print(f"预设值={CutVol[0]} >=买1挂单量：{bid_vol1} 止损价{cut_price} 止损标的{Warrtantcode} "
                          f"买入价格：{warrt_Price} 现价{warrt_Pricecut} p/l:{int((warrt_Pricecut - warrt_Price)*4000)} HKD")
                    warrt_bidprice = Getbaipan(Warrtantcode).bid_price    #获取持仓涡轮代码\
                    cutsucs = cut_order(Warrtantcode)           #下单执行
                    if cutsucs ==True:
                        for i in range(len(CutVol)):
                            del CutVol[i]
                            print("")
                        print("交易完成,清空缓存数据买1挂单量")
                        ORDER=True
                        break
                """止盈策略"""

            break
    endtime=datetime.datetime.now()
    print(f"程序运行时间{endtime-starttime}")
    print("________完整交易____________")
    time.sleep(10)


trd_ctx.close() #关闭交易接口
quote_ctx.close()  # 关闭当条连接，OpenD 会在 1 分钟后自动取消相应股票相应类型的订阅
print("Trade over")