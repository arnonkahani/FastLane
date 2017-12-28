from flask import jsonify,json
from datetime import datetime
import requests

server_ip = 'https://fastlanes-data-processing.herokuapp.com'

def setDefaultHours():
    hours = {}
    for key in range(0, 24):
        hours[key] = 0
    return hours


def getTrips(geoJson):
    headers = {'Content-Type': 'application/json'}
    data = requests.get(server_ip, json=geoJson)
    data = requests.get(server_ip)
    return computeNumForBusStops(data.content)


def computeNumForBusStops(jsonObj):
    retval = []
    record = {}
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
            pair['hour'] = key
            list.append(pair)
        record['numberOfTrips'] = list
        retval.append(record)
    jsonVal = json.dumps(retval[0])
    return jsonVal
