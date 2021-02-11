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
#import requests
#import urllib.request

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        #print(type(body))
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        req = urllib.parse.urlparse(url)
        port = req.port
        host = req.hostname
        #print("HEEEEEEEEEERRRRRREEEEEEE")
        #print(url)
        #print(port) 
        #print(host)
        return (host,port)


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
        #code = 500
        body = ""
        (host, port) = self.get_host_port(url)
        #print("TRANSFER")
        print(url)
        #print(host)
        #print(port)
        self.connect(host,port)
        #print("CONNECTED")
        #self.socket.sendall("GET / HTTP/1.1\r\n\r\n")
        
        request1 = '''GET / HTTP/1.1
        Host: '''+str(host)+":"+str(port)+'''/abcdef/gjkd/dsadas
        Referer: '''+url+'''
        
        '''
        print(request1)

        request2 = '''GET / HTTP/1.1
        Host: '''+url+'''
        
        '''

        request3 = ("GET / HTTP/1.1\r\nHost: "+url+"\r\n\r\n")

        self.socket.sendall(request3.encode())
        print("RCVD")
        self.socket.shutdown(socket.SHUT_WR)
        #self.close()
        print("-------------------")
        data = self.socket.recv(4096).decode()
        print(type(data))
        print(data)
        print("-----------------")
        self.close()
        code_index = data.find("HTTP") + 8
        code_index_end = code_index + 4
        code_str = data[code_index:code_index_end:1]
        print("COOOODE STR")
        print(code_str)
        code = int(code_str)
        """
        index_data = str(data)
        index_start = index_data.find("b'") + 2
        index_end = len(index_data) - 1
        body1 = index_data[index_start:index_end:]
        print(body1)
        """
        body = data + url
        print("BOOOODDDY")
        print(body)

        

        #req = urllib.parse.urlparse(url)
        #print(req)
        # here
        """
        r = requests.get(url, headers=args) 
        code = r.status_code
        print("HEEEEEEEEEEEEEEEEEEEEEEEEERE")
        print(code)
        #r.json()
        body = r.content
        print(type(body))
        print(r.content)
        #body = urllib.parse.urlencode(body1)
        #print(body)
        """
        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        #here
        """
        r = requests.post(url, data=args) 
        code = r.status_code
        print("POOOOOOOOOOOOOOOSSSSSSSTT")
        print(code)
        #r.json()
        body = r.content
        print(type(body))
        """
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
