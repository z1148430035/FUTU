from futu import *


def Getwarrtant_Code(Stock_code):
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

    """设置导入数据"""
    ret, ls = quote_ctx.get_warrant(Stock_code, req)
    if ret == RET_OK:
        warrant_data_list, last_page, all_count = ls
        df = pd.DataFrame(data=warrant_data_list)
        df = df.loc[:, ["stock", "name", "issuer", "lot_size", "bid_price", "ask_price", "bid_vol", "ask_vol",
                        "delta", "strike_price", "conversion_ratio"]]
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

    """导出涡轮数据"""
    for i in range(len(df.index)):
        werrt_code.append(df.stock[i])
    return werrt_code

    """范例使用该函数"""
    # import get_warrtant_code as gwc 导入模组，把此文件放到一起
    # warrtant_code=gwc.Getwarrtant_Code('HK.00700') 输入代码，返回涡轮代码列表
    # print(warrtant_code)
