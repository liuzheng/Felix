"""
speechin.py
Devin Gund + deg + Section E

Encapsulates any speech-to-text applications used with Felix

Utilizes modules:
    - Pocketsphinx

Information for working with Pocketsphinx provided from:
    http://cmusphinx.sourceforge.net/wiki/tutorialpocketsphinx
"""

import os

class PocketSphinx(object):
    def __init__(self,
                 (acousticModel=
                 "/usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k"),
                 (languageFolder="language-folder/"),
                 (languagemodel="languagemodel.lm"),
                 (dictionary="dictionary.dic"),
                 (languagemodelIdentifier="languagemodel_identifier.lm"),
                 (dictionaryIdentifier="dictionary_identifier.dic"),
                 (languagemodelFull=
                 "/usr/local/share/pocketsphinx/model/lm/en_US/hub4.5000.DMP"),
                 (dictionaryFull=
                 "/usr/local/share/pocketsphinx/model/lm/en_US/hub4.5000.dic")):
        """
        PocketSphinx is an open source toolkit for speech recognition
        PocketSphinx is developed by researchers at Carnegie Mellon University
        """
        # Ensure that Pocketsphinx has been imported
        try: import pocketsphinx
        except: import pocketsphinx
        # Create the speech decoder for Felix commands
        self.speechDecoder = pocketsphinx.Decoder(hmm=acousticModel,
                                       lm=languageFolder + languagemodel,
                                       dict=languageFolder + dictionary)
        # Create the speech decoder for the identifier
        self.speechDecoderIdentifier = pocketsphinx.Decoder(hmm=acousticModel,
                            lm=languageFolder + languagemodelIdentifier,
                            dict=languageFolder + dictionaryIdentifier)
        # Create the speech decoder for full speech vocabulary
        self.speechDecoderFullVocabulary = pocketsphinx.Decoder(
                            hmm=acousticModel, lm=languagemodelFull,
                            dict=dictionaryFull)

    @staticmethod
    def isInstalled():
        """
        Returns if installed by running 'which pocketsphinx_continuous'
        """
        return os.system("which pocketsphinx_continuous") == 0

    def textFromSpeech(self, filePath, isIdentifier=False, isFullVocabulary=False):
        """
        Returns a string containing the probable text from a file of speech
        isIdentifier - if the speech should be transcribed for the IDENTIFIER
        isFullVocabulary - if the speech contains the full english language
        """
        speechDataIndex = 44 # Skip WAV header
        audioFile = file(filePath, "rb")
        audioFile.seek(speechDataIndex)
        textPossibilities = []
        if isIdentifier:
            self.speechDecoderIdentifier.decode_raw(audioFile)
            textPossibilities = self.speechDecoderIdentifier.get_hyp()
        elif isFullVocabulary:
            self.speechDecoderFullVocabulary.decode_raw(audioFile)
            textPossibilities = self.speechDecoderFullVocabulary.get_hyp()
        else:
            self.speechDecoder.decode_raw(audioFile)
            textPossibilities = self.speechDecoder.get_hyp() # Hypothesis
        text = textPossibilities[0]
        if text == None: text = "" # Ensure that text is always string
        print "---------------------------------------------"
        print "Text found:", text
        print "---------------------------------------------"
        return text

def speechInEngine():
    """
    Returns a SST engine for use with Felix
    The list of engines is extendible
    Any SST class must implement isInstalled() and textFromSpeech()
    """
    speechClasses = [PocketSphinx]
    for speechClass in speechClasses:
        if speechClass.isInstalled(): return speechClass()
        print "ERROR speechin.py: No speech-to-text engines available"
        return False