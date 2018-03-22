from flask import jsonify,json
from datetime import datetime
from geojson import LineString
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
    data = requests.post('http://132.73.193.102:5000/stops', json=jsonLineStringGeo)
    return data.content


def computeNumForBusStops2(jsonObj):
    retval = []
    dic = json.loads(jsonObj)
    data = dic['data']
    for stop in data['stops']:
        record = {}
        hours = setDefaultHours()
        for trip in data['stops_times']:
            if (trip['stop_id'] == stop['stop_id']):
                dt = datetime.strptime(trip['arrival_time'], '%H:%M:%S')
                hours[dt.hour] += 1
        record['stopName'] = stop['stop_name']
        list = []
        for key, value in hours.iteritems():
            pair = {}
            pair['numOfTripsPerHour'] = value
            pair['hour'] = "%02d:%02d" % (key, 0)
            list.append(pair)
        record['numberOfTrips'] = list
        geoPoint = stop['geom']
        record['lat'] = geoPoint['coordinates'][0]
        record['lng'] = geoPoint['coordinates'][1]
        retval.append(record)
    jsonVal = json.dumps(retval)
    return jsonVal


def computeNumForBusStops(jsonObj):
    retval = []
    dic = json.loads(jsonObj)
    data = dic['data']
    for stop in data['stops']:
        record = {}
        hours = setDefaultHours()
        for arrival_time in stop['arrival_time']:
            try:
                dt = datetime.strptime(arrival_time, '%H:%M:%S')
                hours[dt.hour] += 1
            except:
                print (arrival_time)
        record['stopName'] = stop['stop_name']
        list = []
        for key, value in hours.iteritems():
            pair = {}
            pair['numOfTripsPerHour'] = value
            pair['hour'] = "%02d:%02d" % (key, 0)
            list.append(pair)
        record['numberOfTrips'] = list
        geoPoint = stop['geom']
        record['lat'] = geoPoint['coordinates'][1]
        record['lng'] = geoPoint['coordinates'][0]
        retval.append(record)
    jsonVal = json.dumps(retval)
    return jsonVal