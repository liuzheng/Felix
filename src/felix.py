"""
felix.py
Devin Gund + deg + Section E

In charge of listening and reponding to user speech
Executes all extensions to provide Felix's features
"""

class Felix(object):
    def __init__(self, extensionManager, speechManager, memoryManager, userInfo, identifier="FELIX"):
        """
        Initializes the Felix class
        Holds the program managers
        """
        self.extensionManager = extensionManager # Manages extensions
        self.speechManager = speechManager # Manages speech in and out
        self.memoryManager = memoryManager # Manages memories
        self.identifier = identifier # The name of the system
        self.userInfo = userInfo # Encapsulates user information

    def live(self):
        """
        Should run forever, after being called in main.py
        Listens and reponds to user speech
        Executes the appropriate extension for the input speech
        """
        while True:
            ambientBase = None
            # Listen for identifier
            try: ambientBase = self.speechManager.listenForIdentifier(self.identifier)
            except: continue
            # If identifier found, listen for command
            if ambientBase:
                nickname = self.userInfo.nickname()
                self.speechManager.speakText("Yes, %s." % (nickname))
                input = self.speechManager.listen(ambientBase)
                self.speechManager.speakText("One moment.")
                self.extensionManager.execute(input, self.memoryManager, self.userInfo)