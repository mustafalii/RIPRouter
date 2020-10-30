import sys
import os
from router import Router
from frame import Frame
from interface import Interface

# Configures our router based on the configuration file given
def configureRouter(router, config):   
    for line in config:
        tokens = line.split()
        interface = Interface(tokens[0], tokens[1], tokens[2], tokens[3])
        router.addInterface(interface)
        
def getIpAddrBinary(ipAddr, CIDR):
    tokens = ipAddr.split('.')
    result = ""
    for token in tokens:
        binary = format(int(token), '08b') # formats segment into 8bit binary
        result += binary
    result = result[0:CIDR]
    return result
        
if __name__ == '__main__':
    print("Configuring router...")
    configFile = sys.argv[1]
    myRouter = Router()
    with open(configFile) as file:
        lines = file.readlines()
        configureRouter(myRouter, lines)
    print("Finished router configuration.\n")
    
    while(True):  # start getting frames from stdin
        frameString = input("Enter incoming frame: \n")
        tokens = frameString.split()
        myFrame = Frame(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4], tokens[5], tokens[6]) # our current frame
        if myFrame.protocolTag == "0":
            # we are in forwarding mode
            if myFrame.destMacAddr == "FF:FF:FF:FF:FF:FF":
                print("Frame dropped because it's an broadcast.\n")
            else:
                destInterfaceMac = Interface()
                destInterfaceIP = Interface()
                for interface in myRouter.interfaceList:
                    if myFrame.destMacAddr == interface.macAddr: # dest MAC matches our interface, need to check ip
                        destInterfaceMac = interface
                        break
                if destInterfaceMac.interfaceNum == "-1":
                    print("Frame dropped because destination MAC address does not belong to us.\n")
                else:
                    for interface in myRouter.interfaceList:
                        if getIpAddrBinary(myFrame.destIpAddr, interface.CIDR) == interface.ipAddrBin:
                            destInterfaceIP = interface
                            break
                    if destInterfaceIP.interfaceNum == "-1":
                        # do nothing because destination MAC addr does not belong to us
                        pass
                    elif destInterfaceIP.interfaceNum == destInterfaceMac.interfaceNum:
                        print("Frame dropped because the IP destination is connected to the same interface.\n")
                    else:
                        print(destInterfaceIP.interfaceNum + " " + destInterfaceIP.macAddr + " FF:FF:FF:FF:FF:FF " + myFrame.srcIpAddr
                              + " " + myFrame.destIpAddr + " 0 " + myFrame.payload + "\n")
        elif myFrame.protocolTag == "1":
            # we are in rip update mode
            pass
            
