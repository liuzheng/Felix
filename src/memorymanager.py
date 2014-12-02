"""
memorymanager.py
Devin Gund + deg + Section E

Keeps track of Felix's memories
Keeps track of reminders
"""

import datetime
import pytz
import copy

try: import cPickle as pickle
except: import pickle

class MemoryManager(object):
    def __init__(self, userInfo):
        """
        Initializes all MemoryManager instance
        """
        self.reminders = []
        self.timezone = pytz.timezone(userInfo.timezone())
        self.speechManager = None
        self.readMemory()

    def cleanMemory(self):
        """
        Checks for and removes any memories that have expired
        """
        currentTime = datetime.datetime.now(tz = self.timezone)
        # Remove any expired reminders (reminderTime - currentTime > 1 day)
        reminders = []
        for reminder in self.reminders:
            # If reminder time is greater than current time add it to reminders
            reminderTime = reminder[1]
            difference = currentTime - reminderTime
            if difference.days < 1: reminders.add(reminder)
        self.reminders = reminders
        self.writeMemory(self) # Write memory to file

    def getReminders(self):
        """
        Returns the list of reminder messages
        """
        messages = []
        for reminder in self.reminders: messages.append(reminder[0])
        return messages

    def addReminder(self, message):
        """
        Adds a message to the list of reminders
        A reminder is a tuple of the reminder message and the time created
        """
        currentTime = datetime.datetime.now(tz = self.timezone)
        reminder = (message, currentTime)
        self.reminders.append(reminder)
        self.writeMemory()

    def readMemory(self):
        """
        Readers memory from memory.p
        Memory comes in the form of reminders
        """
        reminders = []
        try:
            memory = pickle.load(open("memory.p", "rb"))
            reminders = memory[0]
        except: print "memorymanager.py: Error reading memory."
        self.reminders = reminders

    def writeMemory(self):
        """
        Writes memory to memory.p
        """
        memory = [self.reminders]
        try: pickle.dump(memory, open("memory.p", "wb"))
        except: print "memorymanager.py: Error writing memory."