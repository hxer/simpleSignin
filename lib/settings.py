#!/usr/bin/env python3
# -*- coding: utf-8 -*-


PC_UA = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, '
         'like Gecko) Chrome/53.0.2785.57 Safari/537.36 OPR/40.0.2308.15')

MOBILE_UA = ('Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, '
             'like Gecko) Version/11.0 Mobile/15C114 Safari/604.1 ')

PROXIES = None

try:
    from lib.local_settings import *
except ImportError:
    pass