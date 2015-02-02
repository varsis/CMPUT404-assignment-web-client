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

    __REGEX_HTTP = "^(http:\/\/)?([A-Za-z0-9\.-]{3,}\.[A-Za-z]{2,})(\:[0-9]{2,4})?(.*)"

    #regex the url from user and parse it for the host, port and path
    def get_host_port_path(self,url):
        # default port number,path and host
        port = 80
        path = '/'
        host = None

        http = re.match(self.__REGEX_HTTP,url)

        if http is not None:
            host = http.group(2)

            if http.group(3) is not None:
                port = int(http.group(3)[1:])

            if http.group(4) is not None:
                path = http.group(4)

        return (host,port,path)


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
        host_port = self.get_host_port_path(url)
        socket = self.connect(host_port[0],host_port[1])
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
