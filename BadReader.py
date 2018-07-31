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

## @file BadReader.py
#  @author Heartbroken-Git
#  @copyright Apache License 2.0
#  @brief Main file for a sandbox program to experiment reading and writing on a SLE4442 "smart" card
#  @note BadReader's dependencies are the pcscd pcsc-tools libpcsclite1 libpcsclite-dev pyscard packages
#  @version PoC 2

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString
from smartcard.Exceptions import CardRequestTimeoutException
import BRutils as utils
import BRcommands as cmds

## @brief Function responsible for handling the pseudo prompt used by BadReader
#  @details Displays the prompt, parses the user's input and executes the requested command
#  @param cardService a CardService object from the smartcard module with a currently active connection to a card
#  @return STATUS_PROMPT_DISCONNECTED if the user is exiting the prompt but just to disconnect the card and potentially to connect to another one
#  @return STATUS_PROMPT_EXITING if the user requested complete exit from the program
#  @todo Maybe protect the getReader() call with a try..except clause if the cardService does not actually have a connection
#  @todo Color the special messages and maybe emphasize the prompt in some way
#  @todo Seperate the actual call to the help command and add a message stating when a command is not recognized (such as with typos)
def enterPrompt(cardService):
	requestedExit = False
	requestedDisconnect = False
	cardReader = cardService.connection.getReader() # TODO : to be protected by try..except clause if cardService not connected

	while not requestedExit:

		cmdIn = input(cardReader + " >>> ") # or any other prompt-like thing
		cmdList = cmdIn.split()

		if cmdList[0] == "disconnect":
			requestedDisconnect = True
			requestedExit = True # Required to exit the prompt for reconnection as is
			cmds.Disconnect.execute(cardService, cmdList)
		elif cmdList[0] == "exit":
			if not requestedDisconnect:
				print("Disconnecting card before exiting") # TODO : Yellow ?
				cmds.Disconnect.execute(cardService, cmdList)
			print("Exiting")
			requestedExit = True
		elif cmdList[0] == "getATR":
			cmds.GetATR.execute(cardService, cmdList)
		elif cmdList[0] == "read":
			cmds.Read.execute(cardService, cmdList)
		else: # default to help()
			cmds.Help.execute(cardService, cmdList) # TODO : add specific message when there's a typo ?

	if requestedDisconnect:
		return utils.const.STATUS_PROMPT_DISCONNECTED
	else:
		return utils.const.STATUS_PROMPT_EXITING

## @brief Function responsible for the connection to the card
#  @details Tries to connect to a card by using the parameters provided by a given CardRequest object until it actually does connect or is stopped (CTRL+C)
#  @param cardRequest a CardRequest object from the smartcard module with at least a timeout and cardType set up as parameters
#  @return A CardService object with the active connection once connected to the first card available
def attemptConnection(cardRequest):

	stillWaiting = True

	print("Waiting for card insertion", flush=True, end='')

	while stillWaiting:
		try:
			stillWaiting = False
			print(".", flush=True, end='')
			cardService = cardRequest.waitforcard()
		except CardRequestTimeoutException:
			stillWaiting = True

	print("!")
	cardService.connection.connect()
	reader = cardService.connection.getReader()
	cardATR = toHexString(cardService.connection.getATR())

	print("Successfully connected on reader", reader)
	print("Card ATR showing", cardATR)

	return cardService

## @brief Main function for BadReader, start point for everything
#  @todo Protect the card against brutal exits (CTRL+Cs) once in the prompt by catching the KeyboardInterruptError
def main():

	mainCardType = AnyCardType()
	mainCardRequest = CardRequest(timeout=1, cardType=mainCardType)

	# Introduction
	print("Bad Reader, PoC2")
	print("By Heartbroken-Dev, licensed under Apache-2.0")

	while True: # Pseudo do: .. while()

		# Attempt to connect to a card
		mainCardService = attemptConnection(mainCardRequest)

		promptStatus = enterPrompt(mainCardService)

		if promptStatus == utils.const.STATUS_PROMPT_EXITING:
			break

if __name__ == '__main__':
	main()
