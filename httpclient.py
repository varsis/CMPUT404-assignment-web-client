#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
#
# Modified by Chris Pavlicek
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

    #group 1 is Code, group 2 is message
    __HTTP_REGEX = "^HTTP/1.[01] (\d{3}) (\S*)"

    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

    def __init__(self, raw):
        self._parse_raw(raw)

    def __str__(self):
        return "{}\n{}".format(self.code,self.body)

    #delegate parsing to httprequest for raw data
    def _parse_raw(self,raw):

        #split the header and body
        items = raw.split('\r\n\r\n')

        # Headers are here
        headers = items[0]
        body = items[1]

        # get the response code and message
        code_message = re.match(self.__HTTP_REGEX,headers)

        #set class vars
        self.code = int(code_message.group(1))
        self.message = code_message.group(2)
        self.body = body


class HTTPClient(object):

    __REGEX_HTTP = "^(http:\/\/)?([A-Za-z0-9\.-]{1,})(\:[0-9]{2,5})?(.*)"

    # format = type,path,host,port,additional header(s),body
    __REQUEST_FORMAT = "{} {} HTTP/1.1\r\nHost: {}:{}\r\nConnection: close{}\r\n\r\n{}"

    #regex the url from user and parse it for the host, port and path
    def get_host_port_path(self,url):
        # default port number,path and host
        port = 80
        path = '/'
        host = None

        # match up the items
        http = re.match(self.__REGEX_HTTP,url)

        # Check each regex group
        if http is not None:
            host = http.group(2)

            if http.group(3) is not None:
                port = int(http.group(3)[1:])

            if http.group(4) is not None and http.group(4):
                path = http.group(4)

        #return the host,port,path
        return (host,port,path)


    def connect(self, host, port):
        try:
            # try creating a connection with a socket
            userSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            userSocket.connect((host,port))
            return userSocket
        except Exception as e:
            print "Address-related error connecting to server: %s" % e
            sys.exit(1)

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
        host_port_path = self.get_host_port_path(url)

        host = host_port_path[0]
        port = host_port_path[1]
        path = host_port_path[2]

        socket = self.connect(host,port)
        self.sendall(socket,self.__REQUEST_FORMAT \
                .format("GET",path,host,port,"","",""))

        return HTTPRequest(self.recvall(socket))

    def POST(self, url, args=None):
        host_port_path = self.get_host_port_path(url)

        host = host_port_path[0]
        port = host_port_path[1]
        path = host_port_path[2]

        # default body,headers..
        body = ""
        headers = ""

        #only add these headers if was have args to pass
        if args is not None and len(args) > 0:
            body = urllib.urlencode(args)
            headers = "\r\nContent-Type: application/x-www-form-urlencoded \
                       \r\nContent-Length: {}".format(len(body))

        #setup the connection
        socket = self.connect(host,port)
        self.sendall(socket,self.__REQUEST_FORMAT \
                .format("POST",path,host,port,headers,body))

        # return parsed httprequest
        return HTTPRequest(self.recvall(socket))

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
        print client.command( command, sys.argv[1] )
