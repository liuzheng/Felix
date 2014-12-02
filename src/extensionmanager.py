"""
extensionmanager.py
Devin Gund + deg + Section E

Manages all extensions that provide Felix's features
Reads and executes each extension in the extensions folder
"""

import os
import languagecompiler

class ExtensionManager(object):
    def __init__(self):
        """
        Initializes all extensions for use with Felix
        """
        self.extensions = []
        self.speechManager = None
        self.memoryManager = None
        self.loadExtensions()
        self.sortExtensions()
        self.compileLanguage()

    def loadExtensions(self, folder="extensions-folder"):
        """
        Imports each extension class in the 'extensions' folder
        """
        extensions = []
        print "IMPORTING EXTENSIONS..."
        for extensionName in os.listdir(folder):
            if extensionName.endswith(".py") and extensionName != "__init__.py":
                extensionName = extensionName.replace(".py", "")
                # Get full path to extension
                extensionName = "%s.%s" % (folder, extensionName)
                print "IMPORTING:", extensionName
                # Import extension and add its contained class to extensions
                extensionFile = __import__(extensionName)
                components = extensionName.split(".")
                for component in components[1:]:
                    extensionFile = getattr(extensionFile, component)
                extensionClass = extensionFile.getExtension()
                extension = extensionClass()
                self.extensions.append(extension)
        print "DONE!\n"

    def sortExtensions(self):
        """
        Sorts each extension by precedence
        The lower extension.getPrecedence() means that extension
            gets executed if two extensions should execute
        """
        # Sort self.extensions from low to high in order of precedence
        self.extensions.sort(key = lambda extension: extension.getPrecedence())

    def compileLanguage(self, corpus="language-folder/corpus.txt",
                        dictionary="language-folder/dictionary.dic",
                        languagemodel="language-folder/languagemodel.lm"):
        """
        Creates a list of all of the 'keys' for each module
        Uses the keys to compile the proper dictionary and language model
        """
        print "COMPILING LANGUAGE MODEL..."
        keys = set()
        for extension in self.extensions:
            # Obtain keys from each extension
            for key in extension.getKeys(): keys.add(key)
        languagecompiler.compileKeys(list(keys), corpus,
                                     dictionary, languagemodel)
        print "DONE!\n"

    def execute(self, input, memoryManager, userInfo):
        """
        Given a text input from the user, executes the proper extension
        """
        for extension in self.extensions:
            # Check if each extension should execute (if it matches the input)
            if extension.shouldExecute(input):
                extension.execute(input, self.speechManager, memoryManager, userInfo)
                break