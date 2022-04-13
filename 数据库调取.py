# 变量
company = '阿里巴巴'
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
sql = 'SELECT * FROM test WHERE company = %s'


cur.execute(sql,company)  # 执行SQL语句
data = cur.fetchall()#提取所有数据赋值给data
print(data)
for i in range(len(data)):
    print(data[i][1])


db.commit()  # 更新数据表
cur.close()
db.close()
