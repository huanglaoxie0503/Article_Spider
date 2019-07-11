# -*- coding: utf-8 -*-
import json
import requests


class YDMHttp(object):
    api_url = 'http://api.yundama.com/api.php'
    username = ''
    password = ''
    app_id = ''
    app_key = ''

    def __init__(self, username, password, appid, appkey):
        self.username = username
        self.password = password
        self.app_id = str(appid)
        self.app_key = appkey

    def balance(self):
        data = {'method': 'balance', 'username': self.username, 'password': self.password, 'appid': self.app_id, 'appkey': self.app_key}
        response_data = requests.post(self.api_url, data=data)
        ret_data = json.loads(response_data.text)
        if ret_data["ret"] == 0:
            print("获取剩余积分", ret_data["balance"])
            return ret_data["balance"]
        else:
            return None

    def login(self):
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.app_id, 'appkey': self.app_key}
        response_data = requests.post(self.api_url, data=data)
        ret_data = json.loads(response_data.text)
        if ret_data["ret"] == 0:
            print("登录成功", ret_data["uid"])
            return ret_data["uid"]
        else:
            return None

    def decode(self, filename, code_type, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.app_id, 'appkey': self.app_key, 'codetype': str(code_type), 'timeout': str(timeout)}
        files = {'file': open(filename, 'rb')}
        response_data = requests.post(self.api_url, files=files, data=data)
        ret_data = json.loads(response_data.text)
        if ret_data["ret"] == 0:
            print("识别成功", ret_data["text"])
            return ret_data["text"]
        else:
            return None


def ydm(file_path):
    username = 'da_ge_da1'
    # 密码
    password = 'da_ge_da'
    # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
    app_id = 3129
    # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
    app_key = '40d5ad41c047179fc797631e3b9c3025'
    # 图片文件
    filename = 'image/captcha.jpg'
    # 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
    code_type = 5000
    # 超时时间，秒
    timeout = 60
    # 检查

    yun_da_ma = YDMHttp(username, password, app_id, app_key)
    if username == 'username':
        print('请设置好相关参数再测试')
    else:
        # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
        return yun_da_ma.decode(file_path, code_type, timeout)


# if __name__ == "__main__":
#     # 用户名
#     username = 'da_ge_da1'
#     # 密码
#     password = 'da_ge_da'
#     # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
#     app_id = 3129
#     # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
#     app_key = '40d5ad41c047179fc797631e3b9c3025'
#     # 图片文件
#     filename = 'image/captcha.jpg'
#     # 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
#     code_type = 5000
#     # 超时时间，秒
#     timeout = 60
#     # 检查
#     if username == 'username':
#         print('请设置好相关参数再测试')
#     else:
#         # 初始化
#         yun_da_ma = YDMHttp(username, password, app_id, app_key)
#
#         # 登陆云打码
#         uid = yun_da_ma.login()
#         print('uid: %s' % uid)
#
#         # 登陆云打码
#         uid = yun_da_ma.login()
#         print('uid: %s' % uid)
#
#         # 查询余额
#         balance = yun_da_ma.balance()
#         print('balance: %s' % balance)
#
#         # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
#         text = yun_da_ma.decode(filename, code_type, timeout)
