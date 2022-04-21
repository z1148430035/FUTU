from futu import *



import pandas as pd
"""自动筛选最优5个涡轮"""

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
"""设置输出格式"""
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

"""设置全局函数"""
req = WarrantRequest()
req.sort_field = SortField.STRIKE_PRICE
req.issuer_list = ['SG', 'BP', 'CS', 'HS', 'UB', 'HT', 'MS', 'GJ']
req.ascend = False
req.type_list = ['CALL']
req.status = WarrantStatus.NORMAL
req.cur_price_max = 0.24
req.cur_price_min = 0.05
werrt_code = []
werrt_size=[]

"""设置导入数据"""
ret, ls = quote_ctx.get_warrant('HK.00005', req)
if ret == RET_OK:
    warrant_data_list, last_page, all_count = ls
    df = pd.DataFrame(data=warrant_data_list)
    df = df.loc[:, ["stock", "name", "issuer", "lot_size", "bid_price", "ask_price", "bid_vol", "ask_vol",
                    "delta", "strike_price", "conversion_ratio","lot_size"]]
else:
    print('error: ', ls)

quote_ctx.close()
"""计算敏感度"""
df["min"] = (0.2 * df.delta) / (0.001 * df.conversion_ratio)

"""排序数据"""
df = df.sort_values(by=["min"], ascending=False, axis=0)
df = df[(df.ask_price - df.bid_price) <= 0.003]
df.index = range(len(df.index))  # 重新排序序号
df = df[:5]

print(df)
"""导出涡轮数据"""
for i in range(0,5):
    werrt_code.append(df.stock[i])

print( type(df.lot_size))
print(werrt_code)