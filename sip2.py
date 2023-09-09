# coding: utf-8
import subprocess
import threading
import time

def run_sip_tools(userid, password, code):

    sip_tools_path = r"C:\Users\huangmengqing\Desktop\sip-tools\sip-tools.exe"
    file_path = r"C:\Users\huangmengqing\Desktop\sip-tools\input.16.wav"
    duration = "100"    #运行时长
    ip = "47.106.127.160:5166"
    subprocess.call([sip_tools_path, ip,userid, password, code, duration, file_path])

with open("data.txt", "r") as f:

    data = f.readlines()[:50]     #启动个数

userids = []
passwords = []
codes = []

for line in data:
    userid, password, code = line.strip().split(",")
    userids.append(userid)
    passwords.append(password)
    codes.append(code)

threads = []

for userid, password, code, in zip(userids, passwords, codes):
    time.sleep(0.1)
    thread = threading.Thread(target=run_sip_tools, args=(userid, password, code))

    thread.start()

    threads.append(thread)

for thread in threads:
    thread.join()