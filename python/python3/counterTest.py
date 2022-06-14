#!/usr/bin/python3

from __future__ import print_function

import time
from pysyncobj import *

class TestObj(SyncObj):

    def __init__(self, selfNode, otherNodes):
        super(TestObj, self).__init__(selfNode,otherNodes)
        self.__counter = 1


    @replicated
    def setCounter(self, value):
        self.__counter = value		
        return self.__counter


    @replicated
    def addValue(self, value):
        self.__counter += value
        return self.__counter


    def getCounter(self):
        return self.__counter


if __name__ == '__main__':
    my_ip = "192.168.1.2"
    o = TestObj('192.168.1.2:12345', ['192.168.1.3:12345', '192.168.1.4:12345'])
    n = 0
    old_value = -1

    while True:
        time.sleep(0.5)
        if o.getCounter() != old_value:
            old_value = o.getCounter()
        if o._getLeader() is None:
            print(o._getLeader())
            continue
        if str(o._getLeader()).split(":", 1)[0] == my_ip:
            print("LEADER: %s" % o._getLeader())
            if o.getCounter() <= 6: 
                o.addValue(1)
            else:
                o.setCounter(1)
            #print("COUNTER: %d" % o.getCounter())
        else:
            print("FOLLOWER")
        if o.getCounter() % 2 == 0:
            print("EVEN - PUSH")
            #print("COUNTER: %d" % o.getCounter())
        n += 1
        print("COUNTER: %d" % o.getCounter())
