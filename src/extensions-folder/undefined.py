"""
undefined.py
Responds with a message indicating that the speech was unclear
"""

from extension import Extension
from sys import maxint
import random

class Undefined(Extension):
    def __init__(self):
        """
        Initializes the Undefined extension
        """
        # Regular expression to match extension
        matchExpression = ".*"
        # Key words that Felix must compile into the language model
        keys = []
        # Extension with lower precedence gets executed in a tie
        precedence = maxint - 1
        super(Undefined, self).__init__(matchExpression, keys, precedence)

    def execute(self, input, speechManager, memoryManager, userInfo):
        """
        Called when the extension must execute
        Responds with a message indicating that the speech was unclear
        """
        nickname = userInfo.nickname()
        messages = []
        messages.append("Sorry, %s, could you try that again?" % (nickname))
        messages.append("I could not quite understand that, %s" % (nickname))
        message = random.choice(messages)
        speechManager.speakText(message)

def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return Undefined