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

    # Handle if we got an stderr or stdout, return the correct one.
    if err is None:
        return out
    else:
        return err

# ' API Functions

# NAS control
def nasControl(status):
    #Make sure hubcontrol is installed: https://github.com/codazoda/hub-ctrl.c
    if(hubCtrlCheckInstalled()):
        if(status == "on"):
            return "Switching on..."
        elif(status == "off"):
            return "Switching off"
        else:
            return "Invalid option: " + `status`
    else:
        return "Please install hub-ctrl at https://github.com/codazoda/hub-ctrl.c"




# Run a rsync backup
def backup(src, dest):
    return syscall("nohup rsync -av " + `src` + " " + `dest` + " --exclude={/mnt,/dev,/sys,/proc} >> /tmp/output.txt &")

# Checks if port is open
def portprobe(pNum):
    # make sure port is a int
    if(validatePort(pNum)):
        pNum = int(pNum)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        isOpen = s.connect_ex(('127.0.0.1', pNum))

        if(isOpen == 0):
            return `pNum` + " is OPEN"
        else:
            return `pNum` + " is CLOSED"
    else:
        return "Invalid port."

# modifies port status
def portmod(pNum, status):
    if(uid() == 0):
        if(validatePort(pNum)):
            pNum = int(pNum)
            status = str.lower(status)

            if(status == 'accept' or status == 'a' or status == 'allow' or status == 'add'):
                status = 'A'
            elif(status == 'deny' or status == 'd' or status == 'deny' or status == 'delete'):
                status = 'D'
            else:
                return "Invalid syntax, specify (a)ccept or (d)eny"

            # Attempt to modify iptables
            val = "iptables -" + `status` + " INPUT -p tcp --dport " + `pNum` + " -j ACCEPT"
            return "Altered port " + `pNum` + "\n" + syscall(val)
        else:
            return "Invalid port."
    else:
        return "Cannot run this command without root permissions."

# disk usage
def callMDF():
   return syscall("df -h | awk '{print $5 \"\t\" $3 \"/\" $4 \"\t | \" $1}' | grep -v tmpfs")

# Server owner
def whoAmiI():
    return syscall('whoami')

def uid():
    return int(syscall('id -u'))

# List of services
def services():
    return syscall('service --status-all')

# Active terminals
def listusers():
    return syscall('w')

# Show help
def showhelp():
    commandList = "\nMaintainence" \
                  "\n portprobe\t| check if a port is open. e.g portprobe <port number>" \
                  "\n portmod\t| Open or close a port. e.g portmod <port number> <add/delete>" \
                  "\n mdf\t\t| Returns a custom diskspace report." \
                  "\n whoami\t\t| Returns the owner of the server daemon." \
                  "\n users\t\t| Returns active terminal sessions on the server." \
                  "\n services\t| Returns the currently enabled services. (Can conflict with SEL.)" \
                  "\n\nMisc" \
                  "\n help\t\t| Returns this information." \
                  "\n q\t\t| Terminates the client.\n"

    return commandList

# ' Determines if the supplied password matches server password
# ' If correct, returns command["command", "arguement"]
def authenticate(message):
        data = str.split(message,' ')
        key = hashlib.md5(data[0]).hexdigest()

        command = list()
        command.append(data[1])

        # Check if arguement(s) were passed with command
        if(len(data) > 2):
            for count,item in enumerate(data):
                if(count >= 2):
                    command.append(data[count])
        else:
            command.append("")

        print "Key: " + key + " | Command: " + command[0] + " arg:" + command[1]

        if(key == password):
            print 'PASSWORD OK!'
            return command
        else:
            print 'PASSWORD BAD!'
            return False

def validatePort(pNum):
    try:
        pNum = int(pNum)
    except ValueError as e:
        return False
    # make sure its in common port range
    if (pNum <= 65535 and pNum > 0):
        return True
    else:
        return False

# Check if we have a binary for hub-controller
def hubCtrlCheckInstalled():
    val = syscall("whereis hub-ctrl | cut -d':' -f2")

    if len(val) <= 1:
        return False
    else:
        return True
