#!/usr/bin/env python3
# -*- coding: utf-8 -*-


UA = ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, '
      'like Gecko) Chrome/53.0.2785.57 Safari/537.36 OPR/40.0.2308.15')

PROXIES = None

try:
    from lib.local_settings import *
except ImportError:
    pass