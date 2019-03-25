#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from base64 import b64encode
from signin.base import Base
from lib.settings import PROXIES
from lib.clipher import rsa_encrypt
from lib.utils import pad_randomstr


PUB_KEY = ('-----BEGIN PUBLIC KEY-----\n'
           'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6'
           'FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9'
           'NPhQo07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0Srctg'
           'aqGfLgKvZHOnwTjyNqjBUxzMeQlEC2czEMSwIDAQAB\n'
           '-----END PUBLIC KEY-----')


class UnicomApp(Base):
    def __init__(self):
        super().__init__()
        self.headers['User-Agent'] = 'Mozilla/5.0 (Linux; Android 6.0; XXX-X00 Build/XXX-X00; wv)'

    def login(self, username, password):
        """
        :param username: phone number
        :param password: 6 numbers
        :return: True or False
        """
        login_url = 'http://m.client.10010.com/mobileService/login.htm'

        username = b64encode(rsa_encrypt(PUB_KEY, pad_randomstr(username, size=6)))
        password = b64encode(rsa_encrypt(PUB_KEY, pad_randomstr(password, size=6)))
        data = {
            'deviceOS': 'android6.0',
            'mobile': username,
            'netWay': 'WIFI',
            'deviceCode': '000000000000000',
            'isRemberPwd': 'true',
            'version': 'android@5.61',
            'deviceId': '000000000000000',
            'password': password,
            'keyVersion': '',
            'provinceChanel': 'general',
            'deviceModel': 'Custom Phone',
            'deviceBrand': 'unknown',
            'appId': 'a49a95f4eacb381ffaa88f86edb3ddb891c8357a5de83d951b720fbd46d989fa',
            'pip': '',
            'pushPlatform': '',
            'platformToken': '',
            'timestamp': time.strftime("%Y%m%d%H%M%S", time.localtime()),
        }
        resp = self.session.post(login_url, data=data, headers=self.headers, proxies=PROXIES)
        if resp.status_code == 200:
            resp = resp.json()
            if resp.get('code') == "0":
                return True
        return False

    def signin(self):
        # login, then get token
        token = self.session.cookies.get('a_token', '')
        query_url = 'https://act.10010.com/SigninApp/signin/querySigninActivity.htm'
        params = {
            'token': token
        }
        self.session.get(query_url, params=params, headers=self.headers, proxies=PROXIES)
        signin_url = 'https://act.10010.com/SigninApp/signin/daySign.do'
        data = {
            'className': 'btnPouplePost'
        }
        self.session.post(signin_url, data=data, headers=self.headers, proxies=PROXIES)
        final_url = 'http://m.client.10010.com/SigninApp/signin/goldTotal.do'
        self.session.post(final_url, headers=self.headers, proxies=PROXIES)
        return True
