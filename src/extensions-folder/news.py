"""
news.py
Responds with the five top news stories
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
    def getNews():
        """
        Returns the five top stories on news.google.com
        """
        NEWS_URL = "http://news.google.com/?output=rss"
        feed = feedparser.parse(NEWS_URL)
        entries = feed.entries
        topStories = []
        for entry in entries:
            if len(topStories) >= 5: break
            title = entry.title
            topStories.append(title)
        return topStories

    def execute(self, input, speechManager, userInfo):
        """
        Called when the extension must execute
        Responds with the five top news stories
        """
        speechManager.speakText("Here are your five top news stories.")
        topStories = News.getNews()
        if len(topStories) == 0:
            # If unable to retrieve the news
            nickname = userInfo.nickname()
            error = "I am sorry, %s, but I could not retrieve the news." % (nickname)
            speechManager.speakText(error)
        for story in topStories:
            speechManager.speakText(story)

def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return News
