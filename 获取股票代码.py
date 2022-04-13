from futu import *
import pandas as pd
import time
date=[]



"""设置格式"""
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows',None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)


"""接口"""
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

"""连接数据"""


df=pd.DataFrame(data=pd.read_csv('BANkuai.csv'))
for i in df['code']:
    ret, data = quote_ctx.get_plate_stock(i)
    if ret == RET_OK:
        date.append(data['code'])
        print(f"已经获取{i}数据，请稍等3秒")
        time.sleep(3.01)
    else:
        print('error:', data)
df=pd.DataFrame(data=date)
df.to_csv("stocks_name.csv")
print("运行完成")
quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽
