#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

from lib.settings import PC_UA


class Base(object):
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'User-Agent': PC_UA
        }