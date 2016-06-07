import hashlib
import socket

from subproc import syscall
from errorHandling import *

# ' Define server password here.
key = "admin"
# ' Hash the key for comparison with the client.
password = (hashlib.md5(key).hexdigest())

# ' API Functions
def init(host, port):
    print "\nStarting server:\t" + `host` + ":" + `port`
    print "Passkey:\t\t", key
    print "Hashed Passkey:\t\t", password
    print "Awaiting connections..."

# usb device controller
def usbController(status, hub, port):
    #Make sure hubcontrol is installed: https://github.com/codazoda/hub-ctrl.c
    preCheck = hubCtrlCheck(hub,port)

    if(preCheck != True):
        if(status == "on"):
            print syscall("hub-ctrl -h " + hub + " -P " + port + " -p 1")
            return "Enabled."
        elif(status == "off"):
            print syscall("hub-ctrl -h " + hub + " -P " + port + " -p 0")
            return "Disabled."
        else:
            return "Invalid option: " + `status`
    else:
        return preCheck

# Run a rsync backup
#def backup(src, dest):
#    return syscall("nohup rsync -av " + `src` + " " + `dest` + " --exclude={/mnt,/dev,/sys,/proc} >> /tmp/output.txt &")

# Checks if port is open.
def portprobe(pNum):
    # make sure port is a int.
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

# modifies port status.
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

            # Attempt to modify iptables.
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
                  "\n usb\t\t| Modify power to a usb controller. e.g usb <on/off> <hub> <port>" \
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

        print "Key: " + key + "(" + data[0] + ")\nCommand: " + command[0] + " arg:" + command[1]

        if(key == password):
            print 'OK!'
            return command
        else:
            print 'BAD!'
            return False


