# coding: utf-8
import yaml
import re

# 读取YAML文件
with open('eng.yml', 'r') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

# 正则表达式匹配括号内的值
pattern = r'\((.*?)\)'

# 遍历每个项并找到带括号的"value"行
for item in data:
    if 'value' in item:
        value = item['value']
        matches = re.findall(pattern, value)
        if len(matches) > 0:
            print(matches[0])