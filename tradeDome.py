"""设置导入库"""
import time

from futu import *
import pandas as pd
import datetime
import get_warrtant_code as gwc
from Market_baipan import Getbaipan

"""设置输出格式"""
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows',None)
# pd.set_option('display.width', 1000)
# pd.set_option('display.max_colwidth', 1000)

"""设置全局变量"""
STOCK_CODE = 'HK.00700'
pwd_unlock = '520131'
cut_price = []
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
    ret, data = trd_ctx.place_order(price=warrt_Price, qty=4000, code=stock,
                                    trd_side=TrdSide.BUY, trd_env=TrdEnv.SIMULATE, acc_id=8116981)
    if ret == RET_OK:
        ordersucess = True
        print(f"已成交：{data['order_id'][0]}")
        return ordersucess
    elif ret != RET_OK:
        ordersucess = False
        return ordersucess


"""止盈止损"""


def cut_order(stock):
    print("进入止盈止损程序")
    print(f"获取卖一价格是{warrt_bidprice[0]}")

    print(f"获取股票代码{Warrtantcode}")
    # unlockID()
    ret, data = trd_ctx.place_order(price=warrt_bidprice[0], qty=4000, code=stock,
                                    trd_side=TrdSide.SELL, trd_env=TrdEnv.SIMULATE, acc_id=8116981)
    if ret == RET_OK:
        cutsucess = True
        print(f"已成交 成交编号：{data['order_id'][0]}  成交价格：{data['price']} 成交时间{datetime.datetime.now()}")
        return cutsucess

    elif ret != RET_OK:
        cutsucess = False
        return cutsucess


