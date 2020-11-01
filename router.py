# Class to define Router object
# Router contains a count of interfaces, a list of interfaces, and a routing table
from interface import Interface

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
        dest_entry = destinationAddr + '/' + str(CIDR)  # @TODO: instead of the original ip, store only the network number e.g. instead of 192.168.3.1/24 we store 192.168.3.0/24
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