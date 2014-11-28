"""
languagecompiler.py
"""
import os
import subprocess
import re
    
def compileKeys(keys, CORPUS_PATH, DICTIONARY_PATH, LANGUAGEMODEL_PATH):
    """
    Main function
    Compiles the keys from each extension
    Creates a corpus file, dictionary, and language model
    """
    createCorpus(keys, CORPUS_PATH)
    createDictionary(keys, DICTIONARY_PATH)
    createLanguageModel(CORPUS_PATH, LANGUAGEMODEL_PATH)

def createCorpus(keys, CORPUS_PATH):
    """
    Creates a corpus file for Pocketsphinx and the language model
    A corpus file consists of a list of the keys
    """
    with open(CORPUS_PATH, "w") as corpus:
        corpus.write("\n".join(keys) + "\n")
        corpus.write("<s> \n </s> \n")
        corpus.close()

def translateGraphemesToPhonemes(words, TEMPFILE_PATH="g2p-temp",
                              MODEL_PATH="/home/pi/phonetisaurus/g014b2b.fst"):
    """
    Translates a list of words to the language model format
    Returns the phonemes for each word, using Phonetisaurus
    """
    PHONETIC_MATCH = re.compile(r"<s> (.*) </s>")
    # Write the list of words to a temporary file
    text = "\n".join(words)
    with open(TEMPFILE_PATH, "wb") as translateTemp:
        translateTemp.write(text)
        translateTemp.flush()
        translateTemp.close()
    # Translate the file using Phonetisaurus and remove the file
    commands = ["phonetisaurus-g2p", "--model=%s" % MODEL_PATH,
                "--input=%s" % TEMPFILE_PATH, "--words", "--isfile"]
    output = subprocess.check_output(commands)
    os.remove(TEMPFILE_PATH)
    # Parse the translated text and return phonemes
    return PHONETIC_MATCH.findall(output)    

def createDictionary(keys, DICTIONARY_PATH):
    """
    Creates a dictionary for Pocketsphinx using Phonetisaurus
    A dictionary consists of a list of the keys and their phonemes
    """
    phonemes = translateGraphemesToPhonemes(keys) # Translate keys to phonemes
    lines = []
    for index in xrange(len(keys)):
        lines.append("%s %s" % (keys[index], phonemes[index]))
    with open(DICTIONARY_PATH, "w") as dictionary:
        dictionary.write("\n".join(lines) + "\n")
        dictionary.close()

def createLanguageModel(CORPUS_PATH, LANGUAGEMODEL_PATH):
    """
    Creates a language model for Pocketsphinx using text2idngram and idngram2lm
    The keys are first translated to idngram form
    The idngrams are then translated to a languagemodel file
    A language model consists of a weighted data series of the keys
    """
    commands = []
    # Translate the keys in the corpus file to idngram form
    commands.append("text2idngram -vocab %s < %s -idngram temp.idngram" %
                    (CORPUS_PATH, CORPUS_PATH))
    # Translate the idngrams to a languagemodel file
    commands.append("idngram2lm -idngram temp.idngram -vocab %s -arpa %s" %
                    (CORPUS_PATH, LANGUAGEMODEL_PATH))
    for command in commands: os.system(command)
    os.remove("temp.idngram")