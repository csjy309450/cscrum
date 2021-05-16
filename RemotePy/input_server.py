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
import pyinter_core

g_global_config = {
    "input_server_ip": "0.0.0.0",
    "input_server_port": 8443,
    "output_server_ip": "0.0.0.0",
    "output_server_port": 8444,
}


class InputServerRequestHandler(BaseHTTPRequestHandler):
    thxRunner = None

    def __init__(self, request, client_address, server):
        self.url_handler_tree = {
            'scservice': {
                'subscribe': {
                    '_': {
                        'GET': self.__scservice_subscribe_get_handler
                    },
                },
                'input': {
                    '_': {
                        'POST': self.__scservice_input_post_handler
                    }
                }
            },
        }
        super().__init__(request, client_address, server)
        pass

    def send_content(self, res_msg_, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(res_msg_)))
        self.end_headers()
        if type(res_msg_) == str:
            self.wfile.write(bytes(res_msg_, encoding='utf-8'))
        elif type(res_msg_) == bytes:
            self.wfile.write(res_msg_)
        pyinter_core.myprint("response: " + res_msg_)

    def do_GET(self):
        pyinter_core.myprint("get url: " + self.path)
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
                pyinter_core.myprint(str(it))
            pass
        if flag is True:
            if handler_tree is not None:
                if type(handler_tree) is dict:
                    if 'GET' in handler_tree['_'] and callable(handler_tree['_']['GET']):
                        handler_tree['_']['GET'](self.headers)
            pass
        pass

    def do_POST(self):
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len)
        pyinter_core.myprint("post url: " + self.path)
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
                pyinter_core.myprint(it)
            pass
        if flag is True:
            if handler_tree is not None:
                if type(handler_tree) is dict:
                    handler_tree['_']['POST'](self.headers, post_body.decode('utf-8'))
            pass
        pass

    def __scservice_subscribe_get_handler(self, header_):
        pyinter_core.myprint(str(header_))
        # pyinter.myprint('remote addr: ' + str(addr))
        InputServerRequestHandler.thxRunner = pyinter_core.CmdRunnerThx("CmdRunnerThx")
        InputServerRequestHandler.thxRunner.start()
        res_ = "{" \
               "\"status\": 0" \
               "\"session_key\": \"" + "sss" + "\"," \
               "\"ip\": \"" + g_global_config['output_server_ip'] + "\"," \
               "\"port\": \"" + str(g_global_config['output_server_port']) + "\"" \
               "}"
        self.send_content(res_)
        pass

    def __scservice_input_post_handler(self, header_, body_):
        pyinter_core.myprint(str(header_))
        pyinter_core.myprint(str(body_))
        jObj = json.loads(body_)
        delay_ = 2
        if jObj is None or type(jObj) is not dict:
            res_ = "{\"status\": -1, \"msg\":\"Invalid Request.\"}"
        else:
            if jObj["input"] == "exit()":
                InputServerRequestHandler.thxRunner.stop()
                time.sleep(delay_)
                InputServerRequestHandler.thxRunner = pyinter_core.CmdRunnerThx("CmdRunnerThx")
                InputServerRequestHandler.thxRunner.start()
            else:
                pyinter_core.g_msg_queue_in.push_back(jObj["input"])
                pyinter_core.myprint("push msg: %s" % jObj["input"])
            res_ = "{\"status\": 0}"
        self.send_content(res_)
        pass


if __name__ == '__main__':
    out_service = pyinter_core.OutputStreamService(g_global_config['output_server_ip'],
                                                   g_global_config['output_server_port'])
    out_service.start()
    try:
        httpd = server.HTTPServer((g_global_config['input_server_ip'], g_global_config['input_server_port']),
                                  InputServerRequestHandler)
    except Exception as a:
        pyinter_core.myprint("HTTPServer start failed.")
        exit()
    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # context.load_cert_chain("server-cert.pem", "server-key.pem")
    # httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    try:
        pyinter_core.myprint("HTTTPS Server listening on " + g_global_config['input_server_ip'] + ":" + str(
            g_global_config['input_server_port']))
        httpd.serve_forever()
    except KeyboardInterrupt:
        pyinter_core.myprint("User quit.")
        exit()
