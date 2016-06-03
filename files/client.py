#!/usr/bin/python

import socket

#Bind IP:Port to our sender

host = socket.gethostname()
port = 12345
command = ""


def sendpacket(toPass):
    s = socket.socket()
    s.connect((host,port))
    s.send(toPass)
    s.close


#Pass packet to server
while(command != 'q'):
    command = raw_input(">> ")
    sendpacket(command)

