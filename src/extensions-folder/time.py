"""
time.py
Responds with the current time and date for the user's time zone
"""

from extension import Extension
import datetime
import pytz

class Time(Extension):
    def __init__(self):
        """
        Initializes the Time extension
        """
        # Regular expression to match extension
        matchExpression = "time|date"
        # Key words that Felix must compile into the language model
        keys = ["WHAT", "IS", "THE", "TIME", "DATE", "IT"]
        # Extension with lower precedence gets executed in a tie
        precedence = 0
        super(Time, self).__init__(matchExpression, keys, precedence)

    @staticmethod
    def getTime(userInfo):
        """
        Returns the current time in 12-hour format
        """
        tz = pytz.timezone(userInfo.timezone())
        now = datetime.datetime.now(tz = tz)
        hour = now.hour
        minute = now.minute
        # Convert 24-hour to 12-hour time
        period = ""
        halfTime = 12
        if hour > halfTime:
            hour -= halfTime
            period = "PM"
        else:
            if hour == 0: hour = halfTime
            period = "AM"
        # Format timeString
        timeString = "%i:%i %s" % (hour, minute, period)
        return timeString

    @staticmethod
    def getDate(userInfo):
        """
        Returns the current time in 12-hour format
        """
        tz = pytz.timezone(userInfo.timezone())
        now = datetime.datetime.now(tz = tz)
        year = now.year
        month = now.month
        day = now.day
        # Obtain name of month
        monthNames = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]
        monthString = monthNames[month - 1]
        # Format dateString
        dateString = "%s %i, %i" % (monthString, day, year)
        return dateString

    def execute(self, input, speechManager, userInfo):
        """
        Called when the extension must execute
        Responds with the current time and date for the user's time zone
        """
        timeString = Time.getTime(userInfo) # Get time
        dateString = Time.getDate(userInfo) # Get date
        message = "The current time is %s. Today is %s." % (
                                                        timeString, dateString)
        speechManager.speakText(message)

def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return Time