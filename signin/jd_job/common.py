#!/usr/bin/env python
# encoding: utf-8
# author: Vincent
# refer: https://github.com/vc5
import re
import time

from requests import Response
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.touch_actions import TouchActions

from ..chrome import mobile_emulation
from lib.settings import MOBILE_UA


class RequestError(Exception):
    def __init__(self, message, code: str = None, response: Response = None):
        self.message = message
        self.code = code
        self.response = response


def find_value(pattern, string, default=None, flags=0):
    """
    根据正则表达式在字符串中搜索值，若未找到，返回 default
    """
    m = re.search(pattern, string, flags)

    if m:
        return m.group(1)
    else:
        return default


class Job:
    job_name = '签到任务名称demo'

    index_url = 'https://bk.jd.com/m/channel/login/daka.html'
    login_url = 'https://home.m.jd.com'
    sign_url = 'https://bk.jd.com/m/channel/login/clock.html'
    test_url = index_url
    job_gb_url = 'https://bk.jd.com/m/channel/login/recDakaGb.html'
    is_mobile = True  # 默认为True,模拟移动动设备登陆
    ua = MOBILE_UA

    # sess = requestium.Session()
    # sess.get(index_url)
    # sess.driver.close()
    # #重新初始化session的driver
    # sess._driver = sess._driver_initializer() 或
    # sess._driver = None后，可以重新使用sess.driver.get

    # 重新指定driver path
    # sess.webdriver_path="bin/chromedriver_linux64"

    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session
        self.job_success = False
        self.logger = bot.user.logger
        self.session.headers.update({'User-Agent': self.ua})
        self.session.webdriver_options.add_argument('user-agent={0}'.format(self.ua))

    def run(self):
        self.logger.info('Job Start: {}'.format(self.job_name))

        is_login = self.is_login()
        self.logger.info('登录状态: {}'.format(is_login))

        if not is_login:
            self.logger.info('进行登录...')
            try:
                self.login(url=self.login_url)
                is_login = True
                self.logger.info('登录成功')
            except Exception as e:
                self.logger.error('登录失败: {}'.format(repr(e)))

        if is_login:
            if self.is_signed():
                self.job_success = True
            else:
                self.job_success = self.sign()

        self.logger.info('Job End.')

    def is_login(self):
        r = self.session.get(self.test_url, allow_redirects=False)

        if r.is_redirect and 'passport' in r.headers['Location']:
            return False
        else:
            return True

    def login(self, url):
        # cookies = browser.get_cookies(url=self.login_url, signbot=self.bot)
        # self.session.cookies.update(cookies)
        self.session._driver = None
        if self.is_mobile:
            self.session.webdriver_options.add_experimental_option("mobileEmulation", mobile_emulation)
            driver = self.session.driver
            # 模拟触控操作
            # https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.touch_actions.html
            tap_loginbtn = TouchActions(driver)
            driver.get(url)
            user_input = driver.find_element_by_id('username')
            password_input = driver.find_element_by_id('password')
            login_btn = driver.find_element_by_id('loginBtn')
            user_input.send_keys(self.bot.user.username)
            password_input.send_keys(self.bot.user.password)
            tap_loginbtn.tap(login_btn).perform()
            time.sleep(6)
            nickname = driver.find_element_by_css_selector('#myHeader span[class$="name_text"]')
            nickname = nickname.text
            self.logger.info('登陆成功，欢迎{}'.format(nickname))
            print('登陆成功')
        else:
            self.login_pc(url)
        self.session.transfer_driver_cookies_to_session()
        self.session.driver.close()

    def login_pc(self, url):
        driver = self.session.driver
        driver.get(url)
        nickname = ''
        switcher = driver.find_element_by_link_text('账户登录')
        switcher.click()
        user_input = driver.find_element_by_id('loginname')
        password_input = driver.find_element_by_id('nloginpwd')
        login_btn = driver.find_element_by_id('loginsubmit')
        user_input.send_keys(self.bot.user.username)
        password_input.send_keys(self.bot.user.password)
        login_btn.click()
        time.sleep(6)
        try:
            nickname = driver.find_element_by_css_selector('#shortcut-2014 a[class=nickname]')
            nickname = nickname.text
            self.logger.info('登陆成功，欢迎{}'.format(nickname))
        except NoSuchElementException:
            self.logger.warning('登陆异常，请检查是否需要验证码')
        return nickname

    def is_signed(self):
        '''
        验证是否签到
        :return: 已经签到则返回True,否则返回False
        '''
        return False

    def sign(self):
        '''
        用来签到的方法
        :return:
        '''
        pass

    def report(self):
        '''
        用来报告签到结果的方法
        :return:返回需要通知用户的签到结果str
        '''
        return ''
