import sys

from window_login import WindowLogin
from request_protocol import RequestProtocol
from client_socket import ClientSocket
from threading import Thread
from client_config import *
from tkinter.messagebox import showinfo
from window_chat import WindowChat

class Client(object):
    def __init__(self):

        """初始化客户端资源"""
        # 初始化登录窗口
        self.window = WindowLogin()
        self.window.on_reset_button_click(self.clear_inputs)
        self.window.on_login_button_click(self.send_login_date)
        self.window.on_window_close(self.exit)

        # 初始化聊天窗口
        self.window_chat = WindowChat()
        self.window_chat.withdraw()       # 隐藏聊天窗口
        self.window_chat.on_send_button_click(self.send_chat_date)
        self.window_chat.on_window_close(self.exit)

        """创建客户端套接字"""
        self.conn = ClientSocket()

        # 初始化消息处理函数
        self.response_handle_function = {}
        self.register(RESPONSE_LOGIN_RESULT, self.response_logon_handle)
        self.register(RESPONSE_CHAT, self.response_chat_handle)

        # 保存在线用户名称
        self.username = None

        # 程序正在进行的标记
        self.is_runing = True
        
    def exit(self):
        """退出程序"""
        self.is_runing = False
        self.conn.close()
        sys.exit(0)   # 退出程序



    def register(self, request_id, handle_function):
        """注册消息和对应的方法到字典里"""
        self.response_handle_function[request_id] = handle_function


    def startup(self):
        """开启窗口"""
        self.conn.connect()
        Thread(target=self.response_handle).start()  # 创建并开启一个子线程接收来自服务器的数据
        self.window.mainloop()

    def clear_inputs(self):
        """清空窗口内容"""
        self.window.clear_username()
        self.window.clear_passwaord()

    def send_login_date(self):
        """将登录信息发送到服务器"""
        # 获取用户输入的账号和密码
        username = self.window.get_username()
        password = self.window.get_password()

        # 将信息生成相应格式
        request_date = RequestProtocol.request_login_result(username, password)

        # 发送协议到服务器

        self.conn.send_date(request_date)
        recv_date = self.conn.recv_date()
        print(recv_date)

        response_date= self.parse_response_date(recv_date)

        # 根据消息内容分别进行处理,将response_id和对应函数放在一个字典里

        handle_function = self.response_handle_function[response_date['response_id']]
        if handle_function:
            handle_function()


    def send_chat_date(self):
        """获取输入框内容，发送到服务器"""
        message = self.window_chat.get_input()
        self.window_chat.clear_input() # 清空输入框

        # 拼接发送的消息
        request_text = RequestProtocol.request_chat(self.username, message)

        # 发送消息到服务器
        self.conn.send_date(request_text)

        # 把消息显示到聊天区
        self.window_chat.append_message('我',message)



    def response_handle(self):
        """不断接收来自服务器的消息"""
        while self.is_runing:
            #
            recv_date = self.conn.recv_date()
            print('收到服务器的消息时：'+recv_date)

    @staticmethod
    def parse_response_date(recv_date):
        """
        登录的响应响应：1001|成功/失败|昵称|账号
        聊天的响应：1002|发送者的昵称|消息内容
        """
        # 使用协议定义的符号切割消息到列表
        response_date_list = recv_date.split(DELIMITER)

        # 解析消息的各个部分到字典
        response_date = dict()
        response_date['response_id'] = response_date_list[0]

        if response_date['response_id'] == RESPONSE_LOGIN_RESULT:
            # 登录结果的响应
            response_date['result'] = response_date_list[1]
            response_date['nickname'] = response_date_list[2]
            response_date['username'] = response_date_list[3]

        elif response_date['response_id'] == RESPONSE_CHAT:
            # 聊天响应的结果
            response_date['nickname'] = response_date_list[1]
            response_date['message'] = response_date_list[2]

        return response_date

    def response_logon_handle(self, response_date):
        """登录结果响应"""
        print("接收到的登录信息", response_date)
        result = response_date['result']
        if result == '0':
            showinfo('提示', '登录失败,账号或密码失败')  # 参数1，标题；参数2，提示内容
            print("登录失败")
            return
        # 登录成功获取用户信息
        showinfo('提示', '登录成功')
        nickname = response_date['nickname']
        self.username = response_date['username']   # 保存登录用户的账号，供发送消息使用

        # 显示聊天窗口，隐藏登录窗口
        self.window_chat.set_title(nickname)
        self.window_chat.deiconify()

        self.window.withdraw()

    def response_chat_handle(self, response_date):
        """聊天结果响应"""
        print('接收到的聊天信息：'+response_date)
        sender = response_date['nickname']
        message = response_date['message']
        self.window_chat.append_message(sender, message)

if __name__ == '__main__':
    client = Client()
    client.startup()




