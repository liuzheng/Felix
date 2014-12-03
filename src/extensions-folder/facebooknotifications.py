"""
facebooknotifications.py
Devin Gund + deg + Section E

Responds with current Facebook notifications for the user

Utilizes modules:
    - Facebook SDK

Information for working with the Facebook SDK and Graph API provided from:
    https://developers.facebook.com/docs/graph-api
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
        precedence = 2
        super(FacebookNotifications, self).__init__(matchExpression,
                                                    keys, precedence)

    @staticmethod
    def getNotifications(accessToken):
        """
        Returns Facebook notifications for the user
        Utilizes the Facebook module and GraphAPI
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
        message = "One moment. Obtaining current Facebook notifications."
        speechManager.speakText(message)
        accessToken = userInfo.facebookKey()
        notifications = FacebookNotifications.getNotifications(accessToken)
        if notifications:
            if len(notifications["data"]) == 0:
                message = "You have no Facebook notifications."
                speechManager.speakText(message)
                return
            updates = []
            for notification in notifications["data"]: # Get notification titles
                updates.append(notification["title"])
            count = len(notifications["data"]) # Get count
            updateSummary = " ".join(updates)
            message = "You have %s Facebook notifications. %s." % (str(count),
                                                                 updateSummary)
            speechManager.speakText(message)
        else:
            nickname = userInfo.nickname()
            error = "I am sorry, %s, but I cannot access Facebook." % (nickname)
            speechManager.speakText(error)

def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return FacebookNotifications