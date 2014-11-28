"""
time.py
Responds with the current time for the user's time zone
"""

from extension import Extension
import datetime
from semantic.dates import DateService
import pytz

class Time(Extension):
    def __init__(self):
        """
        Initializes the Time extension
        """
        # Regular expression to match extension
        matchExpression = "time"
        # Key words that Felix must compile into the language model
        keys = ["WHAT", "IS", "THE", "TIME", "IT"]
        # Extension with lower precedence gets executed in a tie
        precedence = 0
        super(Time, self).__init__(matchExpression, keys, precedence)
    
    def execute(self, input, speechManager, userInfo):
        """
        Called when the extension must execute
        Responds with the current time for the user's time zone
        """
        tz = pytz.timezone(userInfo.getTimezone())
        now = datetime.datetime.now(tz = tz)
        service = DateService()
        time = str(service.convertTime(now))
        message = "The current time is %s." % (time)
        speechManager.speakText(message)
        
def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return Time