import socket
from client_config import *

class ClientSocket(socket.socket):
    """客户端套接字的自定义"""

    def __init__(self):
        """设置为 TCP 套接字"""
        super(ClientSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """自动连接到服务器"""
        super(ClientSocket, self).connect((SERVER_IP, SERVER_PORT))

    def recv_date(self):
        """接收数据，并自动转化为字符串返回"""
        return self.recv(512).decode('utf-8')

    def send_date(self, messages):
        """接收字符串，自动转化为字节数发送"""
        self.send(messages.encode('utf-8'))














