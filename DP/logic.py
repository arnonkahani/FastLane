import sys
sys.path.append('../')
from flask import json
from datetime import datetime
import shapely.geometry
import pickle
from shapely.geometry import LineString as ShapelyLineString, Point,mapping
import numpy as np
import random

headers = {'Content-Type': 'application/json'}

def setDefaultHours():
    hours = {}
    for key in range(0, 24):
        hours[key] = 0
    return hours




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
                try:
                    dt = datetime.strptime(arrivalTime, '%H:%M:%S')
                except:
                    continue
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


def computeTripsPath(pickleObj):
    trips = pickle.loads(pickleObj)
    tripsArr = []

    for trip in trips:
        tripResponse = {}
        tripResponse['trip_id'] = trip.id
        tripResponse['trip_headsign'] = trip.headsign
        tripResponse['path'] = shapely.geometry.mapping(trip.path.path_points)
        tripsArr.append(tripResponse)

    return json.dumps({
        'data': {
            'trips': tripsArr
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


def computeV(pickleObj,geoJson):
    stops = pickle.loads(pickleObj)
    stop_loc_in_lin = {}
    markers = geoJson[0]

    points_from_json = list(map(lambda point: (point['lat'], point['lng']), markers))
    line = ShapelyLineString(points_from_json)

    def pairs(lst):
        for i in range(1, len(lst)):
            yield lst[i - 1], lst[i], i

    def update_locs(new_loc):
        for key, value in stop_loc_in_lin.items():
            if value >= new_loc:
                stop_loc_in_lin[key] = value + 1

    EPS = 0.000362003592

    stops = list(filter(lambda stop: line.distance(Point(stop.location.xy[1][0], stop.location.xy[0][0])) < EPS, stops))

    stop_locations = []
    for stop in stops:
        stop_locations.append([stop.location.xy[0][0], stop.location.xy[1][0]])

    closeset_points = list(
        map(lambda stop: line.interpolate(line.project(Point(stop.location.xy[1][0], stop.location.xy[0][0]))), stops))

    stop_locations_on_line = []
    for p in closeset_points:
        stop_locations_on_line.append([p.xy[1][0], p.xy[0][0]])

    marked_path = []
    old_line = list(zip(*line.coords.xy))
    for x, y in old_line:
        marked_path.append([y, x])

    stop_locations_on_line = np.array(stop_locations_on_line)
    marked_path = np.array(marked_path)


    current_line = marked_path.tolist()
    for stop_idx, point in enumerate(stop_locations_on_line):
        new_line = []
        shapely_point = Point(point)
        for first, second, idx in pairs(current_line):
            if ShapelyLineString([first, second]).distance(shapely_point) < 2.2939795370745424e-14:
                new_line = current_line[0:idx]
                new_line.append(list(zip(*shapely_point.coords.xy))[0])
                new_line += current_line[idx:]
                update_locs(idx)
                stop_loc_in_lin[stop_idx] = idx
                break
        if new_line != []:
            current_line = new_line

    marked_line_with_stops = np.array(current_line)

    all_stop_loc = stop_loc_in_lin.items()
    all_stop_loc = sorted(all_stop_loc, key=lambda x: x[1])
    all_stop_loc = np.array(all_stop_loc)


    sections = []
    for idx, (station, station_idx) in enumerate(all_stop_loc):
        if idx == 0:
            points = marked_line_with_stops[0:station_idx + 1]
            sections.append(points)
        else:
            points = marked_line_with_stops[all_stop_loc[idx - 1][1]:station_idx + 1]
            sections.append(points)


    v = list(map(lambda v: random.randint(0,100),range(1,len(sections)+1)))
    stop_loc = list(map(lambda stop: mapping(Point(stop.xy[0][0],stop.xy[1][0])), closeset_points))

    sections = list(map(lambda section: section.tolist(),sections))
    return json.dumps({
        'data': {
            'v':v,
            'sections' : sections,
            'stops' : stop_locations
        }
    })

def process_analytics(data):
    users = pickle.loads(data)
    url_dict = {}
    for user in users:
        url_dict[user.user_id] = {}
        for analytic in user.analytics:
            url_dict[user.user_id][analytic.url] = {'clicks':{},'movement':{}}
        for analytic in user.analytics:
            analytic_json = json.loads(analytic.event)
            event_type = analytic_json['event_type']
            if not analytic_json["uuid"] in url_dict[user.user_id][analytic.url][event_type]:
                url_dict[user.user_id][analytic.url][event_type][analytic_json["uuid"]] = []
            url_dict[user.user_id][analytic.url][event_type][analytic_json["uuid"]].append(analytic)

        for url_key in url_dict[user.user_id].keys():
            user_movment_dict = url_dict[user.user_id][url_key]['movement']
            for uuid_key in user_movment_dict.keys():
                sorted_list = list(sorted(user_movment_dict[uuid_key],key=lambda x : x.timestamp))
                movement = []
                for captured_movment in sorted_list:
                    analytic_json = json.loads(captured_movment.event)
                    event_data = analytic_json['event_data']
                    movement += event_data
                    user_movment_dict[uuid_key] = movement

    return json.dumps(url_dict)


