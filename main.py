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
from scripts.turtlecoind import TurtleCoind
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
import string
import random
import configparser
import optparse
print("TwitchTurtle  Copyright (C) 2018  Watt Erikson and TurtleCoin Devs \n This program comes with ABSOLUTELY NO WARRANTY. \n This is free software, and you are welcome to redistribute it \n under certain conditions.\n\n")

cwd = os.getcwd()


config = configparser.ConfigParser()
config.sections()
config.read('settings.ini')
config.sections()

with open('settings.ini', 'w') as configfile:
  config.write(configfile)

# Set what type of currency you want (TRTL or USD)
currencyPref = config['SETTINGS']['currencyPref']
key = 'JPb4PBWcAmZtpRF9BTjSun7CPJ0G7MfP8QkzEwQz'
print('Currency is set to {}'.format(currencyPref))

# Set log level
parser = optparse.OptionParser()

parser.add_option('-l', '--log-level',
    action="store", dest="log",
    help="log-level", default="1")

options, args = parser.parse_args()

print ('Log level: {}'.format(options.log))



'''
START STREAMLABS CODE
'''
Stream.checkLocalTokenAndCreate()
keys = Stream.checkToken(key)

'''
START WALLETD
'''
walletname = config['SETTINGS']['walletname']
walletpassword = config['SETTINGS']['walletpassword']

if walletpassword == 'defaultpass':
	input('Change your wallet passsword in settings.ini, or you can choose to ignore this security risk and press [ENTER] to continue')

