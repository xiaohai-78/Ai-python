import pandas as pd
import json

# 定义文件路径
file_path = r'D:\Documents\zhangben\alipay_record_20240719_2143_1.csv'

# 读取CSV文件，从第六行开始读取数据
data = pd.read_csv(file_path, encoding='gbk', sep=',', skiprows=5, on_bad_lines='skip')

# 忽略最后七行数据
data = data.iloc[:-7]

# 提取所需列并将每行数据放入一个对象内组成一个列表
data_list = []
for _, row in data.iterrows():
    record = {
        'tradeId': row.iloc[0],          # 第一列
        'orderId': row.iloc[1],          # 第二列
        'date': row.iloc[4],             # 第五列
        'counterparty': row.iloc[7],     # 第八列
        'productName': row.iloc[8],     # 第八列
        'amount': row.iloc[9]            # 第十列
    }
    data_list.append(record)

# print(data_list)

json_data = json.dumps(data_list, ensure_ascii=False, indent=4)

print(json_data)

# 计算总金额
# total_amount = sum(float(record['amount']) for record in data_list if pd.notna(record['amount']))

# print(f"Total amount: {total_amount:.2f}")
