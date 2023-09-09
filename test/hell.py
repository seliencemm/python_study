#coding:utf-8
# import random
#
# # 生成 100 个账号密码
# accounts = [(str(i), str(i)) for i in range(1, 101)]
#
# # 生成 10 个会议 ID
# meeting_ids = [str(i) for i in range(1000, 1010)]
# random.shuffle(meeting_ids)
#
# # 将账号、密码和会议 ID 写入文件
# with open("participants.txt", "w") as f:
#     for i in range(len(accounts)):
#         account, password = accounts[i]
#         meeting_id = meeting_ids[i // 10]  # 每个会议最多允许 10 个人进入
#         f.write(f"{account},{password},{meeting_id}\n")




"""
生成一个账号密码会议id的txt文件
"""
# with open("participants.txt", "w") as f:
#     for i in range(100000, 100100):
#         account = f"{i+1}"  # 账号是从 100001 到 100100
#         password = f"{i+1}"  # 密码与账号相同
#         meeting_id = f"{100000000 + ((i - 100000) // 10)}"  # 每个会议最多允许 10 个人进入
#         f.write(f"{account},{password},{meeting_id}\n")
with open("participants.txt", "w") as f:
    for i in range(100000, 100500):
        account = f"{i+1}"  # 账号是从 100001 到 100100
        password = f"{i+1}"  # 密码与账号相同
        meeting_id = f"{100000000 + ((i - 100000) // 10)}"  # 每个会议最多允许 10 个人进入
        f.write(f"{account},{password},{meeting_id}\n")


"""
比较两个文件是否一致
"""
# def compare_files(file1, file2):
#     with open(file1, "r") as f1, open(file2, "r") as f2:
#         content1 = f1.readlines()
#         content2 = f2.readlines()
#
#         if content1 == content2:
#             print(f"{file1} 和 {file2} 内容一致")
#         else:
#             print(f"{file1} 和 {file2} 内容不一致")
#             for i, (line1, line2) in enumerate(zip(content1, content2)):
#                 if line1 != line2:
#                     print(f"第 {i+1} 行不一致:")
#                     print(f"{file1}: {line1.strip()}")
#                     print(f"{file2}: {line2.strip()}")
#
# compare_files('participants.txt','data.txt')