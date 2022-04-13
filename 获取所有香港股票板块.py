from futu import *
import pandas as pd


date=[]


"""数据结构"""
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows',None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

"""数据接口"""
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

"""数据返回"""
ret, data = quote_ctx.get_plate_list(Market.HK, Plate.CONCEPT)
if ret == RET_OK:
    date=data
else:
    print('error:', data)
quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽

df = pd.DataFrame(data=date)
df.to_csv('BANkuai.csv',encoding="utf_8_sig")
print(df)
