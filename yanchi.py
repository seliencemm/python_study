# coding: utf-8

"""写入TXT文件"""
# import re
#
# # 打开原始文本文件
# with open('yanchi_data', 'r') as file:
#     content = file.read()
#
# # 定义正则表达式模式
# pattern = r'delay:(\d+ms)'
#
# # 使用正则表达式匹配数据
# matches = re.findall(pattern, content)
#
# # 打开新的目标文本文件
# with open('delay_data.txt', 'w') as file:
#     # 将匹配到的数据写入文件
#     for match in matches:
#         file.write(match + '\n')

"""写入Excel文件"""
import re
import pandas as pd
import openpyxl

# 打开原始文本文件
with open('yanchi_data', 'r') as file:
    content = file.read()

# 定义正则表达式模式
pattern = r'delay:(\d+ms)'

# 使用正则表达式匹配数据
matches = re.findall(pattern, content)

# 创建 DataFrame 对象
df = pd.DataFrame(matches, columns=['Delay'])

# 将数据写入 Excel 文件
df.to_excel('output.xlsx', index=False)