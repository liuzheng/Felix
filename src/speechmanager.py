import os
import audioop
import pyaudio
from wave import open as openAudio
import re

class SpeechManager(object):

    def __init__(self, speechIn, speechOut):
        """
        Initializes the Speech instance
        Sets constants for audio analysis
        """
        self.speechIn = speechIn
        self.speechOut = speechOut
        self.AMBIENT_MULTIPLIER = 1.8 # Leeway to distinguish from ambient noise
        self.DATA_RATE = 16000 # Rate of the audio data
        self.BUFFER_SIZE = 1024 # Amount of frames per buffer for audio data

    def getLevel(self, data):
        """
        Returns the level of an audio data file
        """
        level = audioop.rms(data, 2)
        # Need to scale the level down to prevent false positives
        # Value determined through trial and error
        dampeningScale = 1.0 / 3.0
        return int(level * dampeningScale)

    def getAmbientBase(self):
        """
        Listens to ambient noise and returns a level to be used as the base
        """
        LISTEN_TIME = 1 # Time alloted to calculate ambient base

        # Initialize audio stream
        audio = pyaudio.PyAudio()
        stream = audio.open(format = pyaudio.paInt16, channels = 1,
                            rate = self.DATA_RATE, input = True,
                            frames_per_buffer = self.BUFFER_SIZE)

        # Store level values
        dataPoints = 20 # Amount of level data; higher is precise but s    low
        levels = [i for i in range(dataPoints)]

        # Calculate average level for ambient base
        for i in range(0, (self.DATA_RATE / self.BUFFER_SIZE) * LISTEN_TIME):
            data = stream.read(self.BUFFER_SIZE)
            levels.pop(0)
            levels.append(self.getLevel(data))
            average = sum(levels) / len(levels)

        # Calculate ambient base and stop audio collection
        ambientBase = average * self.AMBIENT_MULTIPLIER
        stream.stop_stream()
        stream.close()
        audio.terminate()
        return ambientBase

    def listenForIdentifier(self, IDENTIFIER):
        """
        Listens for IDENTIFIER (default is 'Felix')
        """
        FILENAME = "identifier.wav"
        LISTEN_TIME = 10 # Time allotted to listening before process restarts
        ambientBase = self.getAmbientBase()

        # Initialize audio stream
        audio = pyaudio.PyAudio()
        stream = audio.open(format = pyaudio.paInt16, channels = 1,
                            rate = self.DATA_RATE, input = True,
                            frames_per_buffer = self.BUFFER_SIZE)

        # Listening for sound above ambient base
        frames = []
        soundDetected = False
        for i in range(0, (self.DATA_RATE / self.BUFFER_SIZE) * LISTEN_TIME):
            data = stream.read(self.BUFFER_SIZE)
            frames.append(data)
            level = self.getLevel(data)
            if level > ambientBase:
                soundDetected = True
                break

        # Stop current steam if no sound detected
        if not soundDetected:
            print "No sound detected"
            stream.stop_stream()
            stream.close()
            audio.terminate()
            return None

        # Else, sound was detected and must be checked for IDENTIFIER
        # Cutoff recording before disturbance was detected
        disturbanceBuffer = 20
        frames = frames[-disturbanceBuffer:]

        # Finish recording
        for i in xrange(0, (self.DATA_RATE / self.BUFFER_SIZE)):
            data = stream.read(self.BUFFER_SIZE)
            frames.append(data)

        # Save audio data and stop audio collection
        stream.stop_stream()
        stream.close()
        audio.terminate()
        write_frames = openAudio(FILENAME, "wb")
        write_frames.setnchannels(1)
        write_frames.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        write_frames.setframerate(self.DATA_RATE)
        write_frames.writeframes("".join(frames))
        write_frames.close()

        # Obtain text from speech and check if it contains IDENTIFIER
        text = self.speechIn.textFromSpeech(FILENAME, isIdentifier = True)
        if IDENTIFIER.upper() in text.upper(): return ambientBase
        else: return False

    def listen(self, ambientBase=None, isFullVocabulary=False):
        """
        Actively listens to user speech
        Records until 1 second of silence
        Time-out after 5 seconds of initial silence
        """
        FILENAME = "speech.wav"
        SOUNDNAME = "media-folder/beep.wav"
        TIMEOUT_LOOP = 20

        if ambientBase == None:
            ambientBase = self.getAmbientBase()

        # TONE IN
        self.speechOut.play(SOUNDNAME)

        # Initialize audio stream
        audio = pyaudio.PyAudio()
        stream = audio.open(format = pyaudio.paInt16, channels = 1,
                            rate = self.DATA_RATE, input = True,
                            frames_per_buffer = self.BUFFER_SIZE)

        frames = []
        # Initialize list of levels
        dataPoints = 30 # Amount of level data; higher is precise but slow
        levels = [ambientBase for i in range(dataPoints)]
        # Listening for sound above ambientBase
        for i in range(0, TIMEOUT_LOOP * self.DATA_RATE / self.BUFFER_SIZE):
            data = stream.read(self.BUFFER_SIZE)
            frames.append(data)
            level = self.getLevel(data)
            levels.pop(0)
            levels.append(level)
            average = sum(levels) / float(len(levels))
            # Need to scale the level down to prevent false positives
            # Value determined through trial and error
            dampeningScale = 3.0 / 4.0
            if average < ambientBase * dampeningScale: break

        # Save audio data and stop audio collection
        stream.stop_stream()
        stream.close()
        audio.terminate()
        write_frames = openAudio(FILENAME, "wb")
        write_frames.setnchannels(1)
        write_frames.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        write_frames.setframerate(self.DATA_RATE)
        write_frames.writeframes("".join(frames))
        write_frames.close()

        # TONE OUT
        self.speechOut.play(SOUNDNAME)

        # Return text from speech
        text = self.speechIn.textFromSpeech(FILENAME, isFullVocabulary = isFullVocabulary)
        return text

    def speakText(self, text):
        """
        Plays a sound file created from a string of output text
        """
        text = SpeechManager.formatForSpeech(text)
        self.speechOut.speakText(text)

    @staticmethod
    def formatYears(text):
        """
        Ensures that years are pronounced correctly instead of as numbers
        """
        YEAR_REGEX = re.compile(r"(\b)(\d\d)([1-9]\d)(\b)")
        return YEAR_REGEX.sub("\g<1>\g<2> \g<3>\g<4>", text)

    @staticmethod
    def formatForSpeech(text):
        """
        Cleans a string text using all format functions
        The list of functions is extendible
        When creating a new format function, add it to formatFunctions
        """
        formatFunctions = [SpeechManager.formatYears]
        for formatFn in formatFunctions:
            text = formatFn(text)
        return text
