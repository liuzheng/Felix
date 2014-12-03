"""
weather.py
Devin Gund + deg + Section E

Responds with a current weather report for the user's location
"""

from extension import Extension
import urllib2
import json

class Weather(Extension):
    def __init__(self):
        """
        Initializes the Weather extension
        """
        # Regular expression to match extension
        matchExpression = "weather|forecast"
        # Key words that Felix must compile into the language model
        keys = ["WEATHER", "FORECAST"]
        # Extension with lower precedence gets executed in a tie
        precedence = 1
        super(Weather, self).__init__(matchExpression, keys, precedence)

    @staticmethod
    def getWeatherCurrent(apiKey, state, city):
        """
        Returns a weather report for current conditions for the user's location
        """
        address = "http://api.wunderground.com/api/%s/" % (apiKey)
        address += "geolookup/conditions/q/%s/%s.json" % (state, city)
        weather = ""
        response = urllib2.urlopen(address)
        jsonString = response.read()
        data = json.loads(jsonString) # Get weather data
        # Get current conditions
        location = str(data["location"]["city"])
        description = str(data["current_observation"]["icon"])
        temperature = str(data["current_observation"]["temp_f"])
        weather += "The current weather in %s is %s " % (location, description)
        weather += "with a temperature of %s degrees." % (temperature)
        return weather

    @staticmethod
    def getWeatherForecast(apiKey, state, city):
        """
        Returns a weather report for forecast conditions for the user's location
        """
        address = "http://api.wunderground.com/api/%s/" % (apiKey)
        address += "forecast/q/%s/%s.json" % (state, city)
        weather = ""
        response = urllib2.urlopen(address)
        jsonString = response.read()
        data = json.loads(jsonString) # Get weather data
        # Get forecast for today and tomorrow
        days = ["Today", "Tomorrow"]
        for index in xrange(len(days)):
            forecast = data["forecast"]["simpleforecast"]["forecastday"][index]
            description = str(forecast["conditions"])
            high = str(forecast["high"]["fahrenheit"])
            low = str(forecast["low"]["fahrenheit"])
            weather += "%s's weather will be %s, " % (days[index], description)
            weather += "with a high temperature of %s degrees " % (high)
            weather += "and a low of %s degrees. " % (low)
        return weather

    def execute(self, input, speechManager, memoryManager, userInfo):
        """
        Called when the extension must execute
        Responds with a current weather report for the user's location
        """
        message = "One moment. Obtaining weather report."
        speechManager.speakText(message)
        apiKey = userInfo.wundergroundKey()
        state = userInfo.locationState()
        city = userInfo.locationCity()
        weatherCurrent = Weather.getWeatherCurrent(apiKey, state, city)
        weatherForecast = Weather.getWeatherForecast(apiKey, state, city)
        if len(weatherCurrent) == 0:
            # If unable to retrieve the weather
            nickname = userInfo.nickname()
            error = "I am sorry, %s, but I could not retrieve the weather." % (nickname)
            speechManager.speakText(error)
        else:
            speechManager.speakText(weatherCurrent)
            speechManager.speakText(weatherForecast)

def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return Weather