import socket
#进行客服端与服务端的网络调试
if __name__ == '__main__':
    #创建套接字对象
    #AF_INET:代表的是创建的连接的ip地址类型为ipv4
    #SOCK_STREAM:表示tcp协议
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #与服务端创建连接
    #与服务端进行三次握手
    client_socket.connect(("35.74.61.68",5051))
    #与服务端进行信息交流
    client_data = "hello!服务端111".encode('utf-8')
    #发送信息给服务端
    client_socket.send(client_data)
    #打印发送的信息  此处的信息为十六进制加码
    print(client_data)
    #接收服务端的信息 1024表示服务端发送的信息最大为1024
    server_socket = client_socket.recv(1024)
    #进行解码为gbk类型
    print('服务端发送的信息：',server_socket.decode('gbk'))
    #关闭客服端
    client_socket.close()
