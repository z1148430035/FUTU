from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

def Getbaipan(STOCK_CODE):

    bid_prices = []
    bid_vols = []
    bidOrder_number = []
    ask_prices = []
    ask_vols = []
    askOrder_number = []
    # 先订阅买卖摆盘类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
    ret_sub = quote_ctx.subscribe([STOCK_CODE], [SubType.ORDER_BOOK], subscribe_push=False)[0]
    if ret_sub == RET_OK:  # 订阅成功
        ret, data = quote_ctx.get_order_book(STOCK_CODE, num=10)  # 获取一次 10 档实时摆盘数据
        if ret == RET_OK:
            # 清洗买盘数据
            if len(bid_prices)==0:
                for bid_price, bid_vol, Order_number, y in data['Bid']:
                    bid_prices.append(bid_price)
                    bid_vols.append(bid_vol)
                    bidOrder_number.append(Order_number)
                    continue
                for ask_price, ask_vol, Order_number, y in data['Ask']:
                    ask_prices.append(ask_price)
                    ask_vols.append(ask_vol)
                    askOrder_number.append(Order_number)
                    continue
            elif len(bid_prices) == 10:
                for i in range(len(bid_prices)):
                    bid_prices[i]=data['Bid'][i][0]
                    bid_vols[i]=data['Bid'][i][1]
                    bidOrder_number[i]=data['Bid'][i][2]
                    ask_prices[i]=data['Ask'][i][0]
                    ask_vols[i]=data['Ask'][i][1]
                    askOrder_number[i]=data['Ask'][i][2]
                    continue
                # print(f"买1价格：{bid_prices[0]} 买1数量：{bid_vols[0]}")
                # print(f"卖1价格：{ask_prices[0]} 买1数量：{ask_vols[0]}")

            df = pd.DataFrame({'bid_price': bid_prices, 'bid_vol': bid_vols, 'bidOrder': bidOrder_number,
                           'ask_price': ask_prices, 'ask_vol': ask_vols, 'askOrder': askOrder_number})
            return df
        else:
            print('error:', data)
    else:
        print('subscription failed')