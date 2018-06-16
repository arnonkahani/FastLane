import sys
sys.path.append('../')
from flask import json
from geojson import LineString
from shapely.geometry import LineString as ShapelyLineString, mapping
import requests



server_ip = 'https://fastlanes-data-processing.herokuapp.com'
headers = {'Content-Type': 'application/json'}

def setDefaultHours():
    hours = {}
    for key in range(0, 24):
        hours[key] = 0
    return hours


def getTrips(geoJson):
    lineStringGeo = LineString(geoJson)
    jsonLineStringGeo = json.dumps(lineStringGeo)
    data = requests.post('http://db:3001/stops_times/square', json=jsonLineStringGeo)
    return data.content


def getTripsPaths(geoJson):
    lineStringGeo = LineString(geoJson)
    jsonLineStringGeo = json.dumps(lineStringGeo)
    data = requests.post('http://db:3001/trips/area', json=jsonLineStringGeo)
    return data.content

def getStopsByPath(geoJson):
    points_from_json = list(map(lambda point: (point['lat'],point['lng']),geoJson))
    lineStringGeo = ShapelyLineString(points_from_json)
    jsonLineStringGeo = json.dumps(mapping(lineStringGeo))
    data = requests.post('http://db:3001/stop/path', json=jsonLineStringGeo)
    return data.content


def addAnalytics(analytics):
    data = requests.post('http://db:3001/analytics', json=analytics)
    return data

def getAnalytics():
    data = requests.get('http://db:3001/analytics')
    return data.content