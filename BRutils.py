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

## @file BRutils.py
#  @author Heartbroken-Git
#  @copyright Apache License 2.0
#  @brief Set of utility functions, variables or constants used by Bad Reader
#  @version PoC 2

## @brief Class containing pesudo constants
class const:

	# Statuses for the prompt
	STATUS_PROMPT_DISCONNECTED = 10
	STATUS_PROMPT_EXITING = 20

## @brief Class containing APDUs to transmit
#  @sa https://hashtips.files.wordpress.com/2013/10/pma-acr38xccid-6-02.pdf
class apdu:
	SELECT_CARD_TYPE = [0xFF,0xA4,0x00,0x00,0x01,0x06]
	READ_MEMORY_CARD = [0xFF,0xB0,0x00] # + byte address of first byte to read + length of data to read (in bytes ?)
	READ_PRESENTATION_ERROR_COUNTER_MEMORY_CARD = [0xFF,0xB1,0x00,0x00,0x04]
	READ_PROTECTION_BITS = [0xFF,0xB2,0x00,0x00,0x04]
	WRITE_MEMORY_CARD = [0xFF,0xD0,0x00] # + byte address of first byte to write + length of data to write (in bytes ?) + every byte to write
	WRITE_PROTECTION_MEMORY_CARD = [0xFF,0xD1,0x00] # + byte address of first byte to write (from 0x00 to 0x1F) + length of data to write (in bytes ?) + every byte to write
	PRESENT_CODE_MEMORY_CARD = [0xFF,0x20,0x00,0x00,0x03] + # + each of the three bytes of the PIN
	CHANGE_CODE_MEMORY_CARD = [0xFF,0xD2,0x00,0x01,0x03] # + each of the three bytes of the new PIN
	
