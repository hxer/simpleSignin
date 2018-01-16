#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback

from selenium.webdriver import ChromeOptions

from signin.chrome import find_chrome_driver_path, JdSession
from signin.jd_job import jobs_all
from lib.log import logger
from lib.settings import PC_UA
from lib.settings import MOBILE_UA


class JDUser:
    def __init__(self, username, password, jobs_skip=None):
        self.headless = True
        self.logger = logger
        self.ua_pc = PC_UA
        self.ua = MOBILE_UA
        self.username = username
        self.password = password
        self.jobs_skip = jobs_skip or []


class JD:
    def __init__(self, username, password):
        self.user = JDUser(username, password)
        self.session = self.make_session()
        self.job_list = [job for job in jobs_all if job.__name__ not in self.user.jobs_skip]

    def sign(self):
        jobs_failed = []

        for job_class in self.job_list:
            job = job_class(self)

            # 默认使用移动设备User-agent,否则使用PC版User-Agent
            # if job.is_mobile:
            #     job.session.headers.update({
            #         'User-Agent': self.user.ua
            #     })
            # else:
            #     job.session.headers.update({
            #         'User-Agent': self.user.ua_pc})

            try:
                job.run()
            except Exception as e:
                logger.error('# 任务运行出错: ' + repr(e))
                traceback.print_exc()

            if not job.job_success:
                jobs_failed.append(job.job_name)

        print('=================================')
        print('= 任务数: {}; 失败数: {}'.format(len(self.job_list), len(jobs_failed)))
        if jobs_failed:
            print('= 失败的任务: {}'.format(jobs_failed))
        else:
            print('= 全部成功 ~')
        print('=================================')
        return len(jobs_failed) == 0

    def make_session(self) -> JdSession:
        chrome_path = find_chrome_driver_path()
        session = JdSession(webdriver_path=str(chrome_path),
                            browser='chrome',
                            webdriver_options=ChromeOptions())
        session.webdriver_options.add_argument('lang=zh_CN.UTF-8')
        if self.user.headless:
            session.webdriver_options.add_argument('headless')
        return session


if __name__ == '__main__':
    pass
