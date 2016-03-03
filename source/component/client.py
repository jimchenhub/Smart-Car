# -*- coding: UTF-8 -*-
import socket
import time
import os

SOURCE_DIR = '/home/pi/Documents/Github/Smart-Car/source/data/'
def sendfile(s,filename):
    print 'send file:',filename
    f = open(SOURCE_DIR + filename,'rb')
    while True:
        data = f.read(4096)
        print data
        if not data:
            break
        s.sendall(data)
    f.close()
    time.sleep(1)
    s.sendall('EOF')
    print 'send successfully!'

def confirm(s, client_command):
    s.send(client_command)
    data = s.recv(4096)
    if data == 'ready':
        return True

def start():
    host = socket.gethostname()
    port = 1234
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host,port))
        for root,dirs,files in os.walk(SOURCE_DIR):
            for filename in files:
                client_command = 'put#'+filename
                print client_command
                action,filename = client_command.split('#')
                if action == 'put':
                    if confirm(s,client_command):
                        sendfile(s,filename)
                    else:
                        print 'server error!'
                else:
                    print "command error!"
    except socket.error,e:
        print "get error as",e
    finally:
        s.close()

if __name__ == "__main__":
    start()




