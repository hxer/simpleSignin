#!/usr/bin/env python
# encoding: utf-8
# author: Vincent
# refer: https://github.com/vc5

import json
import re
import time

from selenium.common.exceptions import WebDriverException

from .common import Job

WIDTH = 480
HEIGHT = 800
PIXEL_RATIO = 3.0
jdstock_Emulation = {"deviceMetrics": {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO},
                     "userAgent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C153 JDStockApp_iOS_2.0.0 jdstock-iphone_2.0.0 JDStockApp_iOS_1.6.0'}


class JDStock_Sign(Job):
    job_name = '京东股票翻牌'
    index_url = 'https://active.jd.com/forever/stockSign/html/index.html'
    sign_url = 'https://gpm.jd.com/signin/choice'
    home_url = 'https://gpm.jd.com/signin/home'
   
    def is_signed(self):
        self.session.headers.update({'Referer': 'https://active.jd.com/forever/stockSign/html/index.html'})

        return False

    def sign(self):
        isSucces = False
        timestamp = str(int(time.time() * 1000))
        self.sid = self.session.cookies.get('sid')
        p = {'sid': self.sid,
             '_': timestamp,
             'position': 1,
             'callback': 'Zepto' + timestamp
             }
        r = self.session.get(self.sign_url, params=p)
        res = re.findall(r'\[.*?\]', r.text)[0]
        j = json.loads(res)
        isSucces = j[0]['success']
        return isSucces

    def sign1(self):
        self.session._driver = None
        # self.session.webdriver_options.set_headless()
        self.session.webdriver_options.add_experimental_option("mobileEmulation", jdstock_Emulation)
        driver = self.session.driver
        driver.get('https://active.jd.com/forever/stockSign/html/index.html?appVersion=2.0.0')
        try:
            self.session.transfer_session_cookies_to_driver()
        except WebDriverException:
            pass
        driver.get('https://active.jd.com/forever/stockSign/html/index.html?appVersion=2.0.0')
