"""
name.py
Devin Gund + deg + Section E

Responds with information about the system
"""

from extension import Extension

class Demo(Extension):
    def __init__(self):
        """
        Initializes the Demo extension
        """
        # Regular expression to match extension
        matchExpression = "what are you"
        # Key words that Felix must compile into the language model
        keys = ["WHAT", "ARE", "YOU"]
        # Extension with lower precedence gets executed in a tie
        precedence = 0
        super(Demo, self).__init__(matchExpression, keys, precedence)

    def execute(self, input, speechManager, memoryManager, userInfo):
        """
        Called when the extension must execute
        Responds with the name of the system ('Felix')
        """
        message = "My name is Felix."
        message += " I am an intelligent computer personal assistant."
        message += " I listen to user speech, and respond"
        message += " with pertinent information or actions."
        message += " My features come in the form of extensions,"
        message += " which are class files that handle a particular"
        message += "speech input by returning related data."
        speechManager.speakText(message)

def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return Demo