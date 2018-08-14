# User defined variables. You MUST change the walletpass and rpcpassword
class Settings():
	Settings = {
	    'walletname': 'defaultwallet.wallet', # Login for wallet. Only change the walletname if you are importing a pre-existing wallet or want muliple different profiles
	    'walletpassword': 'defaultpassword', # Login for wallet. Change this to a password you will remember. If you want to change which wallet you use, you will need this
	    'rpcpassword': 'test', # Password for the program communicating with itself. Change this to something random.
	    'currencyPref': 'USD', # Which currency would you like to use? Defaults to USD but can be any 3 digit currency listed here: https://streamlabs.readme.io/docs/currency-codes
	}
