"""
weather.py
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
        precedence = 0
        super(Weather, self).__init__(matchExpression, keys, precedence)

    @staticmethod
    def getWeather(apiKey, state, city) :
        """
        Returns a weather report for the user's location
        Includes current conditions and a future forecast
        """
        WEATHER_CURRENT_URL = "http://api.wunderground.com/api/%s/geolookup/conditions/q/%s/%s.json" % (apiKey, state, city)
        WEATHER_FORECAST_URL = "http://api.wunderground.com/api/%s/forecast/q/%s/%s.json"  % (apiKey, state, city)
        weather = ""

        response = urllib2.urlopen(WEATHER_CURRENT_URL)
        jsonString = response.read()
        data = json.loads(jsonString)
        
        location = str(data["location"]["city"])
        description = str(data['current_observation']['icon'])
        currentTemperature = str(data["current_observation"]["temp_f"])
        weather += ("The current weather in %s is %s with a temperature of %s degrees Fahrenheit." % (location, description, currentTemperature))

        response = urllib2.urlopen(WEATHER_FORECAST_URL)
        jsonString = response.read()
        data = json.loads(jsonString)
        
        today = data['forecast']['simpleforecast']['forecastday'][0]
        description = str(today['conditions'])
        highTemperature = str(today['high']['fahrenheit'])
        lowTemperature = str(today['low']['fahrenheit'])
        weather += (" Today's weather will be %s, with a high temperature of %s degrees Fahrenheit and a low of %s degrees Fahrenheit." % (description, highTemperature, lowTemperature))
        
        tomorrow = data['forecast']['simpleforecast']['forecastday'][1]
        description = str(tomorrow['conditions'])
        highTemperature = str(tomorrow['high']['fahrenheit'])
        lowTemperature = str(tomorrow['low']['fahrenheit'])
        weather += (" Tomorrow's weather will be %s, with a high temperature of %s degrees Fahrenheit and a low of %s degrees Fahrenheit." % (description, highTemperature, lowTemperature))
        
        return weather

    def execute(self, input, speechManager, userInfo):
        """
        Called when the extension must execute
        Responds with a current weather report for the user's location
        """
        speechManager.speakText("Here is the current weather.")
        apiKey = userInfo.wundergroundKey()
        state = userInfo.locationState()
        city = userInfo.locationCity()
        weather = Weather.getWeather(apiKey, state, city)
        if len(weather) == 0:
            # If unable to retrieve the news
            nickname = userInfo.nickname()
            error = "I am sorry, %s, but I could not retrieve the weather." % (nickname)
            speechManager.speakText(error)
        else:
            speechManager.speakText(weather)

def getExtension():
    """
    Returns the extension class in the file
    Used during the extension importing process
    """
    return Weather