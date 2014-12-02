"""
extensionmanager.py
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
    
    def loadExtensions(self):
        """
        Imports each extension class in the 'extensions' folder
        """
        FOLDER = "extensions-folder"
        extensions = []
        print "IMPORTING EXTENSIONS..."
        for extensionName in os.listdir(FOLDER):
            if extensionName.endswith(".py") and extensionName != "__init__.py":
                extensionName = extensionName.replace(".py", "")
                extensionName = "%s.%s" % (FOLDER, extensionName)
                print "IMPORTING:", extensionName
                extensionFile = __import__(extensionName)
                components = extensionName.split(".")
                for component in components[1:]:
                    extensionFile = getattr(extensionFile, component)
                extensionClass = extensionFile.getExtension()
                extension = extensionClass()
                extensions.append(extension)
        self.extensions = extensions
        print "DONE!\n"
        
    def sortExtensions(self):
        """
        Sorts each extension by precedence
        The lower extension.getPrecedence() means that extension
            gets executed if two extensions should execute
        """
        self.extensions.sort(key = lambda extension: extension.getPrecedence())
    
    def compileLanguage(self, CORPUS_PATH="language-folder/corpus.txt",
                        DICTIONARY_PATH="language-folder/dictionary.dic",
                        LANGUAGEMODEL_PATH="language-folder/languagemodel.lm"):
        """
        Creates a list of all of the 'KEYS' for each module
        Uses this to generate the proper language model and dictionary
        """
        print "COMPILING LANGUAGE MODEL..."
        keys = set()
        for extension in self.extensions:
            for key in extension.getKeys():
                keys.add(key)
        languagecompiler.compileKeys(list(keys), CORPUS_PATH,
                                     DICTIONARY_PATH, LANGUAGEMODEL_PATH)
        print "DONE!\n"

    def execute(self, input, memoryManager, userInfo):
        """
        Given a text input from the user, executes the proper extension
        """
        for extension in self.extensions:
            if extension.shouldExecute(input):
                extension.execute(input, self.speechManager, self.memoryManager, userInfo)
                break