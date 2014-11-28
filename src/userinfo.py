"""
userinfo.py
Allows for the reading and writing of user information
"""

try: import cPickle as pickle
except: import pickle

class UserInfo(object):
    def __init__(self):
        """
        Initiliazes the UserInfo class by reading user information from file
        """
        self.readUserInfo()
    
    def readUserInfo(self):
        """
        Reads user information from userInfo.p
        User information is stored in userInfo dictionary
        """
        userInfo = {}
        try: userInfo = pickle.load(open("userInfo.p", "rb"))
        except: print "user.py: Error reading user info."
        self.userInfo = userInfo
    
    def writeUserInfo(self):
        """
        Writes user information to userInfo.p
        """
        try: pickle.dump(self.userInfo, open("userInfo.p", "wb"))
        except: print "user.py: Error writing user info."
    
    def infoForKey(self, key):
        """
        Called by other functions
        Returns value for key
        If there is no value for key, returns empty string
        """
        return self.userInfo.get(key, "")
    
    def firstName(self):
        """
        Returns user's first name
        """
        return self.infoForKey("firstname")
        
    def lastName(self):
        """
        Returns user's last name
        """
        return self.infoForKey("lastname")
        
    def nickname(self):
        """
        Returns user's nickname
        If no nickname exists, returns user's first name
        """
        nickname = self.infoForKey("nickname")
        if nickname == None or len(nickname) == 0: nickname = self.firstName()
        return nickname
        
    def emailAddress(self):
        """
        Returns user's email address
        """
        return self.infoForKey("emailaddress")
        
    def locationState(self):
        """
        Returns user's state/country
        """
        return self.infoForKey("locationstate")

    def locationCity(self):
        """
        Returns user's city
        """
        return self.infoForKey("locationcity")
        
    def timeZone(self):
        """
        Returns user's TZ* time zone code
        """
        return self.infoForKey("timezone")
        
    def wundergroundKey(self):
        """
        Returns user's Wunderground API key
        """
        return self.infoForKey("wundergroundkey")
    
    def facebookKey(self):
        """
        Returns user's Facebook access key
        """
        return self.infoForKey("facebookkey")