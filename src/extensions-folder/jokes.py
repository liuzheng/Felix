"""
jokes.py
Responds with a random (bad) computer joke
"""

from extension import Extension
import random

class Jokes(Extension):
    def __init__(self):
        """
        Initializes the Jokes extension
        """
        # Regular expression to match extension
        matchExpression = "joke"
        # Key words that Felix must compile into the language model
        keys = ["JOKE"]
        # Extension with lower precedence gets executed in a tie
        precedence = 0
        super(Jokes, self).__init__(matchExpression, keys, precedence)

    @staticmethod
    def randomJoke(jokeFile = "media-folder/jokes.txt"):
        """
        Returns a random joke from jokes.txt
        """
        jokes = []
        with open(jokeFile, "rt") as file:
            print "well, we opened the file....."
            joke = []
            for line in file.readlines():
                if not line.strip() and len(joke) > 0:
                    jokes.append(tuple(joke))
                    print "Adding joke:", joke
                    joke = []
                else:
                    joke.append(line)
        choice = random.choice(jokes)
        return choice

    def execute(self, input, speechManager, memoryManager, userInfo):
        """
        Called when the extension must execute
        Responds with a random joke from jokes.txt
        """
        joke = Jokes.randomJoke()
        speechManager.speakText("Here is a joke.")
        for line in joke:
            speechManager.speakText(line)

def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return Jokes