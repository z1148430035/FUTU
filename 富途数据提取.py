from futu import *
import pandas as pd
import csv


"""设置格式"""
pd.set_option('display.max_columns',1000)
pd.set_option('display.width',1000)
pd.set_option('display.max_colwidth',1000)


############################ 全局变量设置 ############################
FUTUOPEND_ADDRESS = '127.0.0.1'  # FutuOpenD 监听地址
FUTUOPEND_PORT = 11111  # FutuOpenD 监听端口
STOCK_CODE = 'HK.00388'     #设置股票代码
STRAT_DAY = '2022-04-01' #设置开始日期
END_DAY = '2022-04-01'   #设置结束日期
NUB=50
START=True
stocks_inf_1M = []
stocks_infs_1M=[]
i=[]
STOCKS_INF=[]
ret=[]
fileHeader = ["Stock_code","Time","Open","close","high","low","volume","turnover","channge_rate","lc"]

quote_context = OpenQuoteContext(host=FUTUOPEND_ADDRESS, port=FUTUOPEND_PORT)  # 行情对象


def GET_HISTROY():
    ret,data,page_req_key = quote_context.request_history_kline(
        STOCK_CODE,start=STRAT_DAY,end=END_DAY,ktype=KLType.K_1M,fields=KL_FIELD.ALL,
        max_count=NUB,)
    if ret == RET_OK:
        stoc_inf=data.values.tolist()
        stocks_inf_1M.append(stoc_inf)
    else:
        print('error:', data)
    while page_req_key != None:  # 请求后面的所有结果
        ret, data, page_req_key = quote_context.request_history_kline(
        STOCK_CODE,start=STRAT_DAY,end=END_DAY,ktype=KLType.K_1M,fields=KL_FIELD.ALL,
        max_count=NUB,page_req_key=page_req_key)
        # 请求翻页后的数据
        if ret == RET_OK:
            stoc_inf = data.values.tolist()
            stocks_inf_1M.append(stoc_inf)
        else:
            print('error:', data)

def stoks_1M():
    for ins in stocks_inf_1M:
        for code,time,open,close,high,low,x,y,volume,turnover,channge_rate,lc in ins:
            i.append(code)
            i.append(time)
            i.append(open)
            i.append(close)
            i.append(high)
            i.append(low)
            i.append(volume)
            i.append(turnover)
            i.append(channge_rate)
            i.append(lc)

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


def csc_work():
    csvFile =open(STOCK_CODE+".csv","w",newline="")
    writer =csv.writer(csvFile)
    writer.writerow(fileHeader)
    for i in ret:
        writer.writerow(i)

    csvFile.close()

#主函数
GET_HISTROY()
stoks_1M()
ret = list_of_groups(i, 10)
csc_work()


quote_context.close()
