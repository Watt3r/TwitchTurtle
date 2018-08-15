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
import tornado.ioloop
import tornado.web
import requests
from datetime import datetime
import calendar


def getRefreshToken(code):
	# This function takes the authorization code from Streamlabs and pipes it back to streamlabs to get the access_token and refresh_token and returns it
	url = "https://streamlabs.com/api/v1.0/token"

	querystring = {
		'grant_type': "authorization_code",
		'client_id': 'bNN1u60BNNqbOgiId4eNuYKNQ3ykZ3meJoocLqvs',
		'client_secret': 'JPb4PBWcAmZtpRF9BTjSun7CPJ0G7MfP8QkzEwQz',
		'redirect_uri': "http://localhost:11888",
		'code': code
	}
	response = requests.request("POST", url, data=querystring)
	d = datetime.utcnow()
	unixtime = calendar.timegm(d.utctimetuple())

	stopTornado()
	global streamKeys
	streamKeys = [response.json().get('access_token'), response.json().get('refresh_token'), unixtime]
	return streamKeys

class tokenHandler(tornado.web.RequestHandler):
	def get(self):
		code = self.get_argument('code')
		if (code == ""):
			self.write("Please go to streamlabs authorization page to integrate TurtleCoin")
		else:
			self.write("StreamLabs TurtleCoin integration. If you are seeing this message,have successfully authenticated your StreamLabs account with TRTL. You can close this page safely")
		
		print(getRefreshToken(code))

	def post(self):
		token = self.get_argument("token")
		
		self.write("Token is {}".format(token))

def make_app():
	return tornado.web.Application([
		(r"/", tokenHandler),
	])

def stopTornado():
	tornado.ioloop.IOLoop.instance().stop()

def startWebListener():
	app = make_app()
	app.listen(11888)
	tornado.ioloop.IOLoop.current().start()
	return streamKeys