from futu import *
import pandas as pd
from sqlalchemy import create_engine

"""设置格式"""
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows',None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

############################ 全局变量设置 ############################
FUTUOPEND_ADDRESS = '127.0.0.1'  # FutuOpenD 监听地址
FUTUOPEND_PORT = 11111  # FutuOpenD 监听端口
STOCK_CODE = []  # 设置股票代码
STRAT_DAY = '2012-04-13'  # 设置开始日期
END_DAY = '2022-04-13'  # 设置结束日期
NUB = 50
stocks_inf_1M = []
stock = []
inof = []

quote_context = OpenQuoteContext(host=FUTUOPEND_ADDRESS, port=FUTUOPEND_PORT)  # 行情对象


def GET_HISTROY():
    ret, data, page_req_key = quote_context.request_history_kline(
        STOCK_CODE, start=STRAT_DAY, end=END_DAY, ktype=KLType.K_DAY, fields=KL_FIELD.ALL,
        max_count=NUB, )
    if ret == RET_OK:
        stoc_inf = data.values.tolist()
        stocks_inf_1M.append(stoc_inf)
    else:
        print('error:', data)
    while page_req_key != None:  # 请求后面的所有结果
        ret, data, page_req_key = quote_context.request_history_kline(
            STOCK_CODE, start=STRAT_DAY, end=END_DAY, ktype=KLType.K_DAY, fields=KL_FIELD.ALL,
            max_count=NUB, page_req_key=page_req_key)
        # 请求翻页后的数据
        if ret == RET_OK:
            stoc_inf = data.values.tolist()
            stocks_inf_1M.append(stoc_inf)
        else:
            print('error:', data)


def stoks_1M():
    for ins in stocks_inf_1M:
        for code, time, open, close, high, low, x, y, volume, turnover, channge_rate, lc in ins:
            stock.append(time)
            stock.append(open)
            stock.append(close)
            stock.append(high)
            stock.append(low)
            stock.append(volume)
            stock.append(turnover)
            stock.append(channge_rate)
            stock.append(lc)


def list_of_groups(list_info, per_list_len):
    '''
    :param list_info:   列表
    :param per_list_len:  每个小列表的长度
    :return:
    '''
    list_of_group = zip(*(iter(list_info),) * per_list_len)
    end_list = [list(i) for i in list_of_group]  # i is a tuple
    count = len(list_info) % per_list_len
    end_list.append(list_info[-count:]) if count != 0 else end_list
    return end_list
def go_tosql():
    df = pd.DataFrame(data=inof, )
    df.columns = ['Time', 'OPEN', 'CLOSE', 'HIGH', 'LOW', 'VOLUME', 'TURNOVER', 'change_rate', 'lc']
    engine = create_engine('mysql+pymysql://root:mylove520@localhost/stocks_day?charset=utf8')
    df.to_sql(name=STOCK_CODE, con=engine, if_exists='replace', index=True)
"""导入股票代码"""
cs=[]
df=pd.read_csv('stocks.csv')
df.columns=['stocks_code']
for i in df['stocks_code']:
    cs.append(i)

for ic in cs:
    STOCK_CODE=ic
    GET_HISTROY()
    stoks_1M()
    inof = list_of_groups(stock, 9)
    go_tosql()



"""提取数据"""




quote_context.close()
