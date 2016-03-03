# -*- coding: UTF-8 -*-

import SocketServer
import time

class MyHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        print 'get connection from :',self.client_address
        while True:
            try:
                data = self.request.recv(4096)
                print 'receive data:',data
                if not data:
                    print 'break connection!'
                    break
                else:
                    action,filename = data.split('#')
                    if action == 'put':
                        self.recvfile('d:\\data1\\'+filename)
                    else:
                        print 'receive error!'
                        continue
            except Exception,e:
                print 'error:',e
                break

    def recvfile(self,filename):
        print "start receiving!"
        f = open(filename, 'wb')
        self.request.send('ready')
        while True:
            data = self.request.recv(4096)
            if data == 'EOF':
                print 'recv file success'
                break
            f.write(data)
        f.close()

if __name__ == "__main__":
    host = ''
    port = 1234
    s = SocketServer.TCPServer((host,port),MyHandler)
    s.serve_forever()