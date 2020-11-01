import re 

class Interface:
    def __init__(self, interfaceNum = "-1", macAddr = "", ipAddr = "", subnetMask = ""):
        self.interfaceNum = interfaceNum
        self.macAddr = macAddr
        self.ipAddr = ipAddr
        self.subnetMask = subnetMask
        self.CIDR = 0           # number of bits to compare with ip address
        self.networkBits = ''
        if self.interfaceNum != "-1":
            self.calcCIDR()
            self.calcNetworkBits()

    # convert ipAddr to binary
    # count number of 1s to get CIDR value
    def calcCIDR(self):
        tokens = self.subnetMask.split('.')
        for token in tokens:
            binary = bin(int(token))
            self.CIDR += binary.count("1")
            
    # get the network bits
    # convert ipAddr to binary 
    # get first CIDR bits
    def calcNetworkBits(self):
        tokens = self.ipAddr.split('.')
        for token in tokens:
            binary = format(int(token), '08b') # formats segment into 8bit binary
            self.networkBits += binary
        self.networkBits = self.networkBits[0:self.CIDR]