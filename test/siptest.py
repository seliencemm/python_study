# import subprocess
#
# sip_tools_path = r"C:\Users\huangmengqing\Desktop\sip-tools\sip-tools.exe"
# duration = "5"
# file_path = r"C:\Users\huangmengqing\Desktop\sip-tools\input.16.wav"
#
# subprocess.call(sip_tools_path + " 100000 100000 100000000 " + duration + file_path)

import subprocess

sip_tools_path = r"C:\Users\huangmengqing\Desktop\sip-tools\sip-tools.exe"
userid = "100000"
password = "100000"
code = "100000000"
duration = "5"
file_path = r"C:\Users\huangmengqing\Desktop\sip-tools\input.16.wav"

subprocess.call([sip_tools_path, userid, password, code, duration, file_path])








# import subprocess
#
# sip_tools_path = r"C:\Users\huangmengqing\Desktop\sip-tools\sip-tools.exe"
#
# userid = "100000"
# password = "100000"
# code = "100000000"
# duration = "5"
# file_path = r"C:\Users\huangmengqing\Desktop\sip-tools\input.16.wav"
#
# subprocess.call([sip_tools_path, "--user_id", userid, "--password", password, "--conference_id", code, "--duration", duration, "--wav_file", file_path])