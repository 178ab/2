
class socketwapper(object):
    """套接字包装类（套接字的功能包装）"""

    def __init__(self, sock):
        self.sock = sock

        def recv_date(self):
            # 接受数据并解码为字符串
            try:
                return self.sock.recv(512).decode('utf-8')
            except:
                return ""

        def send_date(self, messages):
            return self.sock.send(messages.encode('utf-8'))
        def close(self):
            """关闭套接字"""
            self.sock.close()