"""
main.py
Initiliazes all of the components of Felix
Hands over control to the Felix class to operate indefinitely
"""

import urllib2
from userinfo import UserInfo
from speechmanager import SpeechManager
from speechin import speechInEngine
from speechout import speechOutEngine
from extensionmanager import ExtensionManager
from felix import Felix

def isInternetOn():
    """
    Returns True if the a connection to the Internet is found
    Checks Google servers
    """
    try:
        address = "http://74.125.228.100"
        response = urllib2.urlopen(address, timeout = 1)
        return True
    except urllib2.URLError as err: pass
    return False

if __name__ == "__main__":
    print
    print "/-------------------------------------------------\\"
    print "| Welcome to FELIX                                |"
    print "| The intelligent computer personal assistant     |"
    print "| Copyright 2014 Devin Gund. All rights reserved. |"
    print "\\-------------------------------------------------/"
    print
    
    if not isInternetOn():
        print "A connection to the Internet could not be established."
        print "Some services may be unavailable."
        print
    
    # Create an instance of UserInfo, which encapsulates user data
    userInfo = UserInfo()
    # Create an instance of ExtensionManager, which encapsulates extensions
    extensionManager = ExtensionManager()
    # Create an instance of SpeechManager, which encapsulates STT and TTS
    speechManager = SpeechManager(speechInEngine(), speechOutEngine())
    extensionManager.speechManager = speechManager
    
    print "STARTING UP..."
    
    speechManager.speakText("Hello sir, I am Felix.")
    
    # Create and hand control over to Felix
    felix = Felix(extensionManager, speechManager, userInfo)
    felix.live()
