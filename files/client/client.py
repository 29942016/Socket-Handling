#!/usr/bin/python
from clientAPI import *

def main():
    print 'Connecting to ', host + ':' + `port`
    passkey = getpasskey()

    # 'Pass packet to server
    while(True):
        # 'handling the servers response
        result = sendpacket(passkey + raw_input("[CLIENT] >> "))

        if(result == '1'):  # 'Using wrong passkey
            print 'Bad passkey.'
            getpasskey();
        elif(result == '2'):  # 'User terminates connection
            print 'Terminating.'
            exit()
        else:
            print result


main()