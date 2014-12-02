"""
username.py
Responds with the name of the user
"""

from extension import Extension

class UserName(Extension):
    def __init__(self):
        """
        Initializes the UserName extension
        """
        # Regular expression to match extension
        matchExpression = "my name"
        # Key words that Felix must compile into the language model
        keys = ["WHAT", "IS", "MY", "NAME"]
        # Extension with lower precedence gets executed in a tie
        precedence = 0
        super(UserName, self).__init__(matchExpression, keys, precedence)
    
    def execute(self, input, speechManager, memoryManager, userInfo):
        """
        Called when the extension must execute
        Responds with the name of the user
        """
        firstName = userInfo.firstName()
        lastName = userInfo.lastName()
        nickname = userInfo.nickname()
        message = ("Your name is %s %s, but I call you %s." %
                   (firstName, lastName, nickname))
        speechManager.speakText(message)
        
def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return UserName