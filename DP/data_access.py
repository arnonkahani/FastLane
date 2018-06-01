import sys
sys.path.append('../')
from flask import jsonify,json
from datetime import datetime
from geojson import LineString
import shapely.geometry
import pickle
from SharedLayer.objects.StopTime import StopTime as StopTimeObj
from SharedLayer.objects.Trip import Trip as TripObj
from SharedLayer.objects.Calender import Calender as CalenderObj
from SharedLayer.objects.Stop import Stop as StopObj
from shapely.geometry import LineString as ShapelyLineString, Point,mapping
import requests
import numpy as np
import matplotlib.pyplot as plt
import random

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
    data = requests.post('http://localhost:3001/stops_times/square', json=jsonLineStringGeo)
    return data.content


def getTripsPaths(geoJson):
    lineStringGeo = LineString(geoJson)
    jsonLineStringGeo = json.dumps(lineStringGeo)
    data = requests.post('http://localhost:3001/trips/area', json=jsonLineStringGeo)
    return data.content

def getStopsByPath(geoJson):
    points_from_json = list(map(lambda point: (point['lat'],point['lng']),geoJson))
    lineStringGeo = ShapelyLineString(points_from_json)
    jsonLineStringGeo = json.dumps(mapping(lineStringGeo))
    data = requests.post('http://localhost:3001/stop/path', json=jsonLineStringGeo)
    return data.content


def addAnalytics(analytics):
    data = requests.post('http://localhost:3001/analytics', json=analytics)
    return data

def getAnalytics():
    data = requests.get('http://localhost:3001/analytics')
    return data