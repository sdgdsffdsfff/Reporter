# -*- coding:utf-8 -*-
import requests
import socket
import time

__author__ = 'kiven'

# 封装定时任务类(from internet)
class RepeatableTimer(object):
    def __init__(self, interval, function, args=[], kwargs={}):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def start(self):
        self.stop()
        import threading
        self._timer = threading.Timer(self.interval, self._run)
        self._timer.setDaemon(True)  # 设置后台（守护）进程
        self._timer.start()

    def restart(self):
        self.start()

    def stop(self):
        if self.__dict__.has_key("_timer"):
            self._timer.cancel()
            del self._timer

    def _run(self):
        try:
            self.function(*self.args, **self.kwargs)
        except:
            pass
        self.restart()

# 当前时间 年-月-日 时:分:秒
def nowTime():
    return time.strftime('%Y-%m-%d %H:%M:%S')

# 同步数据
# 调用http接口
def myFunction():
    print nowTime()+'\tstart to sync db from cp4...'
    r = requests.post('http://' + getLocalIP() + ':8000/syncCP4DB/')
    if r.status_code == '200':
        print nowTime()+'\tsync db success...'
    else:
        print nowTime()+'\tsync db failure...'

# 本地ip
def getLocalIP():
    myname = socket.getfqdn(socket.gethostname())
    myip = socket.gethostbyname(myname)
    return myip

# 主函数
if __name__ == '__main__':
    # 每一个小时同步一次
    r = RepeatableTimer(3600, myFunction)
    try:
        r.start()
        # 主线程无限循环
        while True:
            pass
    except KeyboardInterrupt:
        print "Bye..."
        r.stop()

