"""
news.py
Devin Gund + deg + Section E

Responds with the five top news stories

Utilizes extensions:
    - feedparser
"""

from extension import Extension
import feedparser

class News(Extension):
    def __init__(self):
        """
        Initializes the News extension
        """
        # Regular expression to match extension
        matchExpression = "news"
        # Key words that Felix must compile into the language model
        keys = ["NEWS", "STORIES"]
        # Extension with lower precedence gets executed in a tie
        precedence = 2
        super(News, self).__init__(matchExpression, keys, precedence)

    @staticmethod
    def getNews(address="http://news.google.com/?output=rss"):
        """
        Returns the five top stories on news.google.com
        """
        feed = feedparser.parse(NEWS_URL)
        entries = feed.entries
        topStories = []
        for entry in entries:
            if len(topStories) >= 5: break # Limit to five top stories
            title = entry.title
            topStories.append(title)
        return topStories

    def execute(self, input, speechManager, memoryManager, userInfo):
        """
        Called when the extension must execute
        Responds with the five top news stories
        """
        speechManager.speakText("Here are your five top news stories.")
        topStories = News.getNews()
        if len(topStories) == 0:
            # If unable to retrieve the news
            nickname = userInfo.nickname()
            error = "I am sorry, %s, but I could not retrieve the news." % (
                                                                      nickname)
            speechManager.speakText(error)
        for story in topStories: # Speak each story
            speechManager.speakText(story)

def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return News