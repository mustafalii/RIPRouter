import sys
import os
import re
import math
from router import Router
from frame import Frame
from interface import Interface

# configures our router based on the configuration file given
# configuration format: <interface_num> <mac_addr> <ip_addr> <subnet_mask>
def configureRouter(router, config):   
    for line in config:
        tokens = line.split()
        interface = Interface(tokens[0], tokens[1], tokens[2], tokens[3])
        router.addInterface(interface)
    printRoutingTable(router)
# get the network bits from ipAddr, given the CIDR value
def getNetworkBits(ipAddr, CIDR):
    tokens = ipAddr.split('.')
    networkBits = ""
    for token in tokens:
        binary = format(int(token), '08b') # formats segment into 8bit binary
        networkBits += binary
    networkBits = networkBits[0:int(CIDR)]
    return networkBits
        
# get network bits
# check if inputInterfaceNum == outputInterfaceNum
def destinedToSameSubnet(frame, currInterface):
    inputInterfaceNum = frame.interfaceNum
    if getNetworkBits(frame.destIpAddr, currInterface.CIDR) == currInterface.networkBits and \
        inputInterfaceNum == currInterface.interfaceNum:
        print("Input interface: ", inputInterfaceNum)
        print("Output interface: ", currInterface.interfaceNum)
        return True
    return False

def printRoutingTable(router):
    print("\nROUTING TABLE")
    print("----------------------------------------------")
    for entry in router.routing_table.keys():
        print(entry, router.routing_table[entry])
    print("----------------------------------------------\n")


if __name__ == '__main__':
    print("Configuring router...")
    configFile = sys.argv[1]
    myRouter = Router()
    with open(configFile) as file:
        lines = file.readlines()
        configureRouter(myRouter, lines)
    print("Finished router configuration.\n")
    
    while(True):  
        # get frames from standard input
        # frame format: <interface_number> <src_mac_addr> <dest_mac_addr> <src_ip_addr> <dest_ip_addr> <payload>
        forwarded = False
        try:
            frameString = input("Enter incoming frame:\n")
        except EOFError:
            exit()
        tokens = frameString.split()
        myFrame = Frame(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4], tokens[5], tokens[6]) # our current frame
        if myFrame.protocolTag == "0":  # basic data
            currentInterface = ''
            # find current input interface
            for interface in myRouter.interfaceList:
                if myFrame.destMacAddr == interface.macAddr:
                    currentInterface = interface
                    break
            # ignore frames with invalid destination mac address
            if currentInterface == '':
                print("Frame dropped: Invalid destination mac address")
            # ignore frames that are ethernet broadcast
            elif myFrame.destMacAddr == "FF:FF:FF:FF:FF:FF":
                print("Frame dropped: broadcast message.\n")
            # ignore frames that are destined to the same subnet
            elif destinedToSameSubnet(myFrame, currentInterface):
                print("Frame dropped: destined for same subnet.\n")
            else:
                # iterate through the routing table to check for a match
                for entry in myRouter.routing_table.keys():
                    candidateDest = entry.split('/')    # split <ipAddr>/<cidr> on '/'
                    candidateNetwork = getNetworkBits(candidateDest[0], candidateDest[1])
                    if getNetworkBits(myFrame.destIpAddr, candidateDest[1]) == candidateNetwork:
                        _, nextHopAddr, nextHopInterface = myRouter.routing_table[entry]
                        srcMacAddr = myRouter.getMacAddrByInterfaceNum(nextHopInterface)    # get mac address from interface number
                        print(nextHopInterface, srcMacAddr, nextHopAddr, myFrame.srcIpAddr, myFrame.destIpAddr, myFrame.protocolTag, myFrame.payload + "\n") 
                        forwarded = True
                        break
                if not forwarded:
                    print("Frame dropped: No corresponding entry in routing table.\n")
        
        # RIP update
        elif myFrame.protocolTag == "1":
            updated = False
            # if no updates in input
            if len(tokens) <= 6:
                print("Invalid updates")
            else:
                # iterate over all received updates
                for updateAddrCidrDest in tokens[6:]:
                    addrCidr, newMetric = updateAddrCidrDest.split(',')
                    for addrs in myRouter.routing_table.keys():
                        # if entry exists in routing table
                        if addrCidr == addrs:
                            # if new metric better then update
                            # or if new metric worse but frameSrc == nextHopAddr then update
                             if (int(newMetric) < int(myRouter.routing_table[addrs][0])) | \
                                 ((int(newMetric) > int(myRouter.routing_table[addrs][0])) and (myFrame.srcMacAddr == myRouter.routing_table[addrs][1])):
                                 updated = True
                                 myRouter.routing_table[addrs][0] = newMetric
                                 break
                    # if entry not found in routing table, then add it
                    if not updated:
                        myRouter.routing_table[addrCidr] = [newMetric, myFrame.srcMacAddr, myFrame.interfaceNum]
                    updated = False
                #@TODO:
                # emit updates on each of the of interfaces. See lecture
        elif myFrame.protocolTag == "2":
            # RIP request
            pass
            
        printRoutingTable(myRouter)