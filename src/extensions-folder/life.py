"""
life.py
Responds with the meaning of life
"""

from extension import Extension
import random

class Life(Extension):
    def __init__(self):
        """
        Initializes the Life extension
        """
        # Regular expression to match extension
        matchExpression = "meaning of life"
        # Key words that Felix must compile into the language model
        keys = ["MEANING", "OF", "LIFE"]
        # Extension with lower precedence gets executed in a tie
        precedence = 0
        super(Life, self).__init__(matchExpression, keys, precedence)
    
    def execute(self, input, speechManager, memoryManager, userInfo):
        """
        Called when the extension must execute
        Responds with the meaning of life
        """
        messages = ["Well sir, I guess that is up to you.",
                    "42, sir."]
        message = random.choice(messages)
        speechManager.speakText(message)
        
def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return Life