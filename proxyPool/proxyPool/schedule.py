"""
-------------------------------------------------
    File Name:     schedule.py
    Description:   调度器模块，
                   包含VaildityTester，PoolAdder，
                   Schedule三个类，负责维护代理池。
    Author:        Liu
    Edited by:     chonps
-------------------------------------------------
"""
import time
from multiprocessing import Process
import asyncio
import aiohttp

from .db import RedisClient
from .error import ResourceDepletionError
from .proxyGetter import FreeProxyGetter
from .setting import *


class VaildityTester(object):
    """
    检验器，负责对未知的代理进行异步检测。
    """
    # 用百度的首页来检验
    #test_api = 'https://www.baidu.com'

    test_api = TEST_URL

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []

    def set_raw_proxies(self, proxies):
        """设置待检测的代理。
        """
        self._raw_proxies = proxies
        self._usable_proxies = []

    async def test_single_proxy(self, proxy):
        """检测单个代理，如果可用，则将其加入_usable_proxies
        """
        async with aiohttp.ClientSession() as session:
            try:
                real_proxy = 'http://' + proxy
                async with session.get(self.test_api, proxy=real_proxy, timeout=15) as resp:
                    self._usable_proxies.append(proxy)
            except Exception:
                pass

    def test(self):
        """异步检测_raw_proxies中的全部代理。
        """
        print('VaildityTester is working')
        loop = asyncio.get_event_loop()
        tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
        try:
            loop.run_until_complete(asyncio.wait(tasks))
        except:
            self._usable_proxies.extend(self._raw_proxies)
            print ('test GG')

    def get_usable_proxies(self):
        return self._usable_proxies


class PoolAdder(object):
    """
    添加器，负责向池中补充代理
    """

    def __init__(self, threshold):
        self._threshold = threshold
        self._conn = RedisClient()
        self._tester = VaildityTester()
        self._crawler = FreeProxyGetter()

    def is_over_threshold(self):
        """
        判断代理池中的数据量是否达到阈值。
        """
        if self._conn.queue_len >= self._threshold:
            return True
        else:
            return False

    def add_to_queue(self, flag = GET_NUMBER):
        """
        命令爬虫抓取一定量未检测的代理，然后检测，将通过检测的代理
        加入到代理池中。
        """
        print('PoolAdder is working')
        while not self.is_over_threshold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_label]
                raw_proxies = self._crawler.get_raw_proxies(callback, flag)
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test()
                self._conn.put_many(self._tester.get_usable_proxies())
                if self.is_over_threshold():
                    break

            flag += flag
            if flag >= 10 * flag:
                raise ResourceDepletionError


class Schedule(object):
    """
    总调度器，用于协调各调度器模块
    """

    @staticmethod
    def vaild_proxy(cycle=VAILD_CHECK_CYCLE):
        """
        对已经如池的代理进行检测，防止池中的代理因长期
        不使用而过期。
        抽出代理池队列中前1/4的代理，检测，合格者压入队列尾。
        """
        conn = RedisClient()
        tester = VaildityTester()
        while True:
            time.sleep(cycle)
            count = int(0.25 * conn.queue_len)
            if count == 0:
                continue
            raw_proxies = conn.get(count)
            tester.set_raw_proxies(raw_proxies)
            tester.test()
            proxies = tester.get_usable_proxies()
            conn.put_many(proxies)

    @staticmethod
    def check_pool(lower_threshold=POOL_LOWER_THRESHOLD,
                   upper_threshold=POOL_UPPER_THRESHOLD,
                   cycle=POOL_LEN_CHECK_CYCLE):
        """
        协调添加器，当代理池中可用代理的数量低于下阈值时，触发添加器，启动爬虫
        补充代理，当代理达到上阈值时，添加器停止工作。
        """
        conn = RedisClient()
        adder = PoolAdder(upper_threshold)
        while True:
            if conn.queue_len < lower_threshold:
                adder.add_to_queue()
            time.sleep(cycle)

    def run(self):
        """
        运行调度器，创建两个进程，对代理池进行维护。
        """
        vaild_process = Process(target=Schedule.vaild_proxy)
        check_process = Process(target=Schedule.check_pool)
        #vaild_process.start()
        check_process.start()
