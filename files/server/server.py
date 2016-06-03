#!/usr/bin/python
import sys
import socket
from serverAPI import *

s = socket.socket()
host = socket.gethostname()
port = 12345

s.bind((host, port))
print 'Attempting to bind to host:', host, ' on port:', port
print 'Session passkey: ' + password


while True:
    s.listen(5)
    c, addr = s.accept()
    print '\n#=> New request from', addr
    mesg = c.recv(1024)

    # 'Check if users passkey is correct
    result = authenticate(mesg)
    if(result != False):
        # 'call the function they wanted.
        if(result == 'mdf'):
            c.send(callMDF())
        elif(result == 'whoami'):
            c.send(whoAmiI())
        elif(result == 'q'):
            print '\tKILL, terminating: ', addr
            c.send('2')
        elif(result == 'help'):
            c.send(showhelp())
        else:
            c.send('Command not found.')
    else:
        c.send('1')  # bad password

c.close()
