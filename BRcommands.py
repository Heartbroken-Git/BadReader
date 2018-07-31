#!/usr/bin/python3

# Copyright 2018 Heartbroken-Git
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## @file BRcommands.py
#  @author Heartbroken-Git
#  @copyright Apache License 2.0
#  @brief File containing the set of commands recognized by Bad Reader
#  @version PoC 2

from time import sleep
import BRutils as utils
from smartcard.util import toHexString, toBytes, toASCIIString

# While I wrap my head around Abstract classes for Python let's assume all classes are "well-made"


## @brief Class defining the command to disconnect a card from a reader
#  @details Contains both a description for the help command and the actual command in the form of the implemented execute() function
class Disconnect:

    helpDesc = "disconnect : disconnects the current card, giving the user five (5) seconds to remove the currently plugged in card before reattempting connection."

    ## @brief Public implementation of the execute() method to disconnect a card from its reader
    #  @param cardService a CardService object containing the card's connection to be disconnected
    #  @param cmdList a list of the actual commands typed by the user, currently unused
    #  @todo Add some way to check if the disconnection worked and to protect against disconnecting an unconnected CardService object
    #  @todo Color the messages
    def execute(cardService, cmdList):
        print("Disconnecting card...")
        cardService.connection.disconnect() # TODO : should be checked to have worked if possible
        print("Successfully disconnected !") # TODO : Green ?
        sleep(5)

## @brief Class defining the command to exit BadReader
#  @details Contains a description for the help command and a currently unimplemented execute() method
#  @warning The execute() method is currently unimplemented as it is not used in actually exiting from the program. It thus raises an exception if called.
class Exit:

    helpDesc = "exit : neatly closes the prompt, disconnecting the current card beforehand if need be."

    ## @brief Unimplemented execute() method
    #  @exception NotImplementedError This method is currently unimplemented as it is unused right now
    def execute(cardService, cmdList):
        raise NotImplementedError # empty function, currently all done in main

## @brief Class defining the command to display the help message containing all of the recognized commands
#  @details Contains a help message for itself as well and an implementation of the execute() method displaying the help messages of the various commands
class Help:

    helpDesc = "help : displays this help message."

    ## @brief Public implementation of the execute() method to display the help messages of all the commands recognized by BadReader
    #  @details Prints each command's help description in alphabetical order
    #  @param cardService unused parameter
    #  @param cmdList unused parameter
    #  @todo Make display a specific help message for read and write
    def execute(cardService, cmdList):
        print('\t' + Disconnect.helpDesc)
        print('\t' + Exit.helpDesc)
        print('\t' + GetATR.helpDesc)
        print('\t' + Help.helpDesc)
        print('\t' + Read.helpDesc)

## @brief Class defining the command to display the current card's ATR
#  @details Contains a description for the help command and an implementation of the execute() method to display the card's Answer To Reset
class GetATR:

    helpDesc = "getATR : prints out the current card's Answer To Reset."

    ## @brief Public implementation of the execute() method to display the given card's ATR
    #  @param cardService a CardService object with a connection to a card whose ATR to display
    #  @param cmdList a list of the commands actually entered by the user, currently unused
    #  @todo Ensure that the cardService object actually has a connection or protect against cases where it doesn't
    def execute(cardService, cmdList):
        print(toHexString(cardService.connection.getATR())) # TODO : Check that there actually is a connection in the CardService object

## @brief Class defining the command to display the current card's content
#  @details Contains a description for the help command and an implementation of the execute() method to display the card's content
#  @todo Improve the help description look
#  @todo Write a specific detailed help display function to be used by "help read"
class Read:

    helpDesc = "read : read the current card's content, see \"help read\" for details" # TODO : emphasize in some way the "help read" command

    ## @brief Public implementation of the execute() method to read a card's content
    #  @details Parses the command entered by the user in the prompt to check if it should translate to ASCII or not and to retrieve the first address to read and the length
    #  @note If no length is given then will read the card until its end
    #  @param cardService a CardService object with a connection to the card to read
    #  @param cmdList the list of commands entered by the user
    def execute(cardService, cmdList):

        if cmdList[1] == "--ascii":
            startAddrHex = int(hex(int(cmdList[2])),16)

            if len(cmdList) == 4: # check if length set or should read all
                readLenHex = int(hex(int(cmdList[3])),16)
            else:
                readLenHex = int(hex(256 - int(cmdList[2])),16)

            displayAscii = True

        else:
            startAddrHex = int(hex(int(cmdList[1])),16)

            if len(cmdList) == 3: # check if length set or should read all
                readLenHex = int(hex(int(cmdList[2])),16)
            else:
                readLenHex = int(hex(256 - int(cmdList[1])),16)

            displayAscii = False

        apdu = utils.apdu.READ_MEMORY_CARD + [startAddrHex] + [readLenHex]
        response, sw1, sw2 = cardService.connection.transmit(apdu)

        if displayAscii:
            print(toASCIIString(response))
        else:
            print(toHexString(response))
        print("SW : " + hex(sw1) + " " + hex(sw2))
