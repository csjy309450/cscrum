#!/usr/bin/python3
# -*- coding:utf-8 -*-

import traceback
import sys
import json
import os
import threading
import time
import inspect
import ctypes
import socket
from http import server
from http.server import BaseHTTPRequestHandler

import msg_queue

g_sys_std_out = sys.stdout
g_msg_queue_in = msg_queue.MsgQueue()
g_msg_queue_out = msg_queue.MsgQueue()


def myprint(msg_):
    g_sys_std_out.write(msg_ + "\n")
    g_sys_std_out.flush()


class RedirectStdOutErr:
    redthx = set()
    """
    import os, sys, cStringIO
    """
    def __init__(self):
        self.content = ''
        self.savedStdout = sys.stdout
        self.f = open('out.log', 'w+')

    @classmethod
    def add(cls, thxid_):
        RedirectStdOutErr.redthx.add(thxid_)

    @classmethod
    def remove(cls, thxid_):
        RedirectStdOutErr.redthx.remove(thxid_)

    def write(self, msg_):
        # msg = repr(msg_)
        self.savedStdout.write(msg_)
        self.savedStdout.flush()
        # self.content += msg_
        if threading.currentThread().ident in RedirectStdOutErr.redthx:
            self.f.write(msg_)
            self.f.flush()
            g_msg_queue_out.push_back(msg_)
            self.content = ''

    def flush(self):
        if self.content is None or self.content == '':
            return
        # self.content = '<result>\n' + self.content + "</result>\n"
        # self.content = "<result>\n" + r"".join(self.content) + "</result>\n"
        # msg = repr(self.content)
        msg = self.content
        self.savedStdout.write(msg)
        self.savedStdout.flush()
        if threading.currentThread().ident in RedirectStdOutErr.redthx:
            self.f.write(msg)
            self.f.flush()
            g_msg_queue_out.push_back(self.content)
            self.content = ''


sys.stdout = RedirectStdOutErr()
sys.stderr = RedirectStdOutErr()


class CmdRunnerThx(threading.Thread):
    def __init__(self, name_):
        threading.Thread.__init__(self)
        self.strName = name_
        self.bStop = True

    def run(self):
        RedirectStdOutErr.add(threading.currentThread().ident)
        myprint("start thx: " + self.strName)
        self.bStop = False
        CmdRunnerThx.__thx_call(self)
        myprint("stop thx: " + self.strName)

    def stop(self):
        self.bStop = True
        self.join(2)
        if self.is_alive():
            self.__async_raise(self.__get_my_tid(), SystemExit)

    @classmethod
    def __thx_call(cls, self):
        """
        __thx_call
        :param thread_name_:
        :param delay:
        :return:
        """
        delay_ = 1
        while not self.bStop:
            # code = input(">>> ")
            code = g_msg_queue_in.pop_front()
            if code is None:
                time.sleep(delay_)
                continue
            msg = "<input>\n" + code + "\n</input>"
            # print(r"<input>\n" + code + "\n</input>")
            print(msg)
            # exec(code)
            # print(code)
            try:
                exec(code)
            except BaseException as e:
                msg = "<err>\n" + traceback.format_exc() + "</err>"
                print(msg)
            pass

    def __get_my_tid(self):
        """determines this (self's) thread id"""
        return self.ident

    def __async_raise(self, tid_, exctype_):
        """Raises an exception in the threads with id tid"""
        if not inspect.isclass(exctype_):
            raise TypeError("Only types can be raised (not instances)")
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid_), ctypes.py_object(exctype_))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid_, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")


class CmdDispatchThx(threading.Thread):
    def __init__(self, name_):
        threading.Thread.__init__(self)
        self.strName = name_
        self.bStop = True
        self.runner = CmdRunnerThx("CmdRunnerThx")

    def run(self):
        myprint("start thx: " + self.strName)
        self.bStop = False
        self.runner.start()
        CmdDispatchThx.__thx_call(self)
        myprint("stop thx: " + self.strName)

    def stop(self):
        self.bStop = True
        pass

    @classmethod
    def __thx_call(cls, self):
        """
        __thx_call()
        :param thread_name_:
        :param delay:
        :return:
        """
        delay_ = 2
        while not self.bStop:
            # TODO 替换成https
            code = self.session[1].recv(1024).decode('utf-8')
            # time.sleep(delay_)
            if code == "exit()":
                self.runner.stop()
                time.sleep(delay_)
                self.runner = CmdRunnerThx("CmdRunnerThx")
                self.runner.start()
                continue
            g_msg_queue_in.push_back(code)
            myprint("push msg: %s" % code)


class InputService:
    def __init__(self, ip_="0.0.0.0", port_=8086):
        self.ip = ip_
        self.port = port_
        self.sock = socket.socket()
        self.remote = []
        self.out_service = None
        pass

    def start(self):
        self.sock.bind((self.ip, self.port))
        self.sock.listen(5)
        myprint('start listen ' + self.ip + ":" + str(self.port))
        while True:
            c, addr = self.sock.accept()
            myprint('remote addr: ' + str(addr))
            reader = CmdDispatchThx("CmdDispatchThx", (addr, c))
            self.remote.append((addr, c, reader))
            reader.start()
            self.out_service = OutputStreamService()
            self.out_service.start()
            pass


class CmdResponceThx(threading.Thread):
    def __init__(self, name_, session_):
        threading.Thread.__init__(self)
        self.strName = name_
        self.bStop = True
        self.session = session_

    def run(self):
        myprint("start thx: " + self.strName)
        self.bStop = False
        CmdResponceThx.__thx_call(self)
        myprint("stop thx: " + self.strName)

    def stop(self):
        self.bStop = True
        pass

    @classmethod
    def __thx_call(cls, self):
        """
        __thx_call()
        :param thread_name_:
        :param delay:
        :return:
        """
        delay_ = 1
        while not self.bStop:
            msg = g_msg_queue_out.pop_front()
            if msg is not None:
                try:
                    ret = self.session[1].send(msg.encode())
                except InterruptedError as e:
                    pass
                except ConnectionAbortedError as e:
                    self.bStop = True
                    break
                myprint("push msg: %s" % msg)
            else:
                time.sleep(delay_)


class OutputStreamService(threading.Thread):
    def __init__(self, ip_="0.0.0.0", port_=8087):
        threading.Thread.__init__(self)
        self.ip = ip_
        self.port = port_
        self.sock = socket.socket()
        self.remote = []
        pass

    def run(self):
        self.sock.bind((self.ip, self.port))
        self.sock.listen(5)
        myprint('start listen ' + self.ip + ":" + str(self.port))
        while True:
            c, addr = self.sock.accept()
            myprint('remote addr: ' + str(addr))
            reader = CmdResponceThx("CmdResponceThx", (addr, c))
            self.remote.append((addr, c, reader))
            reader.start()
            pass

    def stop(self):
        self.bStop = True
        pass


if __name__ == "__main__":
    service = InputService()
    service.start()
    pass
