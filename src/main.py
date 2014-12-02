"""
main.py
Initializes all of the components of Felix
Hands over control to the Felix class to operate indefinitely
"""

import urllib2
from userinfo import UserInfo
from speechmanager import SpeechManager
from speechin import speechInEngine
from speechout import speechOutEngine
from extensionmanager import ExtensionManager
from memorymanager import MemoryManager
from felix import Felix

def isInternetOn():
    """
    Returns True if the a connection to the Internet is found
    Checks Google servers
    """
    try:
        address = "http://74.125.228.100" # Google server
        response = urllib2.urlopen(address, timeout = 1)
        return True
    except urllib2.URLError as error: pass
    return False

if __name__ == "__main__":
    print
    print "/-------------------------------------------------\\"
    print "| Welcome to Felix                                |"
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
    # Create instances of the managers that govern Felix
    # The extension manager compiles the dictionary and languagemodel,
    #     so it must be called before the speech manager
    # Create an instance of MemoryManager, which encapsulates memory
    memoryManager = MemoryManager(userInfo)
    # Create an instance of ExtensionManager, which encapsulates extensions
    extensionManager = ExtensionManager()
    # Create an instance of SpeechManager, which encapsulates STT and TTS
    speechManager = SpeechManager(speechInEngine(), speechOutEngine())
    # Add speechManager to memoryManager once created
    memoryManager.speechManager = speechManager
    # Add speechManager and memoryManager to extensionManager once created
    extensionManager.speechManager = speechManager
    extensionManager.memoryManager = memoryManager

    print "STARTING UP..."

    message = "I am Felix, the intelligent computer personal assistant."
    speechManager.speakText(message)

    # Create and hand control over to Felix instance
    felix = Felix(extensionManager, speechManager, memoryManager, userInfo)
    felix.live()
