#!/usr/bin/python3
# -*- coding:utf-8 -*-

import http.client, urllib.parse
import json


class FileSyncSession:
    def __init__(self, ip_, port_):
        self.ip = ip_
        self.port = port_
        pass

    def getAllSyncDirectory(self):
        headers = {'Connection': 'keep-alive'}
        conn = http.client.HTTPConnection(self.ip, self.port, timeout=10)
        conn.request("GET", "/filesync/getAllSyncDirctory", headers=headers)
        res = conn.getresponse()
        data = res.read().decode('utf8')
        print(data)
        try:
            jobj = json.loads(data)
            if jobj is None or type(jobj) is not dict:
                raise Exception('invalid data')
            else:
                return jobj['dirs']
            pass
        except Exception as e:
            raise e

    def __getSyncDirectoryMeta(self, sid_):
        headers = {'Connection': 'keep-alive'}
        body = "{" \
               + "\"SDID\": \"" + sid_ + "\"" \
               + "}"
        conn = http.client.HTTPConnection(self.ip, self.port, timeout=10)
        conn.request("POST", "/filesync/getSyncDirectoryMeta", headers=headers, body=body)
        res = conn.getresponse()
        data = res.read().decode('utf8')
        print(data)
        try:
            jobj = json.loads(data)
            if jobj is None or type(jobj) is not dict:
                raise Exception('invalid data')
            else:
                return jobj
            pass
        except Exception as e:
            raise e

    def sync(self, sid_, local_dir_):
        if type(local_dir_) is not str:
            print("invalid local path.")
            raise Exception("invalid param")
        meta_ = self.__getSyncDirectoryMeta(sid_)
        # TODO 20210520 scan local dir and
        pass


if __name__ == '__main__':
    fsyn = FileSyncSession("127.0.0.1", 8444)
    sds = fsyn.getAllSyncDirectory()
    fsyn.sync("c2e102a4-b7ee-11eb-9fa4-3c46d899fc43", "sss")
    pass