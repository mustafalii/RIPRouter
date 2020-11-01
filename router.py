# Class to define Router object
# Router contains a count of interfaces, a list of interfaces, and a routing table
from interface import Interface
import re

class Router:
    def __init__(self):
        self.nums = 0
        self.interfaceList = []
        
        # routing table has a dictionary structure:
        # { <ipaddr/cidr> : [<metric>, <nextHopAddr>, <nextHopInterface>] }
        self.routing_table = {}

    def addInterface(self, interface):
        self.interfaceList.append(interface)
        self.nums += 1
        # update routing table
        destinationAddr = interface.ipAddr
        CIDR = interface.CIDR
        # instead of the original ip, store only the network number e.g. instead of 192.168.3.1/24 we store 192.168.3.0/24
        dest_entry = calculateNetworkAddr(destinationAddr, CIDR) + '/' + str(CIDR) 
        nextHopMacAddr = 'FF:FF:FF:FF:FF:FF'
        nextHopInterface = interface.interfaceNum
        # example of an entry: {192.168.3.0/24: [1, FF:FF:FF:FF:FF:FF, 0]}
        self.routing_table[dest_entry] = [1, nextHopMacAddr, nextHopInterface]
    
    def updateRoutingTable(self, interface):
        pass

    def getMacAddrByInterfaceNum(self, interfaceNumber):
        interface = self.interfaceList[int(interfaceNumber)]
        return interface.macAddr

    def getInterfaceByMacAddr(self, macAddr):
        for interface in self.interfaceList:
            if interface.macAddr == macAddr:
                return interface
        return None

def calculateNetworkAddr(ipAddr, CIDR):
    tokens = ipAddr.split('.')
    networkBits = ""
    for token in tokens:
        binary = format(int(token), '08b') # formats segment into 8bit binary
        networkBits += binary
    networkBits = networkBits[0:int(CIDR)] + str('0' * (32-int(CIDR)))
    bitGroups = re.findall("[01]{8}", networkBits)
    networkAddr = ''
    for group in bitGroups:
        networkAddr = networkAddr + str(int(str(int(group)), 2)) + '.'
    networkAddr = networkAddr[:len(networkAddr)-1]  # truncate last dot
    return networkAddr
