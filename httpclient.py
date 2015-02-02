#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    __REGEX_HTTP = "^http:\/\/[A-Za-z0-9\.-]{3,}\.[A-Za-z]{3}"
    __REGEX_URL = "^[A-Za-z0-9\.-]{3,}\.[A-Za-z]{3}"
    __REGEX_PORT = "(?:\:[0-9]{2,4})"

    def get_host_port(self,url):
        # default port number
        port = 80

        host = re.match(self.__REGEX_HTTP,url)

        if host is not None:
            host = host.group(0)
            host = host[7:]
        else:
            host = re.match(self.__REGEX_URL,url)
            if host is not None:
                host = host.group(0)

        check_port = re.search(self.__REGEX_PORT,url)

        if check_port is not None:
            check_port = check_port.group(0)
            port = int(check_port[1:])

        return (host,port)


    def connect(self, host, port):
        try:
            userSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            userSocket.connect((host,port))
            return userSocket
        except Exception as e:
            print "Address-related error connecting to server: %s" % e
            sys.exit(1)

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None

    def sendall(self, sock, message):
        totalsent = 0
        message_len = len(message)
        while totalsent < message_len:
            sent = sock.send(message[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        host_port = self.get_host_port(url)
        socket = self.connect(host_port[0],host_port[1])
        print(socket)
        self.sendall(socket,"CRAP")
        code = 500
        body = ""
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( command, sys.argv[2] )
