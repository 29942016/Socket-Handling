#!/usr/bin/python
import sys
import socket
from serverAPI import *

s = socket.socket()
host = socket.gethostname()
port = 12345

s.bind((host, port))
print 'Session passkey: ' + password


while True:
    s.listen(5)
    c, addr = s.accept()
    print '\n#=> New request from\n', addr
    mesg = c.recv(1024)

    result = authenticate(mesg)
    if(result != False):
        if(result == 'mdf'):
            callMDF()
            c.send('OK!')
        elif(result == 'whoami'):
            whoAmiI()
            c.send('OK!')
        elif(result == 'q'):
            print '\tKILL, terminating: ', addr
            c.close()
        else:
            print 'No match for: '+result
            c.send('BAD!')
    else:
        c.send('1')  # bad password

c.close()