"""主函数"""
TIME = True
CALLSIGE = False
ORDER = True
SCAN = True
while TIME:
    starttime = datetime.datetime.now()  # 计时
    """建立买卖盘锁定的数据列表"""
    callstock_askprice = [] #预设买涨买1价格
    callstock_askvol = []   #预设买涨的卖1挂单量

    stock_bidprice = []
    stock_bidvol = []

    ORDERSIOE = False   #下单程序关闭
    WIN = False #止损止盈默认关闭
    CutVol = [] #记录止损买1的挂单量
    while ORDER:
        print("""====================================""")
        print("开始执行下单策略")
        #默认关闭下单程序
        """寻找机会"""
        while SCAN:
            for i in range(0, 5):   #提取五档数据
                df = Getbaipan(STOCK_CODE)  #抓取摆盘

                """监控卖盘，发现做多机会"""
                aski_vol = df.ask_vol[i]        #提取整个盘面数据
                askiprice = df.ask_price[i]     #提取总合
                aski_sumvol = sum(df.ask_vol[(i + 1):(i + 3)])

                print(f"卖{i + 1}的价格是{df.ask_price[i]}  "
                      f"卖{i + 1}的挂单量：{df.ask_vol[i]} "
                      f"后面卖{i + 2}与卖{i + 4}挂单量的总合{aski_sumvol}")
                """扫描机器人"""
                if aski_vol >= 2 * aski_sumvol:     #进行扫描
                    print("发现机会")
                    callstock_askprice.append(askiprice)        #导入卖盘价格
                    callstock_askvol.append(aski_vol)           #导入卖盘数量
                    print(f"锁定价格{callstock_askprice[0]} 锁定监控量{callstock_askvol[0]} ")
                    print("______________________")
                    CALLSIGE=True   #触发预备下单参数
                    SCAN = False #关闭扫描器
                    ORDER = False
                    #time.sleep(1)

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
            #     startTreadvol = 0.3 * stock_bidvol[0]
            #     print(f"锁定价格{stock_bidprice[0]} 锁定监控量{stock_bidvol[0]} 设置触发30%买入挂单量 {startTreadvol}")
            #     print("______________________")
            #     time.sleep(3)

    """预先准备进行下单程序"""
    print("进入下单准备环节")
    while CALLSIGE:
        #time.sleep(2)
        df1 = Getbaipan(STOCK_CODE)     #获取股票摆盘数据
        Ask1_Price=callstock_askprice[0]    #获取预设价格
        startTreadvol = 0.3 * callstock_askvol[0]      #获取预设挂单量 系数30%
        ask1_price=df1.ask_price[0]     #获取当前股票摆盘数据
        ask1_vol=df1.ask_vol[0]         #获取当前股票摆盘数量
        x = df1['ask_price'] != Ask1_Price
        """检测价格不符合自动跳过"""
        if (x.iloc[:5].all() == False) == False:
            """清理所有缓存"""
            for i in range(len(callstock_askprice)):
                del callstock_askprice[i]
            for i in range(len(callstock_askvol)):
                del callstock_askprice[i]
            print("交易完成,清空缓存数据买1挂单量")
            time.sleep(2)
            break
        elif Ask1_Price == ask1_price:    #对比盘面数据
            """满足基本成交条件"""
            print(f"满足价格条件 预设价格：{Ask1_Price} 盘面价格{ask1_price} 满足价格条件 "
                  f"实时监控挂单量数据 预设数量:{startTreadvol} != 盘面挂单量:{df1.ask_vol[0]} ")
            if startTreadvol < ask1_vol:    #不满足预设信号
                #print(f"不满足触发买入条件:{startTreadvol} <= {ask1_vol}")
                #print("------------------------------")
                time.sleep(1)
                continue

            elif startTreadvol >= ask1_vol: #满足预设信号
                """满足条件下单"""

                print(f"1满足触发买入条件:{startTreadvol} >= {ask1_vol}")
                print("------------------------------")

                """下单涡轮"""
                Warrtantcode = gwc.Getwarrtant_Code(STOCK_CODE)[0]  # 涡轮代码唯一
                df2 = Getbaipan(Warrtantcode)   #获取涡轮摆盘数据
                warrt_Price = df2.ask_price[0]  #获取涡轮报价
                sucessorder = place_order(Warrtantcode) #下单程序

                if sucessorder == True:
                    cut_price = df2.bid_price[0]     #止损策略中的价格

                    """清理所有缓存"""
                    for i in range(len(CutVol)):    #清理下面的缓存
                        del CutVol[i]
                    for i in range(len(callstock_askprice)):
                        del callstock_askprice[i]
                    for i in range(len(callstock_askvol)):
                        del callstock_askprice[i]
                    print("交易完成,清空缓存数据买1挂单量")
                    CALLSIGE = False    #完成下单 关闭下单
                    ORDER = False       #关闭扫描
                    WIN = True         #触发真值
                    break
        elif Ask1_Price != ask1_price:
            print(f"不满足价格基本条件预设 价格：{Ask1_Price} 盘面价格{ask1_price} ")
    print("__________交易买入成功_____________")




    print("_________开始执行止损策略___________")
    while WIN:
        df_cutinfos = Getbaipan(STOCK_CODE)  # 获取标的摆盘数据
        """止损"""
        if cut_price >= df_cutinfos.bid_price[0]:
            print("进入止损准备状态")

            CutVol.append(0.6 * df_cutinfos.bid_vol[0])  # 读取当前满足条件下的买1的挂单量，添加至列表 设置系数
            print(f"读取添加正股买一挂单量{CutVol[0]}")
            # time.sleep(1)
            print("添加完成，进入循环")
            while CutVol[0] != 0:

                bid_vol1 = Getbaipan(STOCK_CODE).bid_vol[0]  # 读取买1的挂单量重复执行
                warrt_Pricecut = Getbaipan(Warrtantcode).bid_price[0]
                print(f"预设值={CutVol[0]} 买1挂单量：{bid_vol1} 止损价{cut_price} 止损标的{Warrtantcode} "
                      f"买入价格：{warrt_Price} 现价{warrt_Pricecut} p/l:{int((warrt_Pricecut - warrt_Price) * 4000)} HKD")
                # time.sleep(1)
                """止损策略"""
                if CutVol[0] >= bid_vol1:  # 对比成交量,如果触发量过小，进行止损
                    print(f"预设值={CutVol[0]} >=买1挂单量：{bid_vol1} 止损价{cut_price} 止损标的{Warrtantcode} "
                          f"买入价格：{warrt_Price} 现价{warrt_Pricecut} p/l:{int((warrt_Pricecut - warrt_Price) * 4000)} HKD")
                    warrt_bidprice = Getbaipan(Warrtantcode).bid_price  # 获取持仓涡轮代码\
                    cutsucs = cut_order(Warrtantcode)  # 下单执行
                    if cutsucs == True:
                        for i in range(len(CutVol)):
                            del CutVol[i]
                        print("交易完成,清空缓存数据买1挂单量")
                        ORDER = True
                        break
                """止盈策略"""

            break
    endtime = datetime.datetime.now()
    print(f"程序运行时间{endtime - starttime}")
    print("________完整交易____________")
    time.sleep(10)

trd_ctx.close()  # 关闭交易接口
quote_ctx.close()  # 关闭当条连接，OpenD 会在 1 分钟后自动取消相应股票相应类型的订阅
print("Trade over")