"""设置导入库"""
from futu import *
import pandas as pd
import time

"""设置输出格式"""
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows',None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)


"""设置全局变量"""
bid_prices=[]
bid_vols = []
bidOrder_number=[]
ask_prices=[]
ask_vols = []
askOrder_number=[]
STOCK_CODE='HK.00700'
NUM=10
pwd_unlock = '520131'


"""设置数据交易账户"""
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
trd_ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.HK, host='127.0.0.1', port=11111, security_firm=SecurityFirm.FUTUSECURITIES)



ret_sub = quote_ctx.subscribe([STOCK_CODE], [SubType.ORDER_BOOK], subscribe_push=False)[0]
# 先订阅买卖摆盘类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本


def Getdate():
    if ret_sub == RET_OK:  # 订阅成功
        ret, data = quote_ctx.get_order_book(STOCK_CODE, num=NUM)  # 获取一次 3 档实时摆盘数据
        if ret == RET_OK:
            #清洗买盘数据
            for bid_price,bid_vol,Order_number,y in data['Bid']:
                bid_prices.append(bid_price)
                bid_vols.append(bid_vol)
                bidOrder_number.append(Order_number)
            #清洗卖盘数据
            for ask_price,ask_vol,Order_number,y in data['Ask']:
                ask_prices.append(ask_price)
                ask_vols.append(ask_vol)
                askOrder_number.append(Order_number)
        else:
            print('error:', data)
    else:
        print('subscription failed')
def unlockID():
    ret, data = trd_ctx.unlock_trade(pwd_unlock)
    if ret == RET_OK:
        print('unlock success!')
    else:
        print('unlock_trade failed: ', data)
def place_order():
    ret,data = trd_ctx.place_order(
        price=df.ask_price,qty=100,code=STOCK_CODE,trd_side=TrdSide.BUY,trd_env=TrdEnv.SIMULATE,time_in_force='GTC')
    if ret == RET_OK:
        print(f"已成交：{data['dealt_qty']}")
"""主函数"""
unlockID()
while True:

    Getdate()
    df = pd.DataFrame({'bid_price': bid_prices, 'bid_vol': bid_vols, 'bidOrder': bidOrder_number,
                       'ask_price': ask_prices, 'ask_vol': ask_vols, 'askOrder': askOrder_number})

    askVol = df.ask_vol[0]      #获取卖一量
    askVols=sum(df.ask_vol[1:])
    print(askVols)
    number_vol = 10*1000
    while   askVol >= 4*askVols:
        Vol1=askVol
        if Vol1 >= df.ask_vol[0]:
            print("下单")
            place_order()
    if number_vol < askVol:
        print(df)
        print(f"不满足触发买入条件 设置的量小于卖一数量:{number_vol}<={askVol}")
        print("------------------------------")
    elif number_vol >= askVol:
        print(df)
        print(f"满足触发买入条件{number_vol}<={askVol}")
        print("------------------------------")
    time.sleep(5)





trd_ctx.close() #关闭交易接口
quote_ctx.close()  # 关闭当条连接，OpenD 会在 1 分钟后自动取消相应股票相应类型的订阅
print("Trade over")