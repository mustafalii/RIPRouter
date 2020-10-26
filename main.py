import sys
import os
from router import Router
from frame import Frame


# Configures our router based on the configuration file given
def configureRouter(router, configurationFileLines):
    router.setInterfaceNums(len(lines))    # Number of interfaces = Number of lines
    for line in configurationFileLines:
        tokens = line.split()
        router.addMacAddress(tokens[1])      
        router.addIpAddress(tokens[2])
        router.addSubnetMask(tokens[3])

if __name__ == '__main__':
    print("Configuring router...")
    configurationFileName = sys.argv[1]
    myRouter = Router()
    with open(configurationFileName) as file:
        lines = file.readlines()
        try:
            configureRouter(myRouter, lines)
        except:
            print("Invalid configuration file")
    print("Finished router configuration\n")
    while(True):
        frameString = input("Enter incoming frame")
