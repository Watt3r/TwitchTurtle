TwitchTurtle
======
## Integrate TurtleCoin with StreamLabs
Note: This is works with Twitch and Youtube Live
### Basic installation

* Download the new release from https://github.com/Watt3r/TwitchTurtle/releases/ 
* Change the settings in settings.ini with any text editor
* Run main.exe
* While you are streaming, you need to keep main.exe open

#### How to use

* After the first time running, you should just need to run `python main.py` while in the TwitchTurtle folder.
* If you want to take the TurtleCoin out of your donation wallet and into a new one, (which is highly recomended) download [box-turtle from here](https://github.com/watt3r/box-turtle)

### How to get your viewers to donate with TRTL.

To inform your viewers about TurtleCoin and your new way of donating, you can copy and paste this Text into a Nightbot repeating command, or into your description.


TurtleCoin is a cryptocurrency that is fast, private, and easy to use!
If you would like to Donate using TurtleCoin, go to github.com/turtlecoin/box-turtle
Alternatively, if you already use TurtleCoin, you can donate to my address here: <YOUR TRTL ADDRESS>

You can also advertise to the TwitchTurtle discord when you go live! [Invite Code](http://chat.twitchturtle.com)

#### How to get TRTL into USD

* To get TRTL into USD, open `main.exe` and open the `index.html` file inside box-turtle folder. Then use any exchange listed [here](http://turtleturtle.org)
* Send your TRTL with the paymentID (IMPORTANT!) and they will be in the exchange account if you want to transfer them to other coins, or into USD

### Help!

If you need help, with any aspect of this project, make sure to [Join the Official TurtleCoin Discord Server!](http://chat.turtlecoin.lol)
You can also join the TwitchTurtle discord for more specific help questions [Invite Code](http://chat.twitchturtle.com)

#### Building from Source

* Clone or Download this Git repository onto your local machine
* Check to see if you have python already installed, you can check with `python --version` or `python3 --version` You must have python 3.6.5 or higher to work.
* If the command above worked when you had a 3 added to the end of python, you must add that for all steps, with `python` and `pip` so they look like `python3` and `pip3`
* Open terminal or cmd and go to the TwitchTurtle folder and enter `pip install -r requirements.txt`
* Open the `settings.ini` with your favorite editor, and change the password and username.
* Then, run `python main.py` while in the TwitchTurtle folder.
* (Optional) if you want to make the python file into an .exe, run the build.bat file and it will build it into the `dist` folder.


### TL;DR

https://github.com/Watt3r/TwitchTurtle/releases/
