#!/usr/bin/python

import os
import subprocess
import hashlib

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
                  "\n portmod\t| modifies a port. e.g portmod <open/close> <port number>" \
                  "\n mdf\t\t| Returns a custom diskspace report." \
                  "\n whoami\t\t| Returns the owner of the server daemon." \
                  "\n users\t\t| Returns active terminal sessions on the server." \
                  "\n services\t| Returns the currently enabled services. (Can conflict with SEL.)" \
                  "\n\nMisc" \
                  "\n help\t\t| Returns this information." \
                  "\n q\t\t| Terminates the client.\n"

    return commandList



# ' Determines if the supplied password matches server password
def authenticate(message):
        print 'DEBUG: ', message
        data = str.split(message,'.')
        key = hashlib.md5(data[0]).hexdigest()
        command = data[1]

        print "Key: " + key + " | Command: " + command

        if(key == password):
            print 'PASSWORD OK!'
            return command
        else:
            print 'PASSWORD BAD!'
            return False
