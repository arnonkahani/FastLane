import sys
sys.path.append('../')
from flask import json
from geojson import LineString
from shapely.geometry import LineString as ShapelyLineString, mapping
import requests

dev_server_ip = 'localhost:3001'
prod_server_ip = 'db:3001'

server_ip=dev_server_ip

# server_ip = 'localhost:3006'
headers = {'Content-Type': 'application/json'}

def setDefaultHours():
    hours = {}
    for key in range(0, 24):
        hours[key] = 0
    return hours


def getTrips(geoJson):
    lineStringGeo = LineString(geoJson)
    jsonLineStringGeo = json.dumps(lineStringGeo)
    data = requests.post('http://{server_ip}/stops_times/square'.format(server_ip=server_ip), json=jsonLineStringGeo)
    return data.content


def getTripsPaths(geoJson):
    lineStringGeo = LineString(geoJson)
    jsonLineStringGeo = json.dumps(lineStringGeo)
    data = requests.post('http://{server_ip}/trips/area'.format(server_ip=server_ip), json=jsonLineStringGeo)
    return data.content

def getStopsByPath(geoJson):
    points_from_json = list(map(lambda point: (point['lat'],point['lng']),geoJson))
    lineStringGeo = ShapelyLineString(points_from_json)
    jsonLineStringGeo = json.dumps(mapping(lineStringGeo))
    data = requests.post('http://{server_ip}/stop/path'.format(server_ip=server_ip), json=jsonLineStringGeo)
    return data.content


def addAnalytics(analytics):
    data = requests.post('http://{server_ip}/analytics'.format(server_ip=server_ip), json=analytics)
    return data

def getAnalytics():
    data = requests.get('http://{server_ip}/analytics'.format(server_ip=server_ip))
    return data.content