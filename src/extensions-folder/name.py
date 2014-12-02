"""
name.py
Responds with the name of the system ('Felix')
"""

from extension import Extension

class Name(Extension):
    def __init__(self):
        """
        Initializes the Name extension
        """
        # Regular expression to match extension
        matchExpression = "your name"
        # Key words that Felix must compile into the language model
        keys = ["WHAT", "IS", "YOUR", "NAME"]
        # Extension with lower precedence gets executed in a tie
        precedence = 0
        super(Name, self).__init__(matchExpression, keys, precedence)
    
    def execute(self, input, speechManager, memoryManager, userInfo):
        """
        Called when the extension must execute
        Responds with the name of the system ('Felix')
        """
        message = "My name is Felix. I am an intelligent computer personal assistant."
        speechManager.speakText(message)
        
def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return Name