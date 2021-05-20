#!/usr/bin/python3
# -*- coding:utf-8 -*-

from http import server
from http.server import BaseHTTPRequestHandler
import socket
import ssl
import sys
import subprocess
import os
import time
import json
import re
import uuid
import shutil
import hashlib
import threading

g_global_config = {
    "filesync_server_ip": "0.0.0.0",
    "filesync_server_port": 8444,
    "filesync_workdir": "./workdir/",
    "filesync_time_format": '%Y-%m-%d %H:%M:%S',
}


def calcFileSha256(filname):
    """calculate file sha256"""
    with open(filname, "rb") as f:
        sha256obj = hashlib.sha256()
        sha256obj.update(f.read())
        hash_value = sha256obj.hexdigest()
    return hash_value


class SDIDObj:
    def __init__(self, sdid_):
        self.sdid = sdid_
        self.locker = threading.Lock()

    def lock(self):
        return self.locker.acquire()

    def unlock(self):
        return self.locker.release()

    def islocked(self):
        return self.locker.locked()


class SDIDArray:
    def __init__(self):
        self.sdids = {}
        self.locker = threading.Lock()

    def insert(self, sdid_):
        if type(sdid_) is not str:
            return
        else:
            self.locker.acquire()
            if sdid_ not in self.sdids:
                self.sdids[sdid_] = SDIDObj(sdid_)
            self.locker.release()

    def remove(self, sdid_):
        self.locker.acquire()
        if sdid_ in self.sdids:
            self.sdids.pop(sdid_)
        self.locker.release()

    def __find(self, sdid_):
        if sdid_ in self.sdids:
            return self.sdids[sdid_]
        return None

    def locksdid(self, sdid_):
        self.locker.acquire()
        osdid = self.__find(sdid_)
        if osdid is not None:
            osdid.lock()
            self.locker.release()
            return True
        else:
            self.locker.release()
            self.insert(sdid_)
            return self.locksdid(sdid_)

    def unlocksdid(self, sdid_):
        self.locker.acquire()
        osdid = self.__find(sdid_)
        if osdid is not None:
            osdid.unlock()
            self.locker.release()
            return True
        else:
            self.locker.release()
            self.insert(sdid_)
            return True


class GlobalManager:
    sdids = SDIDArray()


class FileSyncServerRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.url_handler_tree = {
            'filesync': {
                'updateFile': {
                    '_': {
                        'POST': self.__filesync_updateFile_post_handler
                    }
                },
                # 'openSyncDirectory': {
                #     '_': {
                #         'POST': self.__filesync_openSyncDirectory_post_handler
                #     }
                # },
                # 'closeSyncDirectory': {
                #     '_': {
                #         'POST': self.__filesync_closeSyncDirectory_post_handler
                #     }
                # },
                'createSyncDirctory': {
                    '_': {
                        'POST': self.__filesync_createSyncDirctory_post_handler
                    }
                },
                'destroySyncDirctory': {
                    '_': {
                        'POST': self.__filesync_destroySyncDirctory_post_handler
                    }
                },
                'getAllSyncDirctory': {
                    '_': {
                        'GET': self.__filesync_getAllSyncDirctory_get_handler
                    }
                },
                'getSyncDirectoryMeta': {
                    '_': {
                        'POST': self.__filesync_getSyncDirectoryMeta_post_handler
                    },
                },
            },
        }
        super().__init__(request, client_address, server)
        pass

    def send_content(self, res_msg_, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/json")
        self.send_header("Content-Length", str(len(res_msg_)))
        self.end_headers()
        if type(res_msg_) == str:
            self.wfile.write(bytes(res_msg_, encoding='utf-8'))
        elif type(res_msg_) == bytes:
            self.wfile.write(res_msg_)
        print("response: "+res_msg_)

    def do_GET(self):
        print("get url: " + self.path)
        uri, query = None, None
        url_tree = []
        if "?" in self.path:
            uri, query = self.path.split('?')
        else:
            uri = self.path
        url_tree = self.path.split('/')
        handler_tree = self.url_handler_tree
        flag = True
        for it in url_tree:
            if type(it) is str and it != '':
                try:
                    handler_tree = handler_tree[it]
                except KeyError as e:
                    flag = False
                    break
                print(str(it))
            pass
        if flag is True:
            if handler_tree is not None:
                if type(handler_tree) is dict:
                    if 'GET' in handler_tree['_'] and callable(handler_tree['_']['GET']):
                        try:
                            handler_tree['_']['GET'](self.headers)
                        except Exception as e:
                            print(e)
                            res_ = "Service error(" + str(e) + ")"
                            self.send_content(res_, 501)
                            pass
                    else:
                        res_ = "Service error."
                        self.send_content(res_, 501)
            pass
        else:
            res_ = "Invalid API call."
            self.send_content(res_, 404)
        pass

    def do_POST(self):
        content_len = int(self.headers['Content-Length'])
        print("post url: "+self.path)
        uri, query = None, None
        url_tree = []
        if "?" in self.path:
            uri, query = self.path.split('?')
        else:
            uri = self.path
        url_tree = self.path.split('/')
        handler_tree = self.url_handler_tree
        flag = True
        for it in url_tree:
            if type(it) is str and it != '':
                try:
                    handler_tree = handler_tree[it]
                except KeyError as e:
                    flag = False
                    break
                print(it)
            pass
        if flag is True:
            if handler_tree is not None:
                if type(handler_tree) is dict:
                    if 'POST' in handler_tree['_'] and callable(handler_tree['_']['POST']):
                        try:
                            handler_tree['_']['POST'](self.headers, content_len)
                        except Exception as e:
                            res_ = "Service error(" + str(e) + ")"
                            self.send_content(res_, 501)
                            pass
                    else:
                        res_ = "Service error."
                        self.send_content(res_, 501)
            pass
        else:
            res_ = "Invalid API."
            self.send_content(res_, 404)
        pass

    def __filesync_updateFile_post_handler(self, header_, content_len_):
        def __rewirte_file(path_, f_, len_):
            path, file = os.path.split(path_)
            if file == '':
                return 3
            filepaths = re.split("[\\/]", path)
            while '' in filepaths:
                filepaths.remove('')
            if not os.path.isdir(g_global_config['filesync_workdir'] + SDID + "/root"):
                os.mkdir(g_global_config['filesync_workdir'] + SDID + "/root")
            for it in filepaths:
                if not os.path.isdir(g_global_config['filesync_workdir'] + SDID + "/root/" + it):
                    os.mkdir(g_global_config['filesync_workdir'] + SDID + "/root/" + it)
                    pass
            if not os.path.isdir(g_global_config['filesync_workdir'] + SDID + "/root/" + path):
                return 3
            batch_size = 1024
            rest_size = len_
            with open(g_global_config['filesync_workdir'] + SDID + "/root/" + path_, 'wb') as f:
                while rest_size > batch_size:
                    buff = f_.read(batch_size)
                    f.write(buff)
                    rest_size -= batch_size
                buff = f_.read(rest_size)
                f.write(buff)
            return 0

        def __append_file(path_, f_, len_):
            path, file = os.path.split(path_)
            if file == '':
                return 3
            filepaths = re.split("[\\/]", path)
            while '' in filepaths:
                filepaths.remove('')
            if not os.path.isdir(g_global_config['filesync_workdir'] + SDID + "/root"):
                os.mkdir(g_global_config['filesync_workdir'] + SDID + "/root")
            for it in filepaths:
                if not os.path.isdir(g_global_config['filesync_workdir'] + SDID + "/root/" + it):
                    os.mkdir(g_global_config['filesync_workdir'] + SDID + "/root/" + it)
                    pass
            if not os.path.isdir(g_global_config['filesync_workdir'] + SDID + "/root/" + path):
                return 3
            batch_size = 1024
            rest_size = len_
            with open(g_global_config['filesync_workdir'] + SDID + "/root/" + path_, 'ab') as f:
                while rest_size > batch_size:
                    buff = f_.read(batch_size)
                    f.write(buff)
                    rest_size -= batch_size
                buff = f_.read(rest_size)
                f.write(buff)
            return 0

        def __remove_file(path_):
            if os.path.isdir(g_global_config['filesync_workdir'] + SDID + "/root/" + path_):
                shutil.rmtree(g_global_config['filesync_workdir'] + SDID + "/root/" + path_)
                return 0
            if os.path.isfile(g_global_config['filesync_workdir'] + SDID + "/root/" + path_):
                os.remove(g_global_config['filesync_workdir'] + SDID + "/root/" + path_)
                return 0
            pass

        def __mkdir(path_):
            filepaths = re.split("[\\/]", path_)
            while '' in filepaths:
                filepaths.remove('')
            if not os.path.isdir(g_global_config['filesync_workdir'] + SDID + "/root"):
                os.mkdir(g_global_config['filesync_workdir'] + SDID + "/root")
            for it in filepaths:
                if not os.path.isdir(g_global_config['filesync_workdir'] + SDID + "/root/" + it):
                    os.mkdir(g_global_config['filesync_workdir'] + SDID + "/root/" + it)
                    pass
            if not os.path.isdir(g_global_config['filesync_workdir'] + SDID + "/root/" + path_):
                return 3
            return 0

        print(str(content_len_))
        # save file
        status = 0
        if header_['Content-Type'].find('multipart') == -1:
            status = 1
            print('Content-Type isn\'t multipart')
        else:
            if header_['Content-Type'].find('boundary=') == -1:
                status = 1
                print('Content-Type without boundary')
            else:
                SDID = ''
                filepath = ''
                fop = ''
                fstate = ''

                boundary = header_['Content-Type'][header_['Content-Type'].find('boundary=')+len('boundary='):]
                # parser first data
                post_body = self.rfile.readline().decode('utf-8')
                if post_body.find('--' + boundary) == -1:
                    status = 1
                    pass
                else:
                    '''parser first data: file header'''
                    print(post_body)
                    post_body = self.rfile.readline().decode('utf-8')
                    if post_body.find('Content-Length: ') != -1:
                        sub_len = int(post_body[post_body.find('Content-Length: ')+len('Content-Length: '):])
                        post_body = self.rfile.readline()  # step over \r\n
                        post_body = self.rfile.read(sub_len).decode('utf-8')
                        try:
                            jobj = json.loads(post_body)
                            if jobj is None or type(jobj) is not dict:
                                status = 1
                            else:
                                print(str(jobj))
                                filepath = jobj['filepath']
                                SDID = jobj['SDID']
                                fop = jobj['fop']
                                fstate = jobj['fstate']
                                pass
                            pass
                        except Exception as e:
                            status = 1
                            pass
                    else:
                        # invalid format
                        status = 1
                        pass
                    '''parser second data: file body'''
                    post_body = self.rfile.readline()# step over \r\n
                    post_body = self.rfile.readline().decode('utf-8')
                    if post_body.find('--' + boundary) == -1:
                        status = 1
                        pass
                    else:
                        print(post_body)
                        post_body = self.rfile.readline().decode('utf-8')
                        if post_body.find('Content-Length: ') != -1:
                            sub_len = int(post_body[post_body.find('Content-Length: ')+len('Content-Length: '):])
                            post_body = self.rfile.readline()  # step over \r\n
                            print('do write file')
                            '''verify SDID'''
                            if SDID != '' \
                                and os.path.isdir(g_global_config['filesync_workdir'] + SDID) \
                                and os.path.isfile(g_global_config['filesync_workdir'] + SDID + "/metainfo.json"):
                                # TODO lock SD
                                if fop == 0:
                                    '''rewirte file'''
                                    status = __rewirte_file(filepath, self.rfile, sub_len)
                                    pass
                                elif fop == 1:
                                    '''__append_file file'''
                                    status = __append_file(filepath, self.rfile, sub_len)
                                    pass
                                elif fop == 2:
                                    status = __remove_file(filepath)
                                    pass
                                elif fop == 3:
                                    status = __mkdir(filepath)
                                    pass

                                if status == 0:
                                    if fop != 3:
                                        '''update metainfo.json'''
                                        buff_out = ""
                                        with open(g_global_config['filesync_workdir'] + SDID + "/metainfo.json",
                                                  'r') as f:
                                            buff_in = f.read()
                                            jmeta = json.loads(buff_in)
                                            if jmeta is None or type(jmeta) is not dict:
                                                pass
                                            else:
                                                if fop == 0 or fop == 1:
                                                    if fstate == 0:
                                                        '''file data receiving complete, update metainfo.json'''
                                                        bfind = False
                                                        sha256 = calcFileSha256(g_global_config['filesync_workdir'] + SDID + "/root/" + filepath)
                                                        for it in jmeta['dir_info']:
                                                            if it[0] == filepath:
                                                                '''compute file SHA256'''
                                                                it[1] = sha256
                                                                bfind = True
                                                                break
                                                        if not bfind:
                                                            jmeta['dir_info'].append([filepath, sha256])
                                                            pass
                                                        pass
                                                elif fop == 2:
                                                    for it in jmeta['dir_info']:
                                                        if it[0] == filepath:
                                                            jmeta['dir_info'].remove(it)
                                                    pass
                                                buff_out = json.dumps(jmeta)
                                        if buff_out is not "":
                                            with open(g_global_config['filesync_workdir'] + SDID + "/metainfo.json", 'w+') as f:
                                                f.write(buff_out)
                                                pass
                                        pass
                                # TODO unlock SD
                                pass
                        else:
                            # invalid format
                            status = 1
                            pass
                        # parse end
                        post_body = self.rfile.readline()# step over \r\n
                        post_body = self.rfile.readline().decode('utf-8')
                        if post_body.find('--' + boundary + '--') != -1:
                            print(post_body)
        res_ = "{" \
               "\"status\": " + str(status) + \
               "}"
        self.send_content(res_)
        pass

    # def __filesync_openSyncDirectory_post_handler(self, header_, content_len_):
    #     post_body = self.rfile.read(content_len_).decode('utf-8')
    #     print(post_body)
    #     status = 0
    #     jobj = None
    #     try:
    #         jobj = json.loads(post_body)
    #     except Exception as e:
    #         status = 1
    #         pass
    #     if jobj is None or type(jobj) is not dict:
    #         status = 1
    #     else:
    #         print(str(jobj))
    #         pass
    #     SDID = jobj['SDID']
    #     if os.path.isdir(g_global_config['filesync_workdir'] + SDID) \
    #             and os.path.isfile(g_global_config['filesync_workdir'] + SDID + "/metainfo.json"):
    #         # TODO lock SDIS
    #         if GlobalManager.sdids.locksdid(SDID):
    #             jobj_metainfo = None
    #             with open(g_global_config['filesync_workdir'] + SDID + "/metainfo.json", 'r') as f:
    #                 f_buff = f.read()
    #                 try:
    #                     jobj_metainfo = json.loads(f_buff)
    #                 except Exception as e:
    #                     status = 3
    #                     pass
    #             if jobj_metainfo is None or type(jobj_metainfo) is not dict:
    #                 status = 3
    #         # TODO unlock SDID
    #         GlobalManager.sdids.unlocksdid(SDID)
    #     else:
    #         status = 2
    #     if status == 0:
    #         res_ = "{" \
    #                "\"status\": " + str(status) + \
    #                "}"
    #     else:
    #         res_ = "{" \
    #                "\"status\": " + str(status) + \
    #                "}"
    #     self.send_content(res_)
    #     pass
    #
    # def __filesync_closeSyncDirectory_post_handler(self, header_, content_len_):
    #     post_body = self.rfile.read(content_len_).decode('utf-8')
    #     print(post_body)
    #     status = 0
    #     jobj = None
    #     try:
    #         jobj = json.loads(post_body)
    #     except Exception as e:
    #         status = 1
    #         pass
    #     if jobj is None or type(jobj) is not dict:
    #         status = 1
    #     else:
    #         print(str(jobj))
    #         pass
    #     SDID = jobj['SDID']
    #     if GlobalManager.sdids.locksdid(SDID):
    #         if os.path.isdir(g_global_config['filesync_workdir'] + SDID) \
    #                 and os.path.isfile(g_global_config['filesync_workdir'] + SDID + "/metainfo.json"):
    #             jobj_metainfo = None
    #             with open(g_global_config['filesync_workdir'] + SDID + "/metainfo.json", 'r') as f:
    #                 f_buff = f.read()
    #                 try:
    #                     jobj_metainfo = json.loads(f_buff)
    #                 except Exception as e:
    #                     status = 3
    #                     pass
    #             if jobj_metainfo is None or type(jobj_metainfo) is not dict:
    #                 status = 3
    #             else:
    #                 pass
    #         else:
    #             status = 2
    #     else:
    #         status = 2
    #     res_ = "{" \
    #            "\"status\": " + str(status) + \
    #            "}"
    #     self.send_content(res_)
    #     pass

    def __filesync_createSyncDirctory_post_handler(self, header_, content_len_):
        post_body = self.rfile.read(content_len_).decode('utf-8')
        SDID = None
        status = 0
        jobj = None
        try:
            jobj = json.loads(post_body)
        except Exception as e:
            status = 1
            pass
        if jobj is None or type(jobj) is not dict:
            status = 1
        else:
            print(str(jobj))
            pass
        orig_path = jobj['orig_path']
        while 1:
            SDID = str(uuid.uuid1())
            if not os.path.isdir(g_global_config['filesync_workdir']+SDID):
                break
        os.mkdir(g_global_config['filesync_workdir']+SDID)
        os.mkdir(g_global_config['filesync_workdir']+SDID+"/root")
        f = os.open(g_global_config['filesync_workdir'] + SDID +"/metainfo.json", os.O_RDWR | os.O_CREAT)
        if f is not None:
            localtime = time.strftime(g_global_config['filesync_time_format'])
            buff = "{" + \
                   "\"orig_path\": \"" + orig_path + "\"," + \
                   "\"SDID\": \"" + SDID + "\"," + \
                   "\"create_time\": \"" + str(localtime) + "\"," + \
                   "\"update_time\": \"" + str(localtime) + "\"," + \
                   "\"host\": \"" + header_['Host'] + "\"," + \
                   "\"dir_info\": []" + \
                   "}"
            os.write(f, buff.encode())
            os.close(f)
        else:
            status = 3
        if status == 0 and SDID is not None or SDID != '':
            res_ = "{" \
                   "\"status\": " + str(status) + "," \
                   "\"SDID\": \"" + SDID + "\"" \
                   "}"
        else:
            res_ = "{" \
                   "\"status\": " + str(status) + \
                   "}"
        self.send_content(res_)
        pass

    def __filesync_destroySyncDirctory_post_handler(self, header_, content_len_):
        post_body = self.rfile.read(content_len_).decode('utf-8')
        print(post_body)
        status = 0
        jobj = None
        try:
            jobj = json.loads(post_body)
        except Exception as e:
            status = 1
            pass
        if jobj is None or type(jobj) is not dict:
            status = 1
        else:
            print(str(jobj))
            pass
        SDID = jobj['SDID']
        if not os.path.isdir(g_global_config['filesync_workdir'] + SDID):
            status = 2
        else:
            shutil.rmtree(g_global_config['filesync_workdir'] + SDID)
            pass
        res_ = "{" \
               "\"status\": " + str(status) + \
               "}"
        self.send_content(res_)
        pass

    def __filesync_getSyncDirectoryMeta_post_handler(self, header_, content_len_):
        post_body = self.rfile.read(content_len_).decode('utf-8')
        print(post_body)
        jobj = None
        status = 0
        try:
            jobj = json.loads(post_body)
        except Exception as e:
            status = 1
            pass
        if jobj is None or type(jobj) is not dict:
            status = 1
        else:
            print(str(jobj))
            pass
        SDID = jobj['SDID']
        if os.path.isdir(g_global_config['filesync_workdir'] + SDID) \
                and os.path.isfile(g_global_config['filesync_workdir'] + SDID + "/metainfo.json"):
            with open(g_global_config['filesync_workdir'] + SDID + "/metainfo.json", 'r') as f:
                f_buff = f.read()
        else:
            status = 2
        if status == 0:
            res_ = f_buff
        else:
            res_ = "{" \
                   "\"status\": " + str(status) + \
                   "}"
        self.send_content(res_)
        pass

    def __filesync_getAllSyncDirctory_get_handler(self, header_):
        status = 0
        SDIDs = []
        if not os.path.isdir(g_global_config['filesync_workdir']):
            status = 1
        else:
            for _0, dirname, _1 in os.walk(g_global_config['filesync_workdir']):
                print(str(dirname))
                for it in dirname:
                    if os.path.isdir(g_global_config['filesync_workdir'] + it) \
                            and os.path.isfile(g_global_config['filesync_workdir'] + it + "/metainfo.json"):
                        with open(g_global_config['filesync_workdir'] + it + "/metainfo.json", 'r') as f:
                            f_buff = f.read()
                            jobj = None
                            try:
                                jobj = json.loads(f_buff)
                            except Exception as e:
                                status = 1
                                pass
                            if jobj is None or type(jobj) is not dict:
                                status = 1
                            else:
                                print(str(jobj))
                                pass
                            jobj.pop('dir_info')
                            SDIDs.append(jobj)
                    pass
                break

        res_ = "{" \
        "\"status\": " + str(status) + "," + \
        "\"dirs\": ["
        for i in range(len(SDIDs)):
            res_ += "{\"SDID\": \"" + SDIDs[i]["SDID"] + "\"," \
                    + "\"orig_path\":\"" + SDIDs[i]["orig_path"] + "\"," \
                    + "\"create_time\":\"" + SDIDs[i]["create_time"] + "\"," \
                    + "\"update_time\":\"" + SDIDs[i]["update_time"] + "\"," \
                    + "\"host\":\"" + SDIDs[i]["host"] + "\"" \
                    + "}" \
                    + ("," if i < len(SDIDs) - 1 else "")
        res_ += "]}"
        self.send_content(res_)
        pass


if __name__ == '__main__':
    try:
        httpd = server.HTTPServer((g_global_config['filesync_server_ip'], g_global_config['filesync_server_port']), FileSyncServerRequestHandler)
    except Exception as a:
        print("HTTPServer start failed.")
        exit()
    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # context.load_cert_chain("server-cert.pem", "server-key.pem")
    # httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    try:
        print("HTTTPS Server listening on "+g_global_config['filesync_server_ip']+":"+str(g_global_config['filesync_server_port']))
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("User quit.")
        exit()
