#!/usr/bin/python

import socket
from serverAPI import *


s = socket.socket()
host = socket.gethostname()
port = 12345 
s.bind((host, port))


while True:
    s.listen(5)
    c, addr = s.accept()
    print '\n#=> New request from\n', addr

    mesg = c.recv(1024)

    if(mesg == 'mdf'):
        callMDF();
    elif(mesg == 'q'):
        print '\tKILL, terminating: ', addr
        c.close()
    else:
        print 'No match for: '+mesg    

c.close()

