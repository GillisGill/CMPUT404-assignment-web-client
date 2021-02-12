#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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
import urllib.parse
import time
#import requests
#import urllib.request

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        req = urllib.parse.urlparse(url)
        port = req.port
        host = req.hostname
        path = req.path
        return (host,port,path)


    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

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
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        body = ""
        # Get host, port, and path
        (host, port,path) = self.get_host_port(url)
        if (port == None):
            port = 80

        # Connect
        self.connect(host,port)
        
        if (path == ""):
            path = "/"
        
        # Form GET request
        request6 = ("GET "+path+" HTTP/1.1\r\nHost: "+host+"\r\nAccept: */*\r\nConnection: close\r\n\r\n")

        self.socket.sendall(request6.encode())

        time.sleep(.100)
        self.socket.shutdown(socket.SHUT_WR)
        # Get response
        data = self.socket.recv(4096).decode()

        time.sleep(.100)
        self.close()

        # set code and body
        code_index = data.find("HTTP") + 8
        code_index_end = code_index + 4
        code_str = data[code_index:code_index_end:1]
        code = int(code_str)

        print(data)
        body = data
        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        body = ""
        # Get host, port, and path
        (host, port,path) = self.get_host_port(url)
        if (port == None):
            port = 80

        # Connect
        self.connect(host,port)
        
        if (path == ""):
            path = "/"
        
        # Parse args
        enargs = "{}"
        length_b = str(len(enargs))
        if (args != None):
            enargs = str(urllib.parse.urlencode(args))
            length_b = str(len(enargs))

        # Form request
        request6 = "POST "+path+" HTTP/1.1\r\nHost: "+host+"\r\nContent-Length: "+length_b+"\r\nContent-Type: application/x-wwww-form-urlencoded\r\nAccept: */*\r\nConnection: close\r\n\r\n"+enargs

        # Send and receive data
        self.socket.sendall(request6.encode())
        time.sleep(.100)
        self.socket.shutdown(socket.SHUT_WR)
        data_byte = self.socket.recv(4096)
        data = data_byte.decode()
        time.sleep(.100)
        self.close()

        code_index = data.find("HTTP") + 8
        code_index_end = code_index + 4
        code_str = data[code_index:code_index_end:1]
        code = int(code_str)

        index_body = data.find("{")
        body_str = data[index_body::]
        print(data)
        body = body_str
        
        return HTTPResponse(code, body)
        

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
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
