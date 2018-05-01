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
    data = requests.post('http://132.73.194.168:3001/stops_times/square', json=jsonLineStringGeo)
    return data.content


def computeNumOfBusesForStation(pickleObj):
    stopTimes = pickle.loads(pickleObj)
    days = 7
    hours = 24
    stopArr = []
    for stopTime in stopTimes:
        stop = stopTime.stop
        arrivalTime = stopTime.arrival_time
        stopResponse = {}
        exsistStop = list(filter(lambda currstop: currstop['stop_id'] == stop.id, stopArr))
        exists = False
        if not exsistStop:
            stopResponse['stop_id'] = stop.id
            stopResponse['stop_name'] = stop.name
            stopResponse['geom'] = shapely.geometry.mapping(shapely.geometry.Point(stop.location.x,stop.location.y))
            stopResponse['rides'] = [[0 for hour in range(hours)] for day in range(days)]
            stopArr.append(stopResponse)
        else:
            exists = True
            stopResponse = exsistStop[0]
        daysCounter = 0
        for day in stopTime.trip.calenders[0].days:
            if day:
                dt = datetime.strptime(arrivalTime, '%H:%M:%S')
                stopResponse['rides'][daysCounter][dt.hour] += 1
            daysCounter += 1
        if not exists:
            stopArr.append(stopResponse)
        else:
            stopArr = replaceStop(stopArr, stopResponse)
    return json.dumps({
        'data': {
            'stops': stopArr
        }
    })


def replaceStop(stopArr, stopResponse):
    return [stopResponse if stop['stop_id'] == stopResponse['stop_id'] else stop for stop in stopArr]


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