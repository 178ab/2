import socket
from threading import Thread

import rsponse_protocol
from config import *
from serversocket import ServerSocket
from socket_wapper import socketwapper
from rsponse_protocol import *

class Server(object):
    """服务器核心类"""
    def __init__(self):
        """创建服务器套接字"""
        self.server_socket = ServerSocket()

        # 创建 请求的id和处理方法关联的 字典
        self.request_handle_function = {}

        self.register(REQUEST_LOGIN, self.request_login_handle())
        self.register(REQUEST_CHAT, self.request_chat_handle())

        # 创建 保存当前登录用户的信息 的字典
        self.clients = {}

    def register(self, request_id, handle_function):
        """注册 消息类型和处理函数 到字典里"""
        self.request_handle_function[request_id] = handle_function

    def startup(self):
        """获取客户端链接，并提供服务"""
        while True:
            """获取客户端链接"""
            soc, addr = self.server_socket.accept()

            """使用套接字生成包装对象"""
            client_soc = socketwapper(soc)

            # 收发数据

            Thread(target=lambda: self.request_handle(client_soc)).start()




    def request_handle(self, client_soc):
            """处理一个客户的请求"""
            while True:
                # 接受客户端数据
                recv_date = client_soc.recv_date()
                # 没接收到数据客户端关闭
                if not recv_date:
                    # 没有接收到数据客户端应该已经关闭
                    self.remove_offline_uers(client_soc)
                    client_soc.close()
                    break
                # 解析数据 返回的是字典
                parse_date = self.parse_request_text(recv_date)

                # 分析请求类型，并根据请求类型调用相应的处理函数

                handle_function = self.request_handle_function.get(parse_date['request_id'])
                if handle_function:
                    handle_function(client_soc, parse_date)





    def remove_offline_user(self, client_soc):
        """客户端下线的处理"""
        for username, info in self.clients.items():
            if info['sock'] == client_soc:
                del self.clients[username]
                break




    def parse_request_text(self, text):
        """解析客户端发送过来的信息
        登录信息：0001|username|password
        聊天信息：0002|username|messages"""
        request_list = text.split(DELIMITER)
        # 按照类型保存数据,字典
        request_date = {}
        request_date['request_id'] = request_date[0]
        if request_date['request_id'] == REQUEST_LOGIN:
            """用户请求登录"""
            request_date['username'] = request_list[1]
            request_date['password'] = request_list[2]

        elif request_date['request_id'] == REQUEST_CHAT:
            """用户发送聊天信息"""
            request_date['username'] = request_list[1]
            request_date['messages'] = request_list[2]

        return request_date

    def request_login_handle(self, client_soc, request_date):
         """处理登录功能"""
         # 获取账号密码
         username = request_date['username']
         password = request_date['passwird']

         # 检查是否登录成功
         ret,nickname,username = self.check_user_login(username,password)

         # 登录成功要保存客户套接字，昵称
         if ret == '1':
            self.clients[username] = {'sock':client_soc, 'nickname':nickname}

         # 拼接要返回给用户的信息

         response_text = ResponseProtocol.response_login_result(ret,nickname,username)

         # 把消息返回给用户
         client_soc.send._date(response_text)


    def check_user_login(self,username,password):
        """检查用户是否登录成功，并返回检查结果（0|失败，1|成功），昵称，用户名"""
        return 1, 'itcast1', 'user1'


    def request_chat_handle(self, client_soc, request_date):
         """处理聊天功能"""
         # 获取消息内容
         username = request_date['username']
         messages = request_date['messages']
         nickname = self.clients[username]['nickname']


         #拼接发送给用户的消息文本
         msg = rsponse_protocol.REQUEST_CHAT(nickname,messages)

         #转发消息给在线用户
         for username,info in self.clients.items():
             if info['sock'] == client_soc:        #不需要向发送消息的账号发送数据
                 continue
             info['sock'].send_date(msg)

if __name__ == '__main__':
    Server().startup()



























