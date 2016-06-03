#!/usr/bin/python

import os;
import hashlib

password = (hashlib.md5("admin").hexdigest())

def callMDF():
    os.system("df -h | awk '{print $5 \"\t\" $3 \"/\" $4 \"\t | \" $1}' | grep -v tmpfs")

def authenticate(message):
        data = str.split(message,'.')
        key = hashlib.md5(data[0]).hexdigest()
        command = data[1]

        print "Key: " + key + " | Data: " + command

        if(key == password):
            print 'Authentication sucessful'
            return command
        else:
            print 'Wrong credientials'
            return False
