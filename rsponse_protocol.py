#定义函数生成相应格式的数据（拼接）
from config import  *
class ResponseProtocol(object):
    """服务器响应协议的格式化字符串"""

    @staticmethod
    def response_login_result(result,nickname,username):

      """生成用户登录结果的字符串
        result:为0表示登录失败，为1表示登录成功
        nickname：登录用户的昵称，登录失败为空
        username：登录用户的账号，登录失败为空
        result:供返回给用户的登录结果的结果字符串"""
     
      return DELIMITER.join([RESPONSE_LOGIN_RESULT, result, nickname, username])

    @staticmethod
    def response_chat(nickname, messages):
        """
        返回给用户的消息字符串
        :param nickname: 发送消息的用户昵称
        :param message: 消息正文
        :return: 返回给用户的消息字符串
        """

        return DELIMITER.join([RESPONSE_CHAT, nickname, messages])

