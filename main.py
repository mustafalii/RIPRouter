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

def emitRIPUpdates(router):
    updates = ''
    for entry in router.routing_table.keys():
        updates = updates + entry + "," + str(router.routing_table[entry][0]) + " "
    for interface in router.interfaceList:
        ripUpdate = interface.interfaceNum + " " + interface.macAddr + " FF:FF:FF:FF:FF:FF " \
            + interface.ipAddr + " 255.255.255.255 " + " 1 " + updates 
        print(ripUpdate)

def getNextHopAddr(frame, router):
    if frame.srcMacAddr in [interface.macAddr for interface in router.interfaceList]:
        nextHopAddr = 'FF:FF:FF:FF:FF:FF'
    else:
        nextHopAddr = frame.srcMacAddr
    return nextHopAddr

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
            frameString = input()
        except EOFError:
            print("Read all of input. Exiting...")
            # sys.stdin.close()
            # sys.stdin = open('/dev/tty', 'r')
            # continue
            exit() # we can quit after piping input
        tokens = frameString.split()
        if (len(tokens) >= 6):
            myFrame = Frame(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4], tokens[5], tokens[6]) # our current frame
        else:
             myFrame = Frame(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4], tokens[5])
        
        # Basic data
        if myFrame.protocolTag == "0":
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
                #@TODO: Do longest prefix matching (We might already be done with this?)
                # - iterate through the routing table;
                # - keep track of all matches 
                # - if there are multiple matches, choose longest prefix one
                # - rest is the same
                for entry in myRouter.routing_table.keys():
                    candidateDest = entry.split('/')    # split <ipAddr>/<cidr> on '/'
                    candidateNetwork = getNetworkBits(candidateDest[0], candidateDest[1])
                    if getNetworkBits(myFrame.destIpAddr, candidateDest[1]) == candidateNetwork:
                        _, nextHopAddr, nextHopInterface = myRouter.routing_table[entry]
                        srcMacAddr = myRouter.getMacAddrByInterfaceNum(nextHopInterface)    # get mac address from interface number
                        print(nextHopInterface, srcMacAddr, nextHopAddr, myFrame.srcIpAddr, myFrame.destIpAddr, myFrame.protocolTag, myFrame.payload) 
                        forwarded = True
                        break
                if not forwarded:
                    print("Frame dropped: No corresponding entry in routing table.\n")
        
        # RIP update
        elif myFrame.protocolTag == "1":
            updated = False
            # iterate over all received updates
            for updateAddrCidrDest in tokens[6:]:
                addrCidr, newMetric = updateAddrCidrDest.split(',')     # split address/cidr and metric
                routingTableEntries = myRouter.routing_table.keys()
                for entry in routingTableEntries:
                    # check if entry exists in routing table
                    receivedNetworkBits = getNetworkBits(addrCidr.split('/')[0], addrCidr.split('/')[1])
                    candidateNetworkBits = getNetworkBits(entry.split('/')[0], entry.split('/')[1])
                    if receivedNetworkBits == candidateNetworkBits:
                        updated = True
                        # if new metric is better
                        # or if new metric is worse but frameSrc == nextHopAddr 
                        # then we update
                        if (int(newMetric) < int(myRouter.routing_table[entry][0])) or \
                            ((int(newMetric) > int(myRouter.routing_table[entry][0])) and (myFrame.srcMacAddr == myRouter.routing_table[entry][1])):
                            nextHopAddr = getNextHopAddr(myFrame, myRouter)
                            myRouter.routing_table[addrCidr] = [newMetric, nextHopAddr, myFrame.interfaceNum]   # add new entry
                            break
                # if entry not found in routing table, then add it
                if not updated:
                    nextHopAddr = getNextHopAddr(myFrame, myRouter)
                    myRouter.routing_table[addrCidr] = [newMetric, nextHopAddr, myFrame.interfaceNum]
                updated = False

            # emit updates on each of the of interfaces. See lecture
            emitRIPUpdates(myRouter)
            printRoutingTable(myRouter)
        
        # RIP Request
        elif myFrame.protocolTag == "2":
            emitRIPUpdates(myRouter)
        