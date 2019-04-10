"""
-------------------------------------------------
    File Name:     db.py
    Description:   数据库操作模块，负责对象与底层数据库
                   的交互。
    Author:        Liu
    Edited by:     chonps
-------------------------------------------------
"""
import redis
import random

from .error import PoolEmptyError
from .setting import HOST, PORT

import datetime

def get_date():
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).day

class RedisClient(object):
    """
    Redis数据库操作类。
    """

    def __init__(self, host=HOST, port=PORT):
        self.__db = redis.Redis(host, port)

    def get(self, count=1):
        """从Pool中获取一定量数据。"""
        proxies = self.__db.lrange("proxies", 0, count - 1)
        self.__db.ltrim("proxies", count, -1)
        return proxies

    def remove(self, proxy):
        # self.__db.srem("proxy_set", proxy)
        self.__db.lrem("proxies", proxy, 0)

    def put(self, proxy):
        """将代理压入Pool中。
        用Redis的set容器来负责去重，如果proxy能被压入proxy_set，
        就将其放入proxy pool中，否则不压入。
        """

        if self.__db.sadd("proxy_set", proxy + '_' + str(get_date())):
            self.__db.rpush("proxies", proxy)
        else:
            pass

    def put_many(self, proxies):
        """将一定量的代理压入Pool。
        """
        for proxy in proxies:
            self.put(proxy)

    def choice(self):
        if self.__db.llen("proxies") == 0:
            return ''
        else:
            return self.__db.lindex("proxies", random.randint(0, self.__db.llen("proxies") - 1))

    def pop(self):
        """弹出一个可用代理。
        """
        try:
            return self.__db.blpop("proxies", 30)[1].decode('utf-8')
        except:
            raise PoolEmptyError

    @property
    def queue_len(self):
        """获取proxy pool的大小。
        """
        return self.__db.llen("proxies")

    def flush(self):
        """刷新Redis中的全部内容，测试用。
        """
        self.__db.flushall()

