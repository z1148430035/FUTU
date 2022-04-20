"""设置导入库"""
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
STOCK_CODE='HK.00700'
pwd_unlock = '520131'


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
    index = 1
    ret,data = trd_ctx.place_order(price=warrt_Price,qty=10000,code=stock,
                                   trd_side=TrdSide.BUY,trd_env=TrdEnv.SIMULATE,acc_id=8116981)
    if ret == RET_OK:
        print(f"已成交：{data['order_id'][0]}")
"""主函数"""


while True:
    starttime = datetime.datetime.now()  # 计时
    df=Getbaipan(STOCK_CODE)

    """使用数据"""
    ask1_price = df.ask_price[0]    #获取卖一价格
    askVol = df.ask_vol[0]      #获取卖一量
    askVols=sum(df.ask_vol[1:])
    # print(f"卖1的总量为：{askVol/1000}k股")
    # print(f"卖2到卖5总量为{askVols/1000}k股")
    """预设卖1价格&预设卖1量"""
    Ask1_Price =362.2 #预设价格
    number_vol = 10 * 1000  # 预设卖1数据值
    index = 0 #空仓
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
            Warrtantcode = gwc.Getwarrtant_Code(STOCK_CODE)[0]

            df1=Getbaipan(Warrtantcode)
            warrt_Price=df1.ask_price[0]
            place_order(Warrtantcode)
            WIN=True
            break

while WIN:
    print(f"进入止盈止损策略，持仓代码{Warrtantcode}")
    break



    endtime=datetime.datetime.now()
    print(f"程序运行时间{endtime-starttime}")







trd_ctx.close() #关闭交易接口
quote_ctx.close()  # 关闭当条连接，OpenD 会在 1 分钟后自动取消相应股票相应类型的订阅
print("Trade over")