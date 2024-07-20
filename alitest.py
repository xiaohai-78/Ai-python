import pandas as pd
import json

# 定义文件路径
file_path = r'D:\Documents\zhangben\alipay_record_20240719_2143_1.csv'

# 读取CSV文件，从第六行开始读取数据
data = pd.read_csv(file_path, encoding='gbk', sep=',', skiprows=4, on_bad_lines='skip')

# 忽略最后七行数据
data = data.iloc[:-7]

# 提取所需列并将每行数据放入一个对象内组成一个列表
data_list = []
total_expense = 0.0
total_income = 0.0
total_transfer = 0.0

# 创建字典来存储按counterparty分类的金额总和
expense_by_counterparty = {}
income_by_counterparty = {}
transfer_by_counterparty = {}

for _, row in data.iterrows():
    record = {
        'tradeId': row.iloc[0],          # 第一列 交易号
        'orderId': row.iloc[1],          # 第二列 商家订单
        'date': row.iloc[4],             # 第五列 最近修改时间
        'counterparty': row.iloc[7].strip(),     # 第八列 交易对方
        'productName': row.iloc[8].strip(),     # 第八列 商品名称
        'amount': float(row.iloc[9]),            # 第十列 金额
        'financialStatus': row.iloc[15].strip()           # 第15列 资金状态
    }
    data_list.append(record)

    # 根据资金状态累加总金额并按counterparty分类
    if record['financialStatus'] == '已支出':
        total_expense += record['amount']
        if record['counterparty'] in expense_by_counterparty:
            expense_by_counterparty[record['counterparty']] += record['amount']
        else:
            expense_by_counterparty[record['counterparty']] = record['amount']
    elif record['financialStatus'] == '已收入':
        total_income += record['amount']
        if record['counterparty'] in income_by_counterparty:
            income_by_counterparty[record['counterparty']] += record['amount']
        else:
            income_by_counterparty[record['counterparty']] = record['amount']
    elif record['financialStatus'] == '资金转移':
        total_transfer += record['amount']
        if record['counterparty'] in transfer_by_counterparty:
            transfer_by_counterparty[record['counterparty']] += record['amount']
        else:
            transfer_by_counterparty[record['counterparty']] = record['amount']

    # 获取总金额最高的3个分类
    top_expenses = sorted(expense_by_counterparty.items(), key=lambda x: x[1], reverse=True)[:3]
    top_incomes = sorted(income_by_counterparty.items(), key=lambda x: x[1], reverse=True)[:3]
    top_transfers = sorted(transfer_by_counterparty.items(), key=lambda x: x[1], reverse=True)[:3]

# 打印结果
print(json.dumps(data_list, ensure_ascii=False, indent=4))

print("===================================")

print(f"已支出: {total_expense:.2f}")
print(f"已收入: {total_income:.2f}")
print(f"资金转移: {total_transfer:.2f}")

print("===================================")

print("已支出中总金额最高的3个分类:")
for counterparty, amount in top_expenses:
    print(f"{counterparty}: {amount:.2f}")

print("===================================")

print("已收入中总金额最高的3个分类:")
for counterparty, amount in top_incomes:
    print(f"{counterparty}: {amount:.2f}")

print("===================================")

print("资金转移中总金额最高的3个分类:")
for counterparty, amount in top_transfers:
    print(f"{counterparty}: {amount:.2f}")