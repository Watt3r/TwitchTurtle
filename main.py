'''

StreamLabs and TurtleCoin integration system.
Made by Watt Erikson and the TurtleCoin devs.
Copyright 2018, Watt Erikson and TurtleCoin devs

This file is part of TwitchTurtle.

    TwitchTurtle is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    TwitchTurtle is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with TwitchTurtle.  If not, see <https://www.gnu.org/licenses/>.

'''
from scripts.walletd import Walletd
from scripts.settings import Settings
from scripts.streamlabs import Stream
from time import sleep
from scripts.webserver import *
import subprocess
import os
import os.path
import requests
import threading
import string
import webbrowser
import json
import ast
import binascii
print("TwitchTurtle  Copyright (C) 2018  Watt Erikson and TurtleCoin Devs \n This program comes with ABSOLUTELY NO WARRANTY. \n This is free software, and you are welcome to redistribute it \n under certain conditions.")

cwd = os.getcwd()
# Set what type of currency you want (TRTL or USD)
currencyPref = Settings.Settings['currencyPref']
print('Currency is set to {}'.format(currencyPref))


'''
START STREAMLABS CODE
'''
Stream.checkLocalTokenAndCreate()
keys = Stream.checkToken()
#print("Printing keys {}".format(keys))
#print(keys[0])

'''
START WALLETD
'''
walletname = Settings.Settings['walletname']
walletpassword = Settings.Settings['walletpassword']

rpc_password = Settings.Settings['rpcpassword']



# Set Variables for interacting with walletd
rpc_host = 'localhost'
rpc_port = 8070
walletd = Walletd(rpc_password, rpc_host, rpc_port)

def startWalletd():
	# Open walletd
	print("Starting Walletd")
	
	try:
		walletdArgs = cwd+"\\scripts\\walletd.exe -w scripts\\"+walletname+" -p "+walletpassword+" --rpc-password "+rpc_password+" --daemon-address public.turtlenode.io" 

		global proc1
		proc1 = subprocess.Popen(walletdArgs, stderr=subprocess.STDOUT)
		sleep(5)
	except Exception as err:
		print('An error occured, check your task manager to make sure walletd is not running. Error: {}'.format(err))


	

def createAddresses():
	# Generate a new wallet file
	print("Could not find any wallet file! Making a new one.")
	
	walletdArgs = cwd+"\\scripts\\walletd.exe -g -w scripts\\"+walletname+" -p "+walletpassword+" --rpc-password "+rpcpassword 
	process = subprocess.Popen(walletdArgs, stdout=subprocess.PIPE)
	process.wait()


def savewallet():
	try:
		response = walletd.save()
	except Exception as err:
		print('An error occured, check your task manager to make sure walletd is not running. Error: {}'.format(err))
	if response['result'] != {}:
		print('Error in saving wallet : {}'.format(response))

def endwallet():
	proc1.terminate()
	sleep(5)
	proc1.kill()
	print("Safe to close wallet now.")
	exit()

def postTransaction(amount, extra):
	try:
		extraASCII = binascii.unhexlify(extra.encode()).decode()
		print(extraASCII)
		extraDict = ast.literal_eval(extraASCII)
		#print(extraDict)
		name = extraDict['name']
		message = extraDict['message'][:255]

		if (len(name) < 2) or (len(name) > 25):
			name = "Name is Invalid"
			print('Invalid Name')

		print("{} has sent the message {}.".format(name, message))

		# Convert TRTL atomic units in actual TRTL
		amount = amount / 100

		# Convert TRTL to currencypref
		coinmarketcap = "https://api.coinmarketcap.com/v2/ticker/2958/?convert={}".format(Settings.Settings['currencyPref']) 
		r = requests.request("GET", coinmarketcap)
		convertTRTL = r.json().get('data').get('quotes').get(Settings.Settings['currencyPref']).get('price')
		amount = amount * convertTRTL
			
		Stream.postDonation(name, message, amount, 'USD', keys[1])
	except Exception as err: 
		print(err)

		# Convert TRTL to currencypref
		coinmarketcap = "https://api.coinmarketcap.com/v2/ticker/2958/?convert={}".format(Settings.Settings['currencyPref']) 
		r = requests.request("GET", coinmarketcap)
		convertTRTL = r.json().get('data').get('quotes').get(Settings.Settings['currencyPref']).get('price')
		amount = amount * convertTRTL
			
		Stream.postDonation('Anonymous', 'Some TRTL\'er forgot to put a name and message! Oh no! If this was you, make sure to add the extra data field from the converter.', amount, 'USD', keys[1])
	

def searchForTransaction(addresses, lastBlockCount=None):


	# Get new block height
	responseStatus = walletd.get_status()
	blockCount = responseStatus['result']['blockCount']
	knownBlockCount = responseStatus['result']['knownBlockCount']
	if not lastBlockCount:
		lastBlockCount = knownBlockCount  - 2
	threading.Timer(0.5, searchForTransaction, args=[addresses, knownBlockCount],).start() # START ASYNC PROCESS
	#print("knownBlockCount {}  \n lastBlockCount {}".format(knownBlockCount, lastBlockCount))
	if ((knownBlockCount - lastBlockCount) > 1):
		skippedBlockDetector = (knownBlockCount - (knownBlockCount - lastBlockCount) - 2)
		#print("Skipped {} blocks".format(knownBlockCount - lastBlockCount))
		
	else:
		skippedBlockDetector = knownBlockCount - 2
		#print("Skipped {} blocks".format(blockCount - skippedBlockDetector))
		#print('{} {} {}'.format(lastBlockCount, knownBlockCount, skippedBlockDetector))
	if (knownBlockCount > lastBlockCount): # If the network found a new block, check the transactions in that block
		print('New block. Block {}'.format(knownBlockCount))
		#print('Skipped block detector says {}'.format(skippedBlockDetector))
		response = walletd.get_transactions(addresses, skippedBlockDetector, 10)
		responseItems = response['result']['items']
		for x in responseItems:
			for y in x['transactions']:
				postTransaction(y['amount'], y['extra'])

	





if os.path.isfile(cwd+"\\scripts\\"+walletname):
	# Start walletd
	#print('wallet found!')
	startWalletd()
else:
	# Create wallet
	#print('no wallet found')
	createAddresses()

# Check if wallet is synced with the network

response = walletd.get_status()
nodeHeight = response['result']['knownBlockCount']
walletHeight = response['result']['blockCount']

print('TRTL network is on block {}'.format(nodeHeight))
i = 0
while (abs(nodeHeight - walletHeight) > 10):
	response = walletd.get_status()
	nodeHeight = response['result']['knownBlockCount']
	walletHeight = response['result']['blockCount']
	print('Please wait while the wallet is syncing, you are {} block(s) behind. Slow and Steady wins the race!'.format(nodeHeight - walletHeight))
	i += 1
	if i==10:
		savewallet()
		i = 0
	sleep(10)
if (nodeHeight - walletHeight) < 10: 
	print("You are now syncronised with the TRTL network. Enjoy!")
	savewallet() 

# Set Address

response = walletd.get_addresses()
addresses = response['result']['addresses']
print('In order to recieve tips, users must send TRTL to this address: {}'.format(addresses[0]))

searchForTransaction(addresses)