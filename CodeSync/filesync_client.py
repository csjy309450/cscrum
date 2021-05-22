#!/usr/bin/python3
# -*- coding:utf-8 -*-

import http.client, urllib.parse
import json
import os
import numpy as np
import hashlib
import base64


def calcFileSha256(filname):
    """calculate file sha256"""
    with open(filname, "rb") as f:
        sha256obj = hashlib.sha256()
        sha256obj.update(f.read())
        hash_value = sha256obj.hexdigest()
    return hash_value


class FileSyncClient:
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

    def __getSyncDirectoryMeta(self, sdid_):
        headers = {'Connection': 'keep-alive'}
        body = "{" \
               + "\"SDID\": \"" + sdid_ + "\"" \
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

    def __updateFile(self, sdid_, fop_, fstate_, file_, buf_):
        # TODO bug file encoding issue, should read binary and encode
        headers = {'Connection': 'keep-alive',
                   'Content-Type': 'multipart; boundary=--AAA'
                   }
        body = ''
        body_file_header = "{" \
                           + "\"filepath\": \"" + file_ + "\"," \
                           + "\"SDID\": \"" + sdid_ + "\"," \
                           + "\"fop\": " + str(fop_) + "," \
                           + "\"fstate\": " + str(fstate_) \
                           + "}"
        body += '----AAA\r\n' \
                + 'Content-Length: ' + str(len(body_file_header.encode())) + '\r\n\r\n' \
                + body_file_header + '\r\n'\
                + '----AAA\r\n' \
                + 'Content-Length: ' + str(len(str(buf_))) + '\r\n\r\n' \
                + str(buf_) + "\r\n" \
                + '----AAA--\r\n'
        conn = http.client.HTTPConnection(self.ip, self.port, timeout=10)
        conn.request("POST", "/filesync/updateFile", headers=headers, body=body.encode('utf8'))
        res = conn.getresponse()
        data = res.read().decode('utf8')
        print(data)
        try:
            jobj = json.loads(data)
            if jobj is None or type(jobj) is not dict:
                raise Exception('invalid data')
            if jobj['status'] != 0:
                raise Exception('update file failed.')
        except Exception as e:
            raise e
        pass

    def __removeFile(self, sdid_, file_):
        # TODO bug file encoding issue, should read binary and encode
        headers = {'Connection': 'keep-alive',
                   'Content-Type': 'multipart; boundary=--AAA'
                   }
        body = ''
        body_file_header = "{" \
                           + "\"filepath\": \"" + file_ + "\"," \
                           + "\"SDID\": \"" + sdid_ + "\"," \
                           + "\"fop\": " + str(2) + "," \
                           + "\"fstate\": " + str(0) \
                           + "}"
        buf_ = 'Delete File.'
        body += '----AAA\r\n' \
                + 'Content-Length: ' + str(len(body_file_header.encode())) + '\r\n\r\n' \
                + body_file_header + '\r\n'\
                + '----AAA\r\n' \
                + 'Content-Length: ' + str(len(str(buf_))) + '\r\n\r\n' \
                + str(buf_) + "\r\n" \
                + '----AAA--\r\n'
        conn = http.client.HTTPConnection(self.ip, self.port, timeout=10)
        conn.request("POST", "/filesync/updateFile", headers=headers, body=body.encode('utf8'))
        res = conn.getresponse()
        data = res.read().decode('utf8')
        print(data)
        try:
            jobj = json.loads(data)
            if jobj is None or type(jobj) is not dict:
                raise Exception('invalid data')
            if jobj['status'] != 0:
                raise Exception('update file failed.')
        except Exception as e:
            raise e
        pass

    def __uploadFile(self, sdid_, root_, file_) -> bool:
        with open(os.path.join(root_, file_), 'rb') as f:
            fop = 0
            while 1:
                buf = f.read(1024 * 1024)
                b64 = base64.encodebytes(buf)
                msg = b64.decode()
                if buf != b'':
                    try:
                        self.__updateFile(sdid_, fop, 1, file_, msg)
                    except Exception as e:
                        return False
                else:
                    try:
                        self.__updateFile(sdid_, fop, 0, file_, msg)
                    except Exception as e:
                        return False
                    break
                fop = 1
            pass
        return True

    @staticmethod
    def __scan_dir(dir_path_):
        if not os.path.isdir(dir_path_):
            raise Exception("invalid dir_path_ " + dir_path_)
        file_list = []
        for root, dirs, files in os.walk(dir_path_):
            begin = 0
            if dir_path_[-1] == '\\' or dir_path_[-1] == '/':
                begin = len(dir_path_)
            else:
                begin = len(dir_path_) + 1
            root_path = root[begin:].replace('\\', '/')
            for file in files:
                if root_path == '':
                    file_list.append(file.replace("\\", '/'))
                else:
                    file_list.append(root_path + '/' + file.replace("\\", '/'))
        return file_list

    def sync(self, sdid_, local_dir_):
        if type(local_dir_) is not str or type(sdid_) is not str:
            print("invalid local path.")
            raise Exception("invalid param")
        if local_dir_[-1] != '\\' and local_dir_[-1] != '/':
            local_dir_ += '/'
        meta_ = self.__getSyncDirectoryMeta(sdid_)
        # TODO 20210520 scan local dir and
        if type(meta_) is not dict:
            raise Exception("invalid sdid_ " + sdid_)
        local_list = np.array(FileSyncSession.__scan_dir(local_dir_))
        remote_list = np.array(meta_['dir_info'])
        for it in local_list:
            # if it == 'test_bills/微信支付账单(20190101-20190301).csv':
            #     print('a')
            #     pass
            ret = np.where(remote_list[:, 0] == it)
            if np.size(ret) == 1:
                '''remote file exist'''
                if os.path.isfile(local_dir_+it):
                    local_sha256 = calcFileSha256(local_dir_+it)
                    remote_sha256 = remote_list[ret[0], 1]
                    if local_sha256 == remote_sha256:
                        pass
                    else:
                        if not self.__uploadFile(sdid_, local_dir_, it):
                            print("upload file faild " + it)
                        pass
                    pass
                pass
                remote_list = np.delete(remote_list, ret[0], axis=0)
            elif np.size(ret) > 1:
                print("duplicate file")
                continue
            else:
                if not self.__uploadFile(sdid_, local_dir_, it):
                    print("upload file faild " + it)
                continue
            pass
        print("---- print will delete")
        for it in remote_list:
            print(it)
            try:
                self.__removeFile(sdid_, it[0])
            except Exception as e:
                pass
        pass


if __name__ == '__main__':
    fsyn = FileSyncClient("127.0.0.1", 8444)
    sds = fsyn.getAllSyncDirectory()
    print('getAllSyncDirectory:\n' + str(sds))
    fsyn.sync("c2e102a4-b7ee-11eb-9fa4-3c46d899fc43", "./source2")
    pass