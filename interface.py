class Interface:
    def __init__(self, interfaceNum = "-1", macAddr = "", ipAddr = "", subnetMask = ""):
        self.interfaceNum = interfaceNum
        self.macAddr = macAddr
        self.ipAddr = ipAddr
        self.subnetMask = subnetMask
        self.CIDR = 0           # number of bits to compare with ip address
        self.ipAddrBin = ""  # string of ip address to compare in binary using CIDR
        if self.interfaceNum != "-1":
            self.calcSubnetMask()
            self.calcIpAddrBinary()
    
    def calcSubnetMask(self):   # gets the CIDR value by converting each segment to binary and counting 1s
        tokens = self.subnetMask.split('.')
        for token in tokens:
            binary = bin(int(token))
            self.CIDR += binary.count("1")
            
    def calcIpAddrBinary(self):
        tokens = self.ipAddr.split('.')
        for token in tokens:
            binary = format(int(token), '08b') # formats segment into 8bit binary
            self.ipAddrBin += binary
        self.ipAddrBin = self.ipAddrBin[0:self.CIDR]