"""服务器相关配置"""
SERVER_IP = '192.168.0.17'
SERVER_PORT = 8090

#  数据协议相关配置
REQUEST_LOGIN = '0001' """登录请求"""
REQUEST_CHAT = '0002'  """聊天请求"""
RESPONSE_LOGIN_RESULT = '1001' """"登录请求"""
RESPONSE_CHAT = '1002' """聊天响应"""
DELIMITER = '|'  """自定义协议数据分隔符"""