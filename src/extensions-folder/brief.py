"""
brief.py
Devin Gund + deg + Section E

Responds with a brief for the current situation
Includes time, weather, and news
"""

from extension import Extension
import datetime
import pytz

from time import Time
from weather import Weather
from news import News

class Brief(Extension):
    def __init__(self):
        """
        Initializes the Brief extension and the extensions it calls
        """
        # Regular expression to match extension containing 'brief' and 'me'
        matchExpression = "^(?=\\b.*brief\\b)(?=\\b.*me\\b)"
        # Key words that Felix must compile into the language model
        keys = ["BRIEF", "ME"]
        # Extension with lower precedence gets executed in a tie
        precedence = 2
        super(Brief, self).__init__(matchExpression, keys, precedence)
        # Import extensions that will be called in the brief
        self.extensions = [Time(), Weather(), News()]

    def execute(self, input, speechManager, memoryManager, userInfo):
        """
        Called when the extension must execute
        Responds with a brief for the current situation
        """
        tz = pytz.timezone(userInfo.timezone())
        now = datetime.datetime.now(tz = tz)
        hour = now.hour
        afternoon = 12 # The afternoon starts at 12:00
        evening = 18 # The evening starts at 18:00
        timeOfDay = ""
        if hour < afternoon: timeOfDay = "morning"
        elif hour >= afternoon and hour < evening: timeOfDay = "afternoon"
        else: timeOfDay = "evening"
        nickname = userInfo.nickname()
        message = "Good %s, %s." % (timeOfDay, nickname)
        speechManager.speakText(message)
        for extension in self.extensions:
            extension.execute(input, speechManager, memoryManager, userInfo)

def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return Brief