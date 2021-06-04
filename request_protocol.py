from client_config import *

class RequestProtocol(object):

    @staticmethod
    def request_login_result(username, password):
        """0001|user1|11111    类型|账号|密码"""
        return DELIMITER.join([REQUEST_LOGIN, username, password])

    def request_chat(self, username, messages):
        """0002|user1|msg  类型|账号|消息"""
        return DELIMITER.join([REQUEST_CHAT, username, messages])

