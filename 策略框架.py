import time

Bsk1_Price =362.2 #预设价格
number_vol = 10 * 1000  # 预设卖1数据值

BSK=362.4
vol=50 * 1000
win=True
wartbuy=0.123
wartBid=0.140
chat=True
win=False
"""开仓"""
while True:#设定交易时间
    while chat:
        print("进行下单")
        win =True
        time.sleep(2)
        break

    """止盈止损"""
    while win:
        if Bsk1_Price == BSK:
            print("止损")
            chat=True
            time.sleep(2)
            break
        elif (wartBid-wartbuy) >= 0.006:
            print("止盈")
            chat=True
            time.sleep(2)
            break