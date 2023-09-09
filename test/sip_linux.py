# coding: utf-8
import subprocess
import multiprocessing

def run_sip_tools(userid, password, code):
    sip_tools_path = "/home/workspace/sip/sip-tools.exe"
    file_path = "/home/workspace/sip/input.16.wav"
    duration = "5"
    subprocess.call([sip_tools_path, userid, password, code, duration, file_path])

# 从数据文件中读取数据
with open("/home/workspace/data.txt", "r") as f:
    data = f.readlines()[:2]
    print(data)

# 解析数据
userids = []
passwords = []
codes = []
for line in data:
    userid, password, code = line.strip().split(",")
    userids.append(userid)
    passwords.append(password)
    codes.append(code)
#
# 启动进程
processes = []
for userid, password, code in zip(userids, passwords, codes):
    process = multiprocessing.Process(target=run_sip_tools, args=(userid, password, code))
    process.start()
    processes.append(process)

# 等待所有进程完成
for process in processes:
    process.join()