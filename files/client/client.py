#!/usr/bin/python

import socket
import errno

host = socket.gethostname()
port = 12345 
passkey = ""
command = ""

print 'Connecting to ', host, ':', port

# 'Send a command
def sendpacket(request):
    try:
        s = socket.socket()
        s.connect((host,port))
        s.send(request)
        result = s.recv(1024)
        s.close()
        return result
    except socket.error as serr:
        if(serr.errno == 111):  # '111 - Host down
            print 'Failed to connect, server may be unavailable.'
            exit()

# 'Password for sending and recieving commands
# 'request will be hash+.+command
def getpasskey():
    global passkey
    passkey = raw_input("Passkey: ")
    passkey += '.'
    print passkey


# '============== Main ================
getpasskey()

# 'Pass packet to server
while(True):
    command = passkey + raw_input("[CLIENT] >> ")

    # 'handling the servers response
    result = sendpacket(command)
    if(result == '1'):
        print 'Bad passkey.'
        getpasskey();
    elif(result == '2'):
        print 'Terminating.'
        exit()
    else:
        print result



