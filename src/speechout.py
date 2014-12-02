"""
speechout.py
Devin Gund + deg + Section E

Encapsulates any text-to-speech applications used with Felix

Utilizes modules:
    - eSpeak or flite
    - aplay

Information for working with eSpeak provided from:
    http://espeak.sourceforge.net/commands.html

Information for working with flite provided from:
    http://www.festvox.org/flite/doc/flite_7.html#SEC15

Information for working with aplay provided from:
    http://linux.die.net/man/1/aplay
"""

import os

class eSpeak(object):
    """
    eSpeak is a compact open source software speech synthesizer
    To use this for output, eSpeak must be installed on the intended device
    """
    @staticmethod
    def isInstalled():
        """
        Returns if eSpeak is installed by running 'which espeak' on command line
        """
        return os.system("which espeak") == 0

    def speakText(self, text,
                 conversionParams="-ven+m4 -p 50 -s 140 --stdout > output.wav"):
        """
        Plays a sound file created from a string of output text
        """
        os.system("espeak %s \"%s\"" % (conversionParams, text))
        self.play("output.wav")

    def play(self, file):
        """
        Plays a sound file using aplay
        Command syntax and parameters obtained from aplay man page
        """
        os.system("aplay -D hw:1,0 %s" % file)

class Flite(object):
    """
    eSpeak is a compact open source software speech synthesizer
    To use this for output, eSpeak must be installed on the intended device
    """
    @staticmethod
    def isInstalled():
        """
        Returns if flite is installed by running 'which flite' on command line
        """
        return os.system("which flite") == 0

    def speakText(self, text,
                 conversionParams="-voice kal -o output.wav"):
        """
        Plays a sound file created from a string of output text
        """
        os.system("echo \"%s\" | flite %s" % (text, conversionParams))
        self.play("output.wav")

    def play(self, file):
        """
        Plays a sound file using aplay
        Command syntax and parameters obtained from aplay man page
        """
        os.system("aplay -D hw:1,0 %s" % file)

def speechOutEngine():
    """
    Returns a TTS engine for use with Felix
    The list of engines is extendible
    When creating a new class, add it to speechClasses
    Any TTS class must implement isInstalled(), speakText(), and play()
    """
    speechClasses = [eSpeak, Flite]
    for speechClass in speechClasses:
        if speechClass.isInstalled(): return speechClass()
    print "ERROR speechout.py: No text-to-speech engines available"
    return False