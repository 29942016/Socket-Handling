#!/usr/bin/python

import os
import subprocess
import hashlib

# ' Define server password here
key = "admin"
# ' Hash the key
password = (hashlib.md5(key).hexdigest())

def callMDF():
    proc = subprocess.Popen(["df -h | awk '{print $5 \"\t\" $3 \"/\" $4 \"\t | \" $1}' | grep -v tmpfs"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out

def whoAmiI():
    proc = subprocess.Popen(['whoami'], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out

def checkStatus():
    return

# ' Determines if the supplied password matches server password
def authenticate(message):
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
