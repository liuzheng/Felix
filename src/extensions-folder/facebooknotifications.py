"""
facebooknotifications.py
Responds with current Facebook notifications for the user
"""

from extension import Extension
import facebook

class FacebookNotifications(Extension):
    def __init__(self):
        """
        Initializes the Facebook extension
        """
        # Regular expression to match extension
        matchExpression = "facebook"
        # Key words that Felix must compile into the language model
        keys = ["FACEBOOK", "NOTIFICATION"]
        # Extension with lower precedence gets executed in a tie
        precedence = 0
        super(FacebookNotifications, self).__init__(matchExpression, keys, precedence)
    
    @staticmethod
    def getNotifications(accessToken):
        """
        Returns Facebook notifications for the user
        Utilizes the facebook module and GraphAPI
        """
        graph = facebook.GraphAPI(accessToken)
        results = None
        try: results = graph.request("me/notifications")
        except: pass
        return results
    
    def execute(self, input, speechManager, memoryManager, userInfo):
        """
        Called when the extension must execute
        Responds with current Facebook notifications for the user
        """
        accessToken = userInfo.facebookKey()
        notifications = FacebookNotifications.getNotifications(accessToken)
        if notifications:
            if len(notifications["data"]) == 0:
                message = "You have no Facebook notifications."
                speechManager.speakText(message)
                return
            updates = []
            for notification in results["data"]:
                updates.append(notification["title"])
            count = len(results['data'])
            updateSummary = " ".join(updates)
            message = "You have %s Facebook notifications. %s." % (str(count), updateSummary) 
            speechManager.speakText(message)
        else:
            nickname = userInfo.nickname()
            error = "I am sorry, %s, but I could not access Facebook." % (nickname)
            speechManager.speakText(error)
        
def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return FacebookNotifications