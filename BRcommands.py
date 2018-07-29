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
from smartcard.util import toHexString

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
    def execute(cardService, cmdList):
        print('\t' + Disconnect.helpDesc)
        print('\t' + Exit.helpDesc)
        print('\t' + Help.helpDesc)
        print('\t' + GetATR.helpDesc)

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
