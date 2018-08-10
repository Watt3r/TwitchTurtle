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
class Settings():
	Settings = {
	    'walletname': 'defaultwallet.wallet', # Login for wallet. Only change the walletname if you are importing a pre-existing wallet or want muliple different profiles
	    'walletpassword': 'defaultpassword', # Login for wallet. If you change this, make sure an existing wallet file (walletname variable) does not exist in the scripts directory
	    'rpcpassword': 'test', # What the default rpc password for walletd is. Basically, change this to something random to be more secure. This is the only place where it is defined.
	    'currencyPref': 'USD', # Which currency would you like to use? Defaults to USD but can be any 3 digit currency listed here: https://streamlabs.readme.io/docs/currency-codes
	}