# coding: utf-8
import subprocess
import threading
#定义
def run_sip_tools(userid, password, code):

    sip_tools_path = r"C:\Users\huangmengqing\Desktop\sip-tools\sip-tools.exe"
    file_path = r"C:\Users\huangmengqing\Desktop\sip-tools\input.16.wav"
    duration = "5"

    subprocess.call([sip_tools_path, userid, password, code, duration, file_path])

userids = ["100000", "100001", "100002"]
passwords = ["100000", "100001", "100002"]
codes = ["100000000", "100000000", "100000000"]
threads = []

for userid, password, code, in zip(userids, passwords, codes):
    thread = threading.Thread(target=run_sip_tools, args=(userid, password, code))

    thread.start()

    threads.append(thread)

for thread in threads:
    thread.join()
