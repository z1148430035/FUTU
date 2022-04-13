# 变量
company = '吉利'
title = '测试标题'
href = '测试网站'
source = '测试来源'
date = '测试日期'

# 连接数据库
import pymysql

db = pymysql.connect(host='localhost', port=3306, user='root',
                     password='mylove520', database='pachong', charset='utf8')
# 插入数据
cur = db.cursor()  # 获取会话指针
sql = "INSERT INTO test(company,title,href,date,source) VALUES (%s,%s,%s,%s,%s)"


cur.execute(sql,(company,title,href,date,source),)  # 执行SQL语句
db.commit()  # 更新数据表
cur.close()
db.close()
