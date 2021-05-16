#!/usr/bin/python3
# -*- coding:utf-8 -*-

import threading


class MsgQueue:
    def __init__(self):
        self.__msg_queue = []
        self.__msg_queue_locker = threading.Lock()

    def push_back(self, msg_):
        self.__msg_queue_locker.acquire()
        self.__msg_queue.append(msg_)
        self.__msg_queue_locker.release()

    def pop_front(self):
        item = None
        self.__msg_queue_locker.acquire()
        if self.__msg_queue is not None and self.__msg_queue != []:
            item = self.__msg_queue.pop(0)
        self.__msg_queue_locker.release()
        return item

    def empty(self):
        return len(self.__msg_queue) == 0

    def size(self):
        return len(self.__msg_queue)
