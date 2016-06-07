# Methods for error handling

from subproc import syscall

# Prerequisite check before running hubctrl command
def hubCtrlCheck(hub, port):
    # Check we have access to hub-ctrl binary.
    val = syscall("whereis hub-ctrl | cut -d':' -f2")
    if(len(val) <= 1):
        return "Cannot find hub-ctrl binary."
    # Check the passed hub/port is valid
    elif(type(hub) != int or type(port) != int):
        return "Passed hub/port invalid type."
    else:
        return True

# Check if the port is valid
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

# Check if the user gave the required amount of paramters for the command.
def invalidparams(required, specificied):
        return "\tInvalid amount of paramaters specified, requires: " + `required` + ", given: " + `specificied` + "."
