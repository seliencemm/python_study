# coding: utf-8

import subprocess
import threading
import time

def run_sip_tools(userid, password, code):
    sip_tools_path = r"C:\Users\huangmengqing\Desktop\sip-tools\sip-tools.exe"
    file_path = r"C:\Users\huangmengqing\Desktop\sip-tools\input.16.wav"
    duration = "60"
    subprocess.call([sip_tools_path, userid, password, code, duration, file_path])

# 从数据文件中读取数据
with open("../data.txt", "r") as f:
    data = f.readlines()

# 初始的账号数量
num_accounts = 2

# 每次增加的账号数量
increment = 2

# 总共要创建的账号数量
total_accounts = 10

# 启动线程
threads = []

while num_accounts <= total_accounts:
    # 解析数据
    userids = []
    passwords = []
    codes = []

    for line in data[:num_accounts]:
        userid, password, code = line.strip().split(",")
        userids.append(userid)
        passwords.append(password)
        codes.append(code)

    for userid, password, code in zip(userids, passwords, codes):
        thread = threading.Thread(target=run_sip_tools, args=(userid, password, code))
        thread.start()
        threads.append(thread)

    # 增加账号数量
    num_accounts += increment

    # 每次启动线程后等待时间
    time.sleep(60)

for thread in threads:
    thread.join()