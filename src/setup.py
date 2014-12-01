"""
setup.py
Can be run separately from Felix to setup up user info
Asks a series of questions to provide more personalized services
"""

import re

try: import cPickle as pickle
except: import pickle

def setup():
    """
    Main function
    Sets up information by prompting user
    Reads from and writes to userInfo.p
    """
    print "To better assist you, I will request some information."
    print "This will allow me to provide more personalized services"
    userInfo = readUserInfo()
    setupName(userInfo)
    setupNickname(userInfo)
    setupLocation(userInfo)
    setupTimezone(userInfo)
    setupWundergroundKey(userInfo)
    setupFacebookKey(userInfo)
    writeUserInfo(userInfo)
    print "Your information has been set up."
    print "You can change it in the future by running setup.py"

def promptForInfo(name, previousInput=""):
    """
    Called by other setup functions
    Returns user input for prompt 'name'
    Can optionally display 'previousInput'
    """
    previous = (" (previous value was %s)" % (previousInput)) if len(previousInput) > 0 else ""
    input = raw_input(("%s%s: ") % (name, previous))
    return input
    
def setupName(userInfo):
    """
    Prompts user for first name and last name
    """
    userInfo["firstname"] = promptForInfo("First Name", userInfo.get("firstname", ""))
    userInfo["lastname"] = promptForInfo("Last Name", userInfo.get("lastname", ""))

def setupNickname(userInfo):
    """
    Prompts user for a nickname, which can optionally be used
    """
    if promptForInfo("Would you rather I use a nickname? (yes/no)") == "yes":
        userInfo["nickname"] = promptForInfo("Nickname", userInfo.get("nickname", ""))
    else: del userInfo["nickname"]
    
def setupLocation(userInfo):
    """
    Prompts user for a location
    Location can be within or outside of the United States
    """
    locationState = None
    if promptForInfo("Are you located within the United States? (yes/no)") == "yes":
        locationState = promptForInfo("State Abbreviation (ex. CT)")
    else:
        locationState = promptForInfo("Country (ex. France)")
    locationCity = promptForInfo("City")
    userInfo["locationstate"] = locationState
    userInfo["locationcity"] = locationCity

def setupTimezone(userInfo):
    """
    Prompts user for TZ* time zone code
    """
    address = "http://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
    timezone = promptForInfo(("Timezone (select from the TZ* column at %s)" % (address)), userInfo.get("timezone", ""))
    userInfo["timezone"] = timezone

def setupWundergroundKey(userInfo):
    """
    Prompts user for a Wunderground API key, which is required for weather
    """
    address = "http://www.wunderground.com/weather/api/"
    print "To access weather reports, you must obtain a free API key from %s" % (address)
    userInfo["wundergroundkey"] = promptForInfo("Wunderground API key")
    
def setupFacebookKey(userInfo):
    """
    Prompts user for a Facebook access key, which is required for Facebook
    """
    address = "https://developers.facebook.com/docs/facebook-login/access-tokens"
    print "To access Facebook notifications, you must obtain a free access key from %s" % (address)
    userInfo["facebookkey"] = promptForInfo("Facebook access key")

def readUserInfo():
    """
    Reads user information from 'userInfo.p'
    """
    userInfo = {}
    try: userInfo = pickle.load(open("userInfo.p", "rb"))
    except: print "Setup: Error reading user info."
    return userInfo

def writeUserInfo(userInfo):
    """
    Writes user information to 'userInfo.p'
    """
    try: pickle.dump(userInfo, open("userInfo.p", "wb"))
    except: print "Setup: Error writing user info."

if __name__ == "__main__":
    setup()
