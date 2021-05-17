# -*- coding:utf-8 -*-
"""
    __auth__: 孟德功
    __require__: QATool 登录验证

    调试飞书：https://open.feishu.cn/open-apis/authen/v1/user_auth_page_beta?
            app_id=cli_a0ef8b1a5279900e&
            redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Ftools%2Fuser
            &state=
"""
import requests
from tools.bin.models_user import get_user


class Access:
    def __init__(self, code):
        # 自定义信息
        self.APP_ID = 'cli_a0ef8b1a5279900e'                    # 飞书应用ID
        self.APP_SECRET = 'cCzZmY7ItXsaURawVT7zkdQJMdY6IV4J'    # 飞书应用秘钥

        # 固定信息
        self.URL = 'https://open.feishu.cn'
        self.TOKEN_URL = self.URL + '/open-apis/auth/v3/app_access_token/internal/'
        self.USER_URL = self.URL + '/connect/qrconnect/oauth2/access_token/'
        self.TOCKEN = self.get_access_token()
        self.code = code

    # 获取access token
    def get_access_token(self):
        try:
            params = dict()
            params['app_id'] = self.APP_ID
            params['app_secret'] = self.APP_SECRET
            app_access_token = requests.post(self.TOKEN_URL, json=params, headers=self.head()).json()
            return app_access_token['app_access_token']
        except Exception as e:
            print(e)
            return

    # 获取User Info
    def get_user_info(self):
        try:
            params = dict()
            params['app_id'] = self.APP_ID
            params['app_secret'] = self.APP_SECRET
            params['app_access_token'] = self.TOCKEN
            params['grant_type'] = 'authorization_code'
            params['code'] = self.code
            response = requests.post(self.USER_URL, json=params, headers=self.head()).json()
            return get_user(response)
        except Exception as e:
            print(e)
            return

    def head(self):
        return {"Content-Type": "application/json"}
