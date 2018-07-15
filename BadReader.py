#!/usr/bin/python3

# Bad Reader
# A sandbox program to experiment reading and writing on a SLE4442 "smart" card
# Author : Heartbroken-Dev
# License : Apache License 2.0
# Dependencies : pcscd pcsc-tools libpcsclite1 libpcsclite-dev pyscard
# Version : Proof of concept

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString 
from smartcard.Exceptions import CardRequestTimeoutException
from time import sleep

def attemptConnection(cardRequest):

	stillWaiting = True
	
	print("Waiting for card insertion", flush=True, end='')
	
	while(stillWaiting):
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

def main():
	
	mainCardType = AnyCardType()
	mainCardRequest = CardRequest(timeout=1, cardType=mainCardType)

	# Introduction
	print("Bad Reader, PoC")
	print("By Heartbroken-Dev, licensed under Apache-2.0")

	# Attempt to connect to a card
	mainCardService = attemptConnection(mainCardRequest)

	# automatic disconnecting for PoC test
	print("Now disconnecting in 5 s")
	sleep(5)
	mainCardService.connection.disconnect()
	print("Card disconnected, can now be safely removed")
	
if __name__ == '__main__':
	main()
