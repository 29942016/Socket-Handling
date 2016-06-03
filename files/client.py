#!/usr/bin/python

import socket

host = socket.gethostname()
port = 12345
passkey = ""
command = ""

# 'Send a command
def sendpacket(request):
    s = socket.socket()
    s.connect((host,port))
    s.send(request)
    result = s.recv(1024)
    s.close()
    return result


# 'Password for send and recieving commands
def getpasskey():
    global passkey
    passkey = raw_input("Authenticate: ")
    passkey += '.'
    print passkey


# '============== Main ================
getpasskey()

# 'Pass packet to server
while(command != 'q'):
    command = passkey + raw_input(">> ")
    print "SENT: " + command

    # 'Error handling the servers response
    if(sendpacket(command) == '1'):
        print 'Bad passkey.'
        getpasskey()



