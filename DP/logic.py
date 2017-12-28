from flask import jsonify
import requests

server_ip = 'http://127.0.0.1:5000/compute'


def setDefaultHours():
    hours = {}
    for key in range(0, 23):
        hours[key] = 0
    return hours


def getTrips(geoJson):
    headers = {'Content-Type': 'application/json'}
    data = requests.get(server_ip, json=geoJson)
    return computeNumForBusStops(data)


def computeNumForBusStops(jsonObj):
    retval = []
    record = {}
    data = jsonObj.data
    for stop in data.stop:
        hours = setDefaultHours()
        for trip in data.stop_times:
            if (trip.stop_id == stop.stop_id):
                hours[trip.arrivale_time.hour] += 1
        record['stopName'] = stop.stop_name
        record['numberOfTrips']=hours
        retval.append(record)
    return jsonify(retval)

