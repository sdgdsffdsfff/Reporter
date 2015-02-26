# -*- coding:utf-8 -*-
from threading import Thread
import time

class ExtTimer(Thread):
    def __init__(self, interval, maxtime, func):
        self.__interval = interval
        self.__maxtime = maxtime
        self.__tottime = 0.0
        self.__func = func
        self.__flag = 0
        Thread.__init__(self, None, "ExtTimer", None)
    
    def run(self):
        while self.__flag == 0:
            time.sleep(self.__interval)
            self.__func()
            # if maxtime is less than 0.0, then it means keep loop for ever
            if self.__maxtime > 0.0:
                self.__tottime += self.__interval
                if self.__tottime >= self.__maxtime:
                    print "Timeout,exit timer!"
                    self.end( )
    
    def end(self):
        self.__flag = 1

class ExtTimerDummy:
    def __init__(self):
        self.__interval = 5.0
    
    def __timerFunc(self):
        print "Hello, it is a timer function!"
    
    def createTimer(self, interval):
        self.__interval = interval
        self.__timer = ExtTimer(self.__interval, 20, self.__timerFunc)
        self.__timer.start()
        
if __name__ == "__main__":
    t = ExtTimerDummy( )
    t.createTimer( 1 )
    while True:
        pass