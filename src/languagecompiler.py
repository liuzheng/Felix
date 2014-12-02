"""
languagecompiler.py
Devin Gund + deg + Section E

Dynamically generates files for Felix's speech recognition
Compiles the corpus file, dictionary, and language model

Utilizes modules:
    - CMU-Cambridge Statistical Language Modeling Toolkit
    - MIT Language Modeling Toolkit
    - OpenFST
    - M2M-aligner
    - Phonetisaurus

Information for generating language models provided from:
    http://cmusphinx.sourceforge.net/wiki/tutoriallm
"""
import os
import subprocess
import re

def compileKeys(keys, corpus, dictionary, languagemodel):
    """
    Main function
    Compiles language using keys from each extension
    Creates a corpus file, dictionary, and language model
    """
    createCorpus(keys, corpus)
    createDictionary(keys, dictionary)
    createLanguageModel(corpus, languagemodel)

def createCorpus(keys, corpus):
    """
    Creates a corpus file for Pocketsphinx and the language model
    A corpus file consists of a list of the keys
    """
    with open(corpus, "w") as corpusFile:
        corpusFile.write("\n".join(keys) + "\n")
        corpusFile.write("<s> \n </s> \n")
        corpusFile.close()

def translateGraphemesToPhonemes(words, tempFile="g2p-temp",
                              model="/home/pi/phonetisaurus/g014b2b.fst"):
    """
    Translates a list of words to the language model format
    Returns the phonemes for each word, using Phonetisaurus
    """
    phoneticMatch = re.compile(r"<s> (.*) </s>")
    # Write the list of words to a temporary file
    text = "\n".join(words)
    with open(tempFile, "wb") as translateTemp:
        translateTemp.write(text)
        translateTemp.flush()
        translateTemp.close()
    # Translate the file using Phonetisaurus and remove the file
    commands = ["phonetisaurus-g2p", "--model=%s" % model,
                "--input=%s" % tempFile, "--words", "--isfile"]
    output = subprocess.check_output(commands)
    os.remove(tempFile)
    # Parse the translated text and return phonemes
    return phoneticMatch.findall(output)    

def createDictionary(keys, dictionary):
    """
    Creates a dictionary for Pocketsphinx using Phonetisaurus
    A dictionary consists of a list of the keys and their phonemes
    """
    # Translate keys to phonemes
    phonemes = translateGraphemesToPhonemes(keys)
    lines = []
    for index in xrange(len(keys)):
        # Group keys and their phonemes
        lines.append("%s %s" % (keys[index], phonemes[index]))
    with open(dictionary, "w") as dictionaryFile:
        # Write each group of key and phonemes to a line
        dictionaryFile.write("\n".join(lines) + "\n")
        dictionaryFile.close()

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