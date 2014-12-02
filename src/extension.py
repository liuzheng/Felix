"""
extension.py
Devin Gund + deg + Section E

The Extension class serves as the parent class for all custom extensions
"""

import re
import copy

class Extension(object):
    def __init__(self, matchExpression="", keys=[], precedence=0):
        """
        Initializes the Extension instance
        This Extension class should be subclassed to create custom extensions
        Parameters:
        matchExpression - The piece of input that refers to this extension
        keys - The keywords that must be added to the language model
        precedence - If multiple extensions match, lower precedence executes
        """
        self.matchExpression = matchExpression
        self.keys = keys
        self.precedence = precedence

    def __eq__(self, other):
        """
        Extension instances / subclasses are equal if precedences are equal
        """
        if not isinstance(other, extension): return False
        return self.precedence == other.precedence

    def __gt__(self, other):
        """
        Extension instance is greater if precedence is greater
        """
        if not isinstance(other, extension): return False
        return self.precedence > other.precedence

    def __lt__(self, other):
        """
        Extension instance is less if precedence is less
        """
        if not isinstance(other, extension): return False
        return self.precedence < other.precedence

    def __ge__(self, other):
        """
        An extension instance is greater/equal if precedence is greater/equal
        """
        return __gt__(self, other) or __eq__(self, other)

    def __le__(self, other):
        """
        An extension instance is less/equal if precedence is less/equal
        """
        return __lt__(self, other) or __eq__(self, other)

    def shouldExecute(self, input):
        """
        Returns True if the input is related to this extension
        """
        snippet = self.matchExpression
        # Account for case where snippet can match anything (or nothing)
        if snippet != ".*": snippet = r"\b" + snippet + r"\b"
        # Regex earches for self.matchExpression within the input
        isMatch = bool(re.search(snippet, input, re.IGNORECASE))
        return isMatch

    def execute(self, input, speechManager, memoryManager, userInfo):
        """
        Responds to user input with pertinent information or actions
        Overridden in any custom extension to provide functionality
        """
        pass

    def getKeys(self):
        """
        Returns the keys of the extension
        The keys are the keywords that must be added to the language model
        """
        return copy.copy(self.keys)

    def getPrecedence(self):
        """
        Returns the precedence of the extension
        If multiple extensions match, extension of lower precedence executes
        """
        return self.precedence