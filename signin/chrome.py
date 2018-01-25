#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
import time
from pathlib import Path
from urllib.parse import urlparse

from requestium import Session
from requestium.requestium import RequestiumChrome
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException

# mobileEmulation = {"deviceMetrics": {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO}, "userAgent": UA}
mobile_emulation = {'deviceName': 'iPhone 6'}


class MobileChrome:
    WIDTH = 480
    HEIGHT = 800
    UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C114 Safari/604.1'

    def __init__(self, signbot):
        self.bot = signbot
        self.user = signbot.user
        self.logger = signbot.user.logger
        try:
            options = webdriver.ChromeOptions()
            if self.user.headless:
                options.add_argument('--headless')
            options.add_argument('lang=zh_CN.UTF-8')
            options.add_argument('user-agent={0}'.format(self.UA))
            self.driver = webdriver.Chrome(options=options)
        except WebDriverException as e:
            self.logger.warn(e)
        self.driver.set_window_size(width=self.WIDTH, height=self.HEIGHT)
        self.cookies = RequestsCookieJar()

    def login(self, url='https://home.m.jd.com'):
        '''
        京东触屏版登陆
        :param usrname:
        :param passwd:
        :return:
        '''
        d = self.driver
        d.get(url)
        user_input = d.find_element_by_id('username')
        password_input = d.find_element_by_id('password')
        login_btn = d.find_element_by_id('loginBtn')
        user_input.send_keys(self.user.username)
        password_input.send_keys(self.user.password)
        if self.user.password != '':
            login_btn.click()
            time.sleep(6)
            nickname = self.driver.find_element_by_id('userName')
            self.nickname = nickname.text
            self.logger.info('{0}, 登陆成功'.format(self.nickname))
        else:
            input('请输入账户密码')
        self.save_cookies()

    def load_session(self):
        pass

    def save_cookies(self):
        cookies_list = self.driver.get_cookies()
        for cookie in cookies_list:
            try:
                cookie = self.__standardize_cookie__(cookie)
                cookiename = cookie.pop('name')
                cookieval = cookie.pop('value')
            except KeyError:
                pass
            self.cookies.set(cookiename, cookieval, **cookie)

    def __standardize_cookie__(self, cookie):
        '''
        将webdriver.get_cookies返回的cookie转换为
        兼容RequestsCookieJar的cookie
        :param cookie:
        :return a single cookie:
        '''
        c = cookie.copy()
        need_fix = [('expires', 'expiry')]
        try:
            c['rest'] = {'HttpOnly': c.pop('httpOnly')}
        except KeyError:
            pass
        for (newkey, oldkey) in need_fix:
            try:

                c[newkey] = c.pop(oldkey)
            except (KeyError, TypeError):
                pass
        return c

    def quit(self):
        self.driver.close()


class PcChrome(MobileChrome):
    UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.94 Chrome/62.0.3202.94 Safari/537.36'
    WIDTH = 1024
    HEIGHT = 768

    def login(self, url):
        d = self.driver
        d.get(url)
        switcher = d.find_element_by_link_text('账户登录')
        switcher.click()
        user_input = d.find_element_by_id('loginname')
        password_input = d.find_element_by_id('nloginpwd')
        login_btn = d.find_element_by_id('loginsubmit')
        user_input.send_keys(self.user.username)
        password_input.send_keys(self.user.password)
        if self.user.username != '':
            login_btn.click()
            time.sleep(6)
            try:
                nickname = self.driver.find_element_by_class_name('nickname')
                self.nickname = nickname.text
                self.logger.info('登陆成功，欢迎{0}'.format(self.nickname))
            except NoSuchElementException:
                self.logger.warn('登陆异常，请检查是否需要验证码')
        else:
            input('请输入账户密码')
        self.save_cookies()


def get_cookies(url, signbot) -> RequestsCookieJar:
    host = urlparse(url).netloc
    if host[-8:] == 'm.jd.com':
        bot = MobileChrome(signbot)
    else:
        bot = PcChrome(signbot)
    bot.login(url)
    cookiejar = bot.cookies
    bot.quit()
    return cookiejar


def find_chrome_driver_path():
    '''
    根据系统类型，选择chromedriver
    :return: 初始化一个
    '''
    base_path = Path(__file__).parent / '../bin'
    if platform.system() == 'Linux':
        wp = base_path.joinpath('chromedriver_linux64').resolve()
    elif platform.system() == 'Windows':
        wp = base_path.joinpath('chromedriver_win32.exe').resolve()
    elif platform.system() == 'Darwin':
        wp = base_path.joinpath('chromedriver_mac').resolve()
    else:
        wp = Path('chromedriver')
    return wp


class JdSession(Session):

    def _start_chrome_browser(self):
        # Create driver process
        return RequestiumChrome(self.webdriver_path,
                                chrome_options=self.webdriver_options,
                                default_timeout=self.default_timeout)
