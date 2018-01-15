#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""
import random


def pad_randomstr(text, size=6):
    chars = '0123456789'
    randstr = ''.join(random.choice(chars) for _ in range(size))
    if isinstance(text, bytes):
        text = str(text, 'utf-8')
    return '{0}{1}'.format(text, randstr)


def proxy_patch():
    """
    Requests 似乎不能使用系统的证书系统, 方便起见, 不验证 HTTPS 证书, 便于使用代理工具进行网络调试...
    http://docs.python-requests.org/en/master/user/advanced/#ca-certificates
    """
    import warnings
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    class XSession(requests.Session):
        def __init__(self):
            super().__init__()
            self.verify = False

    requests.Session = XSession
    warnings.simplefilter('ignore', InsecureRequestWarning)

