import requests
import lxml
import asyncio
import time
import aiohttp
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}


def get_page(url):
    try:
        r = requests.get(url, headers=headers, timeout = 9)
    except:
        raise
    try:
        soup = BeautifulSoup(r.content.decode("utf-8"), 'lxml')
    except UnicodeDecodeError:
        soup = BeautifulSoup(r.text, 'lxml')
    return soup


class Downloader(object):
    """
    一个异步下载器，可以对代理源异步抓取，但是容易被BAN。
    """
    def __init__(self, urls):
        self.urls = urls
        self._htmls = []

    async def download_single_page(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                self._htmls.append(await resp.text())

    def download(self):
        loop = asyncio.get_event_loop()
        tasks = [self.download_single_page(url) for url in self.urls]
        loop.run_until_complete(asyncio.wait(tasks))

    @property
    def htmls(self):
        self.download()
        return self._htmls
