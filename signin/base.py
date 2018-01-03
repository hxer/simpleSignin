#!/usr/bin/env python3
# -*- coding: utf-8 -*-unicomapp.py

import requests

from lib.settings import UA


class Base(object):
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'User-Agent': UA
        }