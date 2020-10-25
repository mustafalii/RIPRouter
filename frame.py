# Class to define Frame object
# Frame consists of:
#   - Interface number
#   - Src and Dest mac address
#   - Src and Dest IP address
#   - Protocol tag
#   - Payload

class Frame:
    def __init__(self, interfaceNum, srcMacAddr, destMacAddr, srcIpAddr, destIpAddr, protocolTag, payload):
        self.interfaceNum = interfaceNum
        self.srcMacAddr = srcMacAddr
        self.destMacAddr = destMacAddr
        self.srcIpAddr = srcIpAddr
        self.destIpAddr = destIpAddr
        self.protocolTag = protocolTag
        self.payload = payload