def passGen(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


rpc_password = passGen()
feeAmount = '100'



# Set Variables for interacting with walletd
rpc_host = 'localhost'
rpc_port = 8070
walletd = Walletd(rpc_password, rpc_host, rpc_port)
turtlecoind = TurtleCoind()

def startWalletd():
	global proc1
	# Open walletd
	print("Starting Walletd")
	
	try:
		walletdArgs = cwd+"\\scripts\\turtle-service.exe -w scripts\\"+walletname+" -p "+walletpassword+" --rpc-password "+rpc_password+" --enable-cors  '*' --log-level "+ options.log +" --daemon-address 127.0.0.1"

		proc1 = subprocess.Popen(walletdArgs, stderr=subprocess.STDOUT)
		sleep(5)
	except Exception as err:
		print('An error occured, check your task manager to make sure walletd is not running. Error: {}'.format(err))
		exit()

def startdaemon():
	global proc2
	# Get the most recent Checkpoints file and save it
	url = 'https://github.com/turtlecoin/checkpoints/raw/master/checkpoints.csv'
	r = requests.get(url, allow_redirects=True)
	open('checkpoints.csv', 'wb').write(r.content)

	# Open Daemons
	print("Starting TurtleCoind")
	
	try:
		turtlecoindArgs = cwd+"\\scripts\\turtlecoind.exe --load-checkpoints checkpoints.csv --log-level "+ options.log +" --fee-address TRTLuxXuMJYPAWwbqUpBPkjWA79hLdb6G5CF4fjqhdgP8ufhbLcFWNRPJiwtdZ5QcDgukvXT8yVxXSoXrehdwnRTZwDLQCMVoNf --fee-amount "+feeAmount 
		
		proc2 = subprocess.Popen(turtlecoindArgs, stderr=subprocess.STDOUT)
		sleep(10)
		while True:
			print('Still syncing. {} More blocks'.format(turtlecoind.get_height()['network_height'] - turtlecoind.get_height()['height']))
			if (turtlecoind.get_info()['synced']):
				if os.path.isfile(cwd+"\\scripts\\"+walletname):
					# Start walletd
					startWalletd()
					break
				else:
					# Create wallet
					createAddresses()
					break
			sleep(20)

	except Exception as err:
		print('An error occured, check your task manager to make sure turtlecoind is not running. Error: {}'.format(err))
		exit()
		
def createAddresses():
	# Generate a new wallet file
	print("Could not find any wallet file! Making a new one.")
	
	walletdArgs = cwd+"\\scripts\\turtle-service.exe -g -w scripts\\"+walletname+" -p "+walletpassword+" --rpc-password "+rpc_password 
	process = subprocess.Popen(walletdArgs, stdout=subprocess.PIPE)
	process.wait()
	startWalletd()


def savewallet():
	# Save the wallet periodically in case the User closes without warning.
	try:
		response = walletd.save()
	except Exception as err:
		print('An error occured, check your task manager to make sure walletd is not running. Error: {}'.format(err))
	if response['result'] != {}:
		print('Error in saving wallet : {}'.format(response))

def endwallet():
	# Stop the wallet
	proc1.terminate()
	proc2.terminate()
	sleep(5)
	proc1.kill()
	proc2.kill()
	print("Safe to close Script now.")
	exit()

def postTransaction(amount, extra):
	# Convert The extra data and send it to streamlabs.py
	amount = amount / 100
	coinmarketcap = "https://api.coinmarketcap.com/v2/ticker/2958/?convert={}".format(currencyPref) 
	r = requests.request("GET", coinmarketcap)
	convertTRTL = r.json().get('data').get('quotes').get(currencyPref).get('price')
	amount = amount * convertTRTL
	try:
		extraASCII = binascii.unhexlify(extra.encode()).decode()
		print(extraASCII)
		extraDict = ast.literal_eval(extraASCII)
		name = extraDict['name']
		message = extraDict['message'][:255]

		if (len(name) < 2) or (len(name) > 25):
			name = "Name is Invalid"
			print('Invalid Name')

		print("{} has sent the message {}.".format(name, message))
			
		Stream.postDonation(name, message, amount, currencyPref, keys[1])
	except Exception as err: 
		print(err)
		Stream.postDonation('Anonymous', 'Some TRTL\'er forgot to put a name and message! Oh no! If this was you, make sure to add the extra data field from the converter.', amount, currencyPref, keys[1])
def searchForTransaction(addresses, lastBlockCount=None):
	# Get new block height
	responseStatus = walletd.get_status()
	blockCount = responseStatus['result']['blockCount']
	knownBlockCount = responseStatus['result']['knownBlockCount']
	if not lastBlockCount:
		lastBlockCount = knownBlockCount  - 2
	threading.Timer(0.5, searchForTransaction, args=[addresses, knownBlockCount],).start() # START ASYNC PROCESS
	if ((knownBlockCount - lastBlockCount) > 1):
		skippedBlockDetector = (knownBlockCount - (knownBlockCount - lastBlockCount) - 2)
	else:
		skippedBlockDetector = knownBlockCount - 2
	if (knownBlockCount > lastBlockCount): # If the network found a new block, check the transactions in that block
		response = walletd.get_transactions(addresses, skippedBlockDetector, 10)
		responseItems = response['result']['items']
		for x in responseItems:
			for y in x['transactions']:
				postTransaction(y['amount'], y['extra'])


# Start TurtleCoind and wait for it to sync
startdaemon()
sleep(20)


# Check if wallet is synced with the network
response = walletd.get_status()
nodeHeight = response['result']['knownBlockCount']
walletHeight = response['result']['blockCount']

while response['result']['knownBlockCount'] is 1:
	print('Turtlecoin is starting, please wait')
	response = walletd.get_status()
	sleep(5)
# Set Address

response = walletd.get_addresses()
addresses = response['result']['addresses']
print('\n\n\nIn order to recieve tips, users must send TRTL to this address: {} \n It is highly recommended to transfer all the funds out of this wallet into a more secure one. You can transact the TRTL out from the box-turtle folder.\n\n\n'.format(addresses[0]))


i = 0
while ((abs(nodeHeight - walletHeight) > 10) or nodeHeight < 10 or walletHeight < 10):
	response = walletd.get_status()
	nodeHeight = response['result']['knownBlockCount']
	walletHeight = response['result']['blockCount']
	print('Still syncing, you are {} block(s) behind.'.format(nodeHeight - walletHeight))
	i += 1
	if i==10:
		savewallet()
		i = 0
	sleep(10)

savewallet()	
print('\n\n\nIn order to recieve tips, users must send TRTL to this address: {} \n It is highly recommended to transfer all the funds out of this wallet into a more secure one. You can transact the TRTL out from the box-turtle folder.\n\n\n'.format(addresses[0]))
searchForTransaction(addresses)