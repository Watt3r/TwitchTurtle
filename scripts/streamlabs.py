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
from time import sleep
from scripts.webserver import *
import subprocess
import os
import os.path
import requests
import threading
import string
import webbrowser
'''
START STREAMLABS CODE
'''
class Stream:
	def checkLocalTokenAndCreate():
		global cwd
		cwd = os.getcwd()
		global refresh_token
		# Checks if authtoken is present, if it is then it reads the keys, if not, it goes to the authorize endpoint for streamlabs
		#print(os.path.isfile(cwd+"\\scripts\\authtoken.auth"))
		
		if  os.path.isfile(cwd+"\\scripts\\authtoken.auth"):
			#print('Has authtoken file')
			if (os.stat("scripts\\authtoken.auth").st_size == 0):
				print('Auth file corrupt')
				os.remove("scripts\\authtoken.auth")
				return Stream.authpageAndCreateFile()
			f = open(cwd+"\\scripts\\authtoken.auth",'r') #Opens the file
			data = f.read()
			refresh_token = data
			
			return refresh_token
		else:
			return Stream.authpageAndCreateFile()
	def authpageAndCreateFile():
		global refresh_token
		global access_token
		print('Does not have valid authtoken file. Redirecting to authorize page.')
		# Open url to streamlabs auth site
		print('Openinig webbrowser')
		webbrowser.open('https://www.streamlabs.com/api/v1.0/authorize?client_id=bNN1u60BNNqbOgiId4eNuYKNQ3ykZ3meJoocLqvs&redirect_uri=http://localhost:11888&response_type=code&scope=donations.read+donations.create')
		# startWebListener listens for localhost:11888 from streamlabs and returns tokens
		keys = startWebListener()

		# Saves refresh token so that user does not have to auth every time

		datatowrite = str(keys[1])
		refresh_token = keys[1]
		access_token = keys[0]

		print('writing key to authfile')
		f = open(cwd+"\\scripts\\authtoken.auth",'w')
		f.write(datatowrite)
		f.close()

			
		return refresh_token, access_token

	# Make sure access_token does not expire 
	def checkToken(key):
		global refresh_token
		global access_token

		#print('Starting {} '.format(refresh_token))
		
		url = "https://streamlabs.com/api/v1.0/token"

		querystring = {
			'grant_type': "refresh_token",
			'client_id': 'bNN1u60BNNqbOgiId4eNuYKNQ3ykZ3meJoocLqvs',
			'client_secret': key,
			'redirect_uri': "http://localhost:11888",
			'refresh_token': refresh_token
		}
		
		response = requests.request("POST", url, data=querystring)
		if response.status_code == 400:
			# Request failed.
			print('Error 400, wrong token')
			keys = Stream.authpageAndCreateFile()
			refresh_token = keys[0]
			access_token = keys[1]
		elif response.status_code == 200:
			# Request success
			#print(response.status_code)
			refresh_token = response.json().get('refresh_token')
			access_token = response.json().get('access_token')

			#print('Access token: {}'.format(response.json().get('access_token')))
			#print('Refresh token: {}'.format(response.json().get('refresh_token')))

			# Update authtoken.auth file with new refresh_token in case of unexpected closure
			f = open(cwd+"\\scripts\\authtoken.auth",'w')
			f.write(refresh_token)
			f.close()

		threading.Timer(3000.0, Stream.checkToken, args=(key,)).start() # START ASYNC PROCESS
		return refresh_token, access_token

	def postDonation(name, message, amount, currency, access_token):
		
		TRTLmessage = message + " This message was donated with TurtleCoin."


		url = "https://streamlabs.com/api/v1.0/donations"

		querystring = {
			'name': name,
			'message': TRTLmessage,
			'identifier': name,
			'amount': amount,
			'currency': currency,
			'access_token': access_token,
		}
		response = requests.request("POST", url, data=querystring)
		print(response.text)
