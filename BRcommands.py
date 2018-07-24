#!/usr/bin/python3

# Set of commands recognized by Bad Reader
# Author : Heartbroken-Dev
# License : Apache License 2.0
# Version : PoC 2

from time import sleep
from smartcard.util import toHexString

# While I wrap my head around Abstract classes for Python let's assume all classes are "well-made"

class Disconnect:

    helpDesc = "disconnect : disconnects the current card, giving the user five (5) seconds to remove the currently plugged in card before reattempting connection."

    def execute(cardService, cmdList):
        print("Disconnecting card...")
        cardService.connection.disconnect() # TODO : should be checked to have worked if possible
        print("Successfully disconnected !") # TODO : Green ?
        sleep(5)

class Exit:

    helpDesc = "exit : neatly closes the prompt, disconnecting the current card beforehand if need be."

    def execute(cardService, cmdList):
        raise NotImplementedError # empty function, currently all done in main

class Help:

    helpDesc = "help : displays this help message."

    def execute(cardService, cmdList):
        print('\t' + Disconnect.helpDesc)
        print('\t' + Exit.helpDesc)
        print('\t' + Help.helpDesc)
        print('\t' + GetATR.helpDesc)

class GetATR:

    helpDesc = "getATR : prints out the current card's Answer To Reset."

    def execute(cardService, cmdList):
        print(toHexString(cardService.connection.getATR()))
