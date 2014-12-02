"""
reminders.py
Responds with the current reminders
Optionally allows for the addition of a reminder
Reminders last for 24 hours
"""

from extension import Extension

class Reminders(Extension):
    def __init__(self):
        """
        Initializes the Brief extension
        """
        # Regular expression to match extension
        matchExpression = "reminder"
        # Key words that Felix must compile into the language model
        keys = ["REMINDER", "ADD"]
        # Extension with lower precedence gets executed in a tie
        precedence = 2
        super(Reminders, self).__init__(matchExpression, keys, precedence)
        # Import extensions that will be called in the brief

    @staticmethod
    def getReminders(memoryManager):
        """
        Returns a list of the current reminder messages from memoryManager
        """
        messages = memoryManager.getReminders()
        return messages

    @staticmethod
    def addReminder(memoryManager, message):
        """
        Adds a reminder message to memoryManager
        """
        memoryManager.addReminder(message)

    def execute(self, input, speechManager, memoryManager, userInfo):
        """
        Called when the extension must execute
        Responds with a brief for the current situation
        """
        # Check if the user wants to add a new reminder
        if "ADD" in input:
            # Query the user for the reminder message
            speechManager.speakText("Please speak the reminder message to add.")
            message = speechManager.listen(isFullVocabulary = True)
            speechManager.speakText("Adding reminder. %s" % (message))
            Reminders.addReminder(memoryManager, message)
        # Speak the current list of reminders
        reminders = Reminders.getReminders(memoryManager)
        message = ""
        if len(reminders) > 0:
            message = "Here are your current reminders. "
            message += ". ".join(reminders) # Combine list of messages into string
        else:
            message = "You have no current reminders."
        speechManager.speakText(message)

def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return Reminders