#!/usr/bin/env python3
# encoding: utf-8
# author: Vincent
# refer: https://github.com/vc5

from lib.settings import PC_UA
from .common import Job

# 店铺签到列表
SHOPSIGN_LIST = ['https://mall.jd.com/shopSign-1000081124.html',
                 'https://mall.jd.com/shopSign-1000092704.html',
                 'https://mall.jd.com/shopSign-146935.html',
                 'https://mall.jd.com/shopSign-22705.html',
                 'https://mall.jd.com/shopSign-199094.html',
                 'https://mall.jd.com/shopSign-77222.html',
                 'https://mall.jd.com/shopSign-86174.html',
                 'https://mall.jd.com/shopSign-1000001582.html',
                 'https://mall.jd.com/shopSign-1000003179.html',
                 'https://mall.jd.com/shopSign-1000000725.html']


class ShopSign(Job):
    job_name = '店铺签到'
    ua = PC_UA
    index_url = 'https://mall.jd.com/shopSign-1000081124.html'
    login_url = index_url
    is_mobile = False

    def sign(self):
        for url in SHOPSIGN_LIST:
            r = self.session.get(url)
        return True
