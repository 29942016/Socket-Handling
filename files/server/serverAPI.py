#!/usr/bin/python

import os
import subprocess
import hashlib
import socket

# ' Define server password here
key = "admin"
# ' Hash the key
password = (hashlib.md5(key).hexdigest())

# ' Constructor method for API
def syscall(command):
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out

# ' API Functions
def portprobe(pNum):
    #' make sure port is a int
    try:
        pNum = int(pNum)
    except ValueError as e:
        return "Invalid port " + `e`
    #' make sure its in common port range
    if(pNum <= 65535 and pNum > 0):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        isOpen = s.connect_ex(('127.0.0.1', int(pNum)))
        if(isOpen == 0):
            return "Port " + `pNum` + " is OPEN"
        else:
            return "Port " + `pNum` + " is CLOSED"
    else:
        return "Selected port out of bounds. 0-65535"

def callMDF():
   return syscall("df -h | awk '{print $5 \"\t\" $3 \"/\" $4 \"\t | \" $1}' | grep -v tmpfs")

def whoAmiI():
    return syscall('whoami')

def services():
    return syscall('service --status-all | grep +')

def listusers():
    return syscall('w')

def showhelp():
    commandList = "\nMaintainence" \
                  "\n portprobe\t| check if a port is open. e.g portprobe <port number>" \
                  "\n mdf\t\t| Returns a custom diskspace report." \
                  "\n whoami\t\t| Returns the owner of the server daemon." \
                  "\n users\t\t| Returns active terminal sessions on the server." \
                  "\n services\t| Returns the currently enabled services. (Can conflict with SEL.)" \
                  "\n\nMisc" \
                  "\n help\t\t| Returns this information." \
                  "\n q\t\t| Terminates the client.\n"

    return commandList



# ' Determines if the supplied password matches server password
# ' Returns command array which contains command+arguement
def authenticate(message):
        print 'DEBUG: ', message
        data = str.split(message,' ')
        key = hashlib.md5(data[0]).hexdigest()

        command = list()
        command.append(data[1])

        # Check if an arguement was passed with command
        if(len(data) > 2):
            command.append(data[2])
        else:
            command.append("")

        print "Key: " + key + " | Command: " + command[0] + " arg:" + command[1]

        if(key == password):
            print 'PASSWORD OK!'
            return command
        else:
            print 'PASSWORD BAD!'
            return False
