"""
felix.py
In charge of listening and reponding to user speech
Executes all extensions to provide Felix's features
"""

class Felix(object):
    
    def __init__(self, extensionManager, speechManager, memoryManager, userInfo, IDENTIFIER="FELIX"):
        """
        Initializes the Felix class
        """
        self.extensionManager = extensionManager
        self.speechManager = speechManager
        self.memoryManager = memoryManager
        self.IDENTIFIER = IDENTIFIER
        self.userInfo = userInfo
    
    def live(self):
        """
        Should run forever, after being called in main.py
        Listens and reponds to user speech
        Executes the appropriate extension for the input speech
        """
        while True:
            ambientBase = None
            try: ambientBase = self.speechManager.listenForIdentifier(self.IDENTIFIER)
            except: continue
            if ambientBase:
                nickname = self.userInfo.nickname()
                self.speechManager.speakText("Yes, %s." % (nickname))
                input = self.speechManager.listen(ambientBase)
                self.speechManager.speakText("One moment.")
                self.extensionManager.execute(input, self.memoryManager, self.userInfo)
