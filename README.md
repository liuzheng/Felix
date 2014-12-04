Felix
=====
Felix is an intelligent personal assistant with speech recognition and text-to-speech abilities. In essence, Felix will listen to user speech, and respond with pertinent information or an action. Its features come in the form of "extensions," which are class files that handle a particular speech input (ex. the user asking about the time) by returning related data (ex. returning the current time to be spoken to the user). Felix runs on a Raspberry Pi computer for portability and convenience. It is also designed to understand speech without the need of the Internet; offline processes are favored heavily over online in order to preserve autonomy of the program.

*&copy; 2014 Devin Gund. All rights reserved. Website at [dgund.com](http://dgund.com).*

**Features Overview:**
- Briefing of current events and information
- Aggregated news and weather reports
- Notification of reminders
- Web integration
- Modular design allows for simple extension and addition of features

**User Interaction Overview:**

1. User: "Felix"
2. Felix: "Yes, User"
3. Felix: _beeps_
4. User: _speaks command_ (ex. "What time is it?" or "Search Wikipedia.")
5. Felix: _beeps_
6. Felix: _speaks response_ (ex. "The time is 3:15pm.") or _asks for more input_ (ex. "Please speak your search query.")

**Modules Utilized:**
- [aplay](http://linux.die.net/man/1/aplay) – command line audio recorder and player for ALSA soundcard driver
- [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/) – screen scraping library for parsing web pages
- [eSpeak](http://espeak.sourceforge.net/) – text to speech option
- [Flite](http://www.speech.cs.cmu.edu/flite/index.html) – text to speech option
- [Pocketsphinx](http://cmusphinx.sourceforge.net/) – speech to text
- [PyAudio](http://people.csail.mit.edu/hubert/pyaudio/) – audio library for sampling sound from a stream
- [Python for Facebook](https://github.com/pythonforfacebook/facebook-sdk) – provides tools for working with the Facebook API and Graph Search

The following modules are used to generate speech language models offline and dynamically for Pocketsphinx, and were
recommended by the creators of Pocketsphinx at CMU on [their tutorial](http://cmusphinx.sourceforge.net/wiki/tutoriallm):
- [Bison](http://www.gnu.org/software/bison/) – converting an annotated context-free grammar into an LR parser
- [CMU-Cambridge Statistical Language Modeling Toolkit](http://www.speech.cs.cmu.edu/SLM/toolkit_documentation.html) – building statistical language models
- [M2M-aligner](https://code.google.com/p/m2m-aligner/) – letter to phoneme conversion
- [MIT Language Modeling Toolkit](https://code.google.com/p/mitlm/) – building statistical language models
- [OpenFST](http://www.openfst.org) – weighting the words in the model
- [Phonetisaurus](https://code.google.com/p/phonetisaurus/) – grapheme to phoneme conversion

**Structure:**
- main.py – Called to begin the program; initializes program managers and the Felix instance
- felix.py – Controls the program, looping, checking for speech, and running extensions
- extensionsmanager.py – In charge of importing the extension files and running them
- extension.py – Parent class for all extensions; handles regular expression matching to determine if extension should execute
- languagecompiler.py – Builds language models from the words defined in extensions
- speechmanager.py – Controls the speech-to-text and text-to-speech abilities of Felix
- speechin.py – Wrapper file for Pocketsphinx; implements easy methods to use
- speechout.py – Wrapper file for eSpeak or Flite; implements easy methods to use
- memorymanager.py – Keeps track of Felix's memories (ex. reminders)
- userinfo.py – Keeps track of important user data (ex. name, location, timezone)
- setup.py – May be called separately from the program to initialize user data

**Extensions:**

On top of the core structure of Felix, the different features of interaction with the user come from extensions, which are
classes in extension-folder that inherit from Extension, the parent class for all extensions.
- brief.py – Responds with a brief for the current situation
- demo.py – Responds with an overview of the Felix system and how it works
- facebooknotifications.py – Responds with a summary of [Facebook](https://www.facebook.com/) notifications
- jokes.py – Responds with a random computer joke, taken from jokes.txt
- life.py – Responds with the meaning of life
- name.py – Responds with its name (Felix)
- news.py – Responds with the five top news stories on [Google News](http://news.google.com)
- reminders.py – Responds with the current list of reminders and allows for adding reminders
- time.py – Responds with the current time and date for the user's time zone
- undefined.py – Responds with a message telling the user their speech was unclear
- username.py – Responds with the name of the user
- weather.py – Responds with the current weather and forecast for the user location from [Weather Underground](http://www.wunderground.com/)
- wikipedia.py – Responds by asking for a query and then with a summary of the query on [Wikipedia](https://en.wikipedia.org/)
