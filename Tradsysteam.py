from futu import *

k = 1_000  # 定义数值
M = 10_00_000
stock_code = []
stocks_Bid_inf = []
stocks_Ask_inf = []
stock_Bidone = []
stock_Askone = []
stock_Bid_inf = {}
stock_Ask_inf = {}
stock_orde = {
    'stock_code': '',
    'stock_number': '',
    'stock_bidvol': '',
    'stock_askvol': ''
}
pwd_unlock = '520131'

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
trd_ctx = OpenSecTradeContext(
    filter_trdmarket=TrdMarket.HK,
    host='127.0.0.1', port=11111,
    security_firm=SecurityFirm.FUTUSECURITIES
)


def trade_acc():
    """获得账户"""
    ret, data = trd_ctx.get_acc_list()
    if ret == RET_OK:
        print(data['acc_id'])  # 取第一个账号
        print(data['sim_acc_type'])  # 转为 list
    else:
        print('get_acc_list error: ', data)


def First_unlcok_trade():
    """解锁账户"""
    ret, data = trd_ctx.unlock_trade(pwd_unlock)
    if ret == RET_OK:
        print('unlock success!')
    else:
        print('unlock_trade failed: ', data)


def get_moneynumber():
    """查询资金"""
    ret, data = trd_ctx.accinfo_query(
        trd_env=TrdEnv.SIMULATE, acc_id=8116981, acc_index=1, refresh_cache=False, currency=Currency.HKD)
    if ret == RET_OK:
        print(f"模拟账户账户余额为：{data['cash']} HKD")
    else:
        print('accinfo_query error: ', data)


def get_info_stockprice():
    """查询价格"""
    ret_sub = quote_ctx.subscribe(stock_code, [SubType.ORDER_BOOK], subscribe_push=False)[0]
    if ret_sub == RET_OK:  # 订阅成功
        ret, data = quote_ctx.get_order_book(stock_code, num=10)  # 获取一次 3 档实时摆盘数据
        if ret == RET_OK:
            for bid_inf in data['Bid']:
                stocks_Bid_inf.append(bid_inf)
            for ask_inf in data['Ask']:
                stocks_Ask_inf.append(ask_inf)
        else:
            print('error:', data)
    else:
        print('subscription failed')


def Trade_buy():
    """买入股票流程"""
    stock_Askone.append(stocks_Ask_inf[0])
    # 分别取出买一卖一的盘口数据
    for ask_price, vol, x, y in stock_Askone:
        stock_Ask_inf = {
            'ask_priceone': ask_price,
            'ask_vol1': vol,
        }
    # 提取卖一的价格和挂单
    ask_Price = stock_Ask_inf['ask_priceone']
    ret, data = trd_ctx.place_order(
        price=ask_Price, qty=stock_qty, code=stock_code, trd_side=TrdSide.BUY, trd_env=TrdEnv.SIMULATE, acc_id=8116981,
    )
    if ret == RET_OK:
        print(f"成功以{ask_Price}HKD 买入{stock_code} {stock_qty} 股")
    else:
        print('place_order erro:', data)


def Trade_sell():
    """卖出股票流程"""
    stock_Bidone.append(stocks_Bid_inf[0])
    # 分别取出买一卖一的盘口数据
    for bid_price, vol, x, y in stock_Bidone:
        stock_Bid_inf = {
            'bid_priceone': bid_price,
            'bid_vol1': vol,
        }
    bid_Price = stock_Bid_inf['bid_priceone']
    ret, data = trd_ctx.place_order(
        price=bid_Price, qty=stock_qty, code=stock_code, trd_side=TrdSide.SELL, trd_env=TrdEnv.SIMULATE, acc_id=8116981,
    )
    if ret == RET_OK:
        print(f"成功以{bid_Price}HKD 卖出{stock_code} {stock_qty} 股")
    else:
        print('place_order erro:', data)


# 主函数
print("Welcome to use")
trade_acc()
First_unlcok_trade()
get_moneynumber()

while True:
    stock_code = input("请输入以00000代码的股票代码:")
    stock_qty = input("请输入要交易的数量：")
    # stock_vol = input("请输入正股触发成交的量：")
    stock_side = input("请输入要买入的方向(buy/sell):")
    stock_side.lower()
    if stock_side == 'buy':
        get_info_stockprice()
        Trade_buy()
    elif stock_side == 'sell':
        get_info_stockprice()
        Trade_sell()
    elif stock_side == 'quit':
        break
trd_ctx.close()
quote_ctx.close()  # 关闭当条连接，OpenD 会在 1 分钟后自动取消相应股票相应类型的订阅
