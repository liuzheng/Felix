"""
speechin.py
Encapsulates any speech-to-text applications used with Felix
"""

import os

class PocketSphinx(object):
    def __init__(self,
                 MODEL = "/usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k",
                 LANGUAGE_FOLDER="language-folder/",
                 LANGUAGEMODEL="languagemodel.lm",
                 DICTIONARY="dictionary.dic",
                 LANGUAGEMODEL_IDENTIFIER="languagemodel_identifier.lm",
                 DICTIONARY_IDENTIFIER="dictionary_identifier.dic",
                 LANGUAGEMODEL_FULL="/usr/local/share/pocketsphinx/model/lm/en_US/hub4.5000.DMP",
                 DICTIONARY_FULL="/usr/local/share/pocketsphinx/model/lm/en_US/hub4.5000.dic"):
        """
        PocketSphinx is an open source toolkit for speech recognition
        PocketSphinx is developed by researchers at Carnegie Mellon University
        """
        try: import pocketsphinx
        except: import pocketsphinx
        # Create the speech decoder for Felix commands
        self.speechDecoder = pocketsphinx.Decoder(hmm=MODEL,
                                       lm=LANGUAGE_FOLDER + LANGUAGEMODEL,
                                       dict=LANGUAGE_FOLDER + DICTIONARY)
        # Create the speech decoder for the IDENTIFIER
        self.speechDecoderIdentifier = pocketsphinx.Decoder(hmm=MODEL,
                            lm=LANGUAGE_FOLDER + LANGUAGEMODEL_IDENTIFIER,
                            dict=LANGUAGE_FOLDER + DICTIONARY_IDENTIFIER)
        # Create the speech decoder for full speech vocabulary
        self.speechDecoderFullVocabulary = pocketsphinx.Decoder(hmm=MODEL,
                                  lm=LANGUAGEMODEL_FULL, dict=DICTIONARY_FULL)
    
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
        if text == None: text = ""
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
