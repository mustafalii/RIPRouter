# Class to define Router object
# Router contains a count of interfaces and a list of interfaces

from interface import Interface

class Router:
    def __init__(self):
        self.nums = 0
        self.interfaceList = []
        
    def addInterface(self, Interface):
        self.interfaceList.append(Interface)
        self.nums += 1
        