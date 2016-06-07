#!/usr/bin/python
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
        if(result[0] == 'mdf'):
            c.send(callMDF())

        elif(result[0] == 'usb'):
            if (len(result) == 4):
                c.send(usbController(result[1], result[2], result[3]))
            else:
                c.send(invalidparams(3, len(result)-1))

        elif(result[0] == 'portprobe'):
            c.send(portprobe(result[1]))

        elif(result[0] == 'portmod'):
            if(len(result) == 3):
                c.send(portmod(result[1], result[2]))
            else:
                c.send(invalidparams(2, len(result)-1))

        elif(result[0] == 'whoami'):
            c.send(whoAmiI())

        elif(result[0] == 'services'):
            c.send(services())

        elif(result[0] == 'users'):
            c.send(listusers())

        elif(result[0] == 'q'):
            print '\tKILL, terminating: ', addr
            c.send('2')

        elif(result[0] == 'help'):
            c.send(showhelp())

        else:
            c.send('Command not found.')
    else:
        c.send('1')  # bad password

c.close()

