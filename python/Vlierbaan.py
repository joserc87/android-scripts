import urllib
import urllib2
import json
import android

# API: https://github.com/oleander/9292-nl-api-spec
class WebServiceHelper:

	# The default server
	SERVER = 'https://api.9292.nl/'

	def __init__(self):
		""" Constructor """
		self.server = WebServiceHelper.SERVER
		self.stationID = 'capelle-aan-den-ijssel/bushalte-vlierbaan'

	def getLocationsURL(self, stationName):
		""" Builds the URL to login a user in the system: https://api.apalabrados.com/api/login """
		return self.server + '0.1/locations?lang=en-GB&type=station,stop&q=' + stationName

	def getDepartureTimesURL(self, stationID):
		""" Builds the URL to retrieve the list of games: https://api.apalabrados.com/api/users/[UserID]/games """
		return self.server + '0.1/locations/' + stationID + '/departure-times?lang=en-GB'

	def searchLocation(self, stationName):
		""" Calls https://api.9292.nl/0.1/locations?lang=en-GB&type=station,stop&q=[stationName]/ returns the list of matching stations """
		try:
			# GET
			handler = urllib.urlopen(self.getLocationsURL(stationName))
			data = handler.read()
			jsonObj = json.loads(data)
			locations = jsonObj['locations']
			if len(locations) >= 1:
				self.stationID = locations[0]['id']
				return jsonObj
			else:
				print 'Error'
				return None
		except:
			print "Unexpected error"
			raise
		return None

	def getDepartureTimes(self, stationID = None):
		""" Calls https://api.9292.nl/0.1/locations/[StationID]/departure-times?lang=en-GB returns the list of matching stations """
		stationID = stationID or self.stationID
		try:
			# GET
			handler = urllib.urlopen(self.getDepartureTimesURL(stationID))
			data = handler.read()
			jsonObj = json.loads(data)
			return jsonObj

		except:
			print "Unexpected error"
			raise
		return None

def timeToText(time):
	div = time.split(':')
	hour = div[0]
	minutes = div[1]
	h = int (hour)
	m = int (minutes)
	h = h if h <= 12 else h-12
	if h == 0:
		h = 12
	h1 = h+1 if h+1 <= 12 else h-11
	if h1 == 0:
		h1 = 12

	hour = str(h)

	if m == 0:
		text = hour + ' en punto'
	if m == 5:
		text = hour + ' y 5'
	if m == 10:
		text = hour + ' y 10'
	if m == 15:
		text = hour + ' y cuarto'
	if m == 20:
		text = hour + ' y 20'
	if m == 30:
		text = hour + ' y media'
	if m == 40:
		text = str(h1) + ' menos 20'
	if m == 45:
		text = str(h1) + ' menos cuarto'
	if m == 50:
		text = str(h1) + ' menos 10'
	if m == 55:
		text = str(h1) + ' menos 5'
	else:
		text = hour + ' y ' + minutes
	return text



if __name__ == "__main__":
	droid = android.Android()
	server = WebServiceHelper()
	result = server.getDepartureTimes()
	departures = result['tabs'][0]['departures']
	times = []
	for departure in departures:
		if departure['destinationName'] == 'Rotterdam':
			times.append(departure['time'])

	text = 'el autobus pasa a las '
	i=0
	for t in times[:2]:
		text = text + timeToText(t) + (' y a las ' if i==0 else '')
		i += 1
	print text
	droid.ttsSpeak(text)



"""
EXAMPLE:
searchLocations('Noordwal')
Returns:
{
  "locations": [
    {
      "id": "den-haag/tramhalte-noordwal-1",
      "type": "stop",
      "stopType": "Tram stop",
      "name": "Noordwal",
      "place": {
        "name": "Den Haag",
        "regionCode": "ZH",
        "regionName": "South Holland",
        "showRegion": false,
        "countryCode": "NL",
        "countryName": "The Netherlands",
        "showCountry": false
      },
      "latLong": {
        "lat": 52.079923,
        "long": 4.302473
      },
      "urls": {
        "nl-NL": "/den-haag/tramhalte-noordwal-1",
        "en-GB": "/en/den-haag/tramhalte-noordwal-1"
      }
    }
  ]
}

{
  "location": {
    "id": "den-haag/tramhalte-noordwal-1",
    "type": "stop",
    "stopType": "Tram stop",
    "name": "Noordwal",
    "place": {
      "name": "Den Haag",
      "regionCode": "ZH",
      "regionName": "South Holland",
      "showRegion": false,
      "countryCode": "NL",
      "countryName": "The Netherlands",
      "showCountry": false
    },
    "latLong": {
      "lat": 52.079923,
      "long": 4.302473
    },
    "urls": {
      "nl-NL": "/den-haag/tramhalte-noordwal-1",
      "en-GB": "/en/den-haag/tramhalte-noordwal-1"
    }
  },
  "tabs": [
    {
      "id": "tram",
      "name": "Tram",
      "locations": [
        {
          "id": "den-haag/tramhalte-noordwal-1",
          "type": "stop",
          "stopType": "Tramhalte",
          "name": "Noordwal",
          "place": {
            "name": "Den Haag",
            "regionCode": "ZH",
            "regionName": "Zuid-Holland",
            "showRegion": false,
            "countryCode": "NL",
            "countryName": "Nederland",
            "showCountry": false
          },
          "latLong": {
            "lat": 52.079923,
            "long": 4.302473
          },
          "urls": {
            "nl-NL": "/den-haag/tramhalte-noordwal-1",
            "en-GB": "/en/den-haag/tramhalte-noordwal-1"
          }
        }
      ],
      "departures": [
        {
          "time": "21:26",
          "destinationName": "Wateringen",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "21:29",
          "destinationName": "Statenkwartier",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "21:41",
          "destinationName": "Wateringen",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "21:44",
          "destinationName": "Statenkwartier",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "21:56",
          "destinationName": "Wateringen",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "21:59",
          "destinationName": "Statenkwartier",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "22:11",
          "destinationName": "Wateringen",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "22:14",
          "destinationName": "Statenkwartier",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "22:26",
          "destinationName": "Wateringen",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "22:29",
          "destinationName": "Statenkwartier",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "22:40",
          "destinationName": "Wateringen",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "22:44",
          "destinationName": "Statenkwartier",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "22:55",
          "destinationName": "Wateringen",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "22:59",
          "destinationName": "Statenkwartier",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        },
        {
          "time": "23:10",
          "destinationName": "Wateringen",
          "viaNames": null,
          "mode": {
            "type": "tram",
            "name": "Tram"
          },
          "operatorName": "HTM",
          "service": "17",
          "platform": null,
          "platformChanged": false,
          "remark": null,
          "realtimeState": "ontime",
          "realtimeText": null
        }
      ]
    }
  ]
}
"""


