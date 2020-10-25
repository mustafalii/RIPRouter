# Class to define Router object
# Router consists of:
#   - Number of interfaces
#   - Mac address per interface
#   - IP address per interface
#   - Subnet mask per interface
class Router:
    def __init__(self, interfaceNums=0, macList=[], ipList=[], subnetList=[]):
        self.interfaceNums = interfaceNums
        self.macList = macList
        self.ipList = ipList
        self.subnetList = subnetList
    
    def setInterfaceNums(self, interfaceNums):
        self.interfaceNums = interfaceNums
    
    def addMacAddress(self, macAddr):
        self.macList.append(macAddr)
    
    def addIpAddress(self, ipAddr):
        self.ipList.append(ipAddr)
    
    def addSubnetMask(self, subnet):
        self.subnetList.append(subnet)
