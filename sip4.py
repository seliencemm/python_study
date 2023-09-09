# coding:utf-8
import subprocess
import threading
import time

def run_sip_tools(userid, password, code):
    sip_tools_path = r"C:\Users\huangmengqing\Desktop\sip-tools\sip-tools.exe"
    file_path = r"C:\Users\huangmengqing\Desktop\sip-tools\input.16.wav"
    duration = "60"    #运行时长
    subprocess.call([sip_tools_path, userid, password, code, duration, file_path])

with open("data.txt", "r") as f:
    data = f.readlines()   # 总共100个账号
userids = []
passwords = []
codes = []

for line in data:
    userid, password, code = line.strip().split(",")
    userids.append(userid)
    passwords.append(password)
    codes.append(code)

threads = []

for i in range(0, 2):   # 首次启动10个账号
    thread = threading.Thread(target=run_sip_tools, args=(userids[i], passwords[i], codes[i]))
    thread.start()
    threads.append(thread)

for i in range(2, 14, 2):   # 每隔10分钟启动10个账号
    time.sleep(30)    # 等待10分钟
    for j in range(i, i+2):
        thread = threading.Thread(target=run_sip_tools, args=(userids[j], passwords[j], codes[j]))
        thread.start()
        threads.append(thread)

for thread in threads:
    thread.join()