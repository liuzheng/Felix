"""
wikipedia.py
Devin Gund + deg + Section E

Responds by first asking the user for their search query
Then responds with the summary of the query on Wikipedia

Utilizes modules:
    - BeautifulSoup

Information for working with BeautifulSoup provided from:
    http://www.crummy.com/software/BeautifulSoup/bs4/doc/
"""

from extension import Extension
import urllib
import urllib2
from bs4 import BeautifulSoup
import re

class Wikipedia(Extension):
    def __init__(self):
        """
        Initializes the Wikipedia extension
        """
        # Regular expression to match extension
        matchExpression = "wikipedia"
        # Key words that Felix must compile into the language model
        keys = ["WIKIPEDIA", "SEARCH"]
        # Extension with lower precedence gets executed in a tie
        precedence = 2
        super(Wikipedia, self).__init__(matchExpression, keys, precedence)

    @staticmethod
    def getArticleSummary(query, count=3):
        """
        Returns a summary for the Wikipedia article for the query
        This summary is pulled from the first paragraph of the article
        Utilizes the BeautifulSoup module for HTML parsing
        """
        if len(query) == 0: return None # If the query is blank
        article = urllib.quote(query)
        opener = urllib2.build_opener()
        opener.addheaders = [("User-agent", "Mozilla/5.0")] # Set user agent
        summary = None
        try:
            resource = opener.open("http://en.wikipedia.org/wiki/" + article)
            data = resource.read()
            resource.close()
            soup = BeautifulSoup(data)
            summary = soup.find("div",id="bodyContent").p.get_text()
            summary = re.sub(r"\( listen\)", "", summary) # Remove listen tag
            summary = re.sub(r"\(.*?\)", "", summary) # Remove parantheticals
            summary = re.sub(r"\[.*?\]", "", summary) # Remove citations
            summary = re.sub(r"  ", " ", summary) # Remove extra spaces
            summary = re.sub(r" \.", ".", summary) # Format periods
            summary = re.sub(r" \,", ",", summary) # Format commas
            summary.replace("\"", "") # Remove quotation marks
            # Limit number of sentences to number specified in count
            summary = " ".join(re.split(r"(?<=[.?!])\s+", summary, count)[:-1])
        except:
            print "Error retrieving information."
        return summary

    def execute(self, input, speechManager, memoryManager, userInfo):
        """
        Called when the extension must execute
        Responds with a current weather report for the user's location
        """
        speechManager.speakText("Please speak your search query.")
        query = speechManager.listen(isFullVocabulary = True)
        # Remove 'and' from beginning of query (sometimes Pocketsphinx adds it)
        removeStr = "and "
        if query.startswith(removeStr): query = query[len(removeStr):]
        speechManager.speakText("One moment. Searching for %s." % (query))
        summary = Wikipedia.getArticleSummary(query)
        if summary:
            speechManager.speakText(summary)
        else:
            error = "I am sorry, but I could not retrieve that article."
            speechManager.speakText(error)

def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return Wikipedia