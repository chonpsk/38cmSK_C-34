"""
-------------------------------------------------
    File Name:     run.py
    Description:   程序的入口。
    Author:        Liu
    Date:          2016/12/9
-------------------------------------------------
"""
from proxyPool.api import app
from proxyPool.schedule import Schedule
from multiprocessing import Process

def cli():
    s = Schedule()
    s.run()
    app.run(port = 1025)

if __name__ == '__main__':
    cli()

