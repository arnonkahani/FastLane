import pickle

from DB.gtfsdb.app import GTFS_DB
import os
from DB.gtfsdb import Stop, StopTime, Base, Calendar, Trip
from sqlalchemy.orm import sessionmaker, Query
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from geoalchemy2.elements import WKBElement
from geoalchemy2 import func, functions
from datetime import datetime
from flask import Flask, url_for, request, jsonify
from time import time
import sys
import geojson

app = Flask(__name__)

headers = {'Content-Type': 'application/json'}
url = "z"
result = []


def to_json(data):
    def extended_encoder(x):
        if isinstance(x, Base):
            return x.to_dict()
        if isinstance(x, WKBElement):
            return mapping(to_shape(x))
        if isinstance(x, datetime):
            return x.isoformat()

    return json.dumps(data, default=extended_encoder)


def construct_linestring(geoJSONCoordinates):
    linestring = ""
    for geo_point in geoJSONCoordinates:
        linestring += str(geo_point[1]) + " " + str(geo_point[0]) + ","
    linestring = linestring[0:-2]
    return 'LINESTRING(' + linestring + ')'


@app.route('/viz', methods=['POST'])
def dataVizdataViz():
    stop_line = construct_linestring(request.get_json()['coordinates'])
    # stop_line = construct_linestring(request.get_json()['coordinates'])
    print(stop_line)
    request.get_json()
    que = session.query(Stop) \
        .with_entities(Stop.stop_id,
                       Stop.stop_name,
                       Stop.geom,
                       StopTime.arrival_time,
                       StopTime.trip_id) \
        .filter(
        Stop.geom.intersects(stop_line)) \
        .join(StopTime, StopTime.stop_id == Stop.stop_id)

    # que2 = session.query(Calendar).with_entities(Calendar.service_id,Calendar.sunday,
    #                    Calendar.monday,
    #                    Calendar.tuesday,
    #                    Calendar.wednesday,
    #                    Calendar.thursday,
    #                    Calendar.friday,
    #                    Calendar.saturday,
    #                    Trip.trip_id)\
    #     .join(Trip, Trip.service_id == Calendar.service_id)



    def constructResponse(row, names):
        resp = {}
        for idx in range(len(names)):
            resp[names[idx]] = row[idx]
        return resp

    def convert_to_number(date):
        return int(date[:2]) % 24

    days = ["sunday","monday", "tuesday", "wednesday","thursday", "friday", "saturday"]
    # res_calender = [constructResponse(x, ["service_id","sunday", "monday", "tuesday", "wednesday","thursday", "friday", "saturday","trip_id"]) for x in que2]
    serives_2_dates = {}
    # for service_res in res_calender:
    #     serives_2_dates[service_res['trip_id']] = {}
    #     for day in days:
    #         serives_2_dates[service_res['trip_id']][day] = service_res[day]

    with open('gtfsdb/obj/' + "calander" + '.pkl', 'rb') as f:
        serives_2_dates = pickle.load(f)

    res = [constructResponse(x, ["stop_id", "stop_name", "geom", "arrival_time", "trip_id"]) for x in que]
    data_to_send = {}
    for trip in res:
        stop_id = trip["stop_id"]
        if not stop_id in data_to_send:
            data_to_send[stop_id] = {}
            data_to_send[stop_id]['stop_id'] = trip["stop_id"]
            data_to_send[stop_id]['stop_name'] = trip["stop_name"]
            data_to_send[stop_id]['geom'] = trip["geom"]
            data_to_send[stop_id]['rides'] = []
            for i in range(7):
                data_to_send[stop_id]['rides'].append([])
                for j in range(24):
                    data_to_send[stop_id]['rides'][i].append(0)

        for idx, day in enumerate(days):
            if serives_2_dates[trip['trip_id']][day]:
                data_to_send[stop_id]['rides'][idx][convert_to_number(trip['arrival_time'])] += 1
    print(que)
    data = {"data": {"stops": list(data_to_send.values())}}
    data_json = to_json(data)
    return data_json


@app.route('/stops', methods=['POST'])
def dataForFormulaComputation():
    stop_line = construct_linestring(json.loads(request.get_json())['coordinates'])
    # stop_line = construct_linestring(request.get_json()['coordinates'])
    print(stop_line)
    request.get_json()
    que = session.query(Stop) \
        .with_entities(Stop.stop_id,
                       Stop.stop_name,
                       Stop.geom,
                       StopTime.arrival_time) \
        .filter(
        Stop.geom.intersects(
            functions.ST_Buffer(stop_line,
                                0.000000000000063, 'endcap=flat join=round'))) \
        .join(StopTime, StopTime.stop_id == Stop.stop_id)

    def constructResponse(row, names):
        resp = {}
        for idx in range(len(names)):
            resp[names[idx]] = row[idx]
        return resp

    res = [constructResponse(x, ["stop_id", "stop_name", "geom", "arrival_time"]) for x in que]
    data_to_send = {}
    for trip in res:
        stop_id = trip["stop_id"]
        if not stop_id in data_to_send:
            data_to_send[stop_id] = {}
            data_to_send[stop_id]['stop_id'] = trip["stop_id"]
            data_to_send[stop_id]['stop_name'] = trip["stop_name"]
            data_to_send[stop_id]['geom'] = trip["geom"]
            data_to_send[stop_id]['arrival_time'] = []
        data_to_send[stop_id]['arrival_time'].append(trip['arrival_time'])
    print(que)
    data = {"data": {"stops": list(data_to_send.values())}}
    return to_json(data)


@app.route('/')
def getData():
    time_S = time()
    print("start: " + str(time_S))
    s = session.query(Stop).with_entities(Stop.stop_id).all()
    st = []
    time_S = time() - time_S
    print("end: " + str(time_S))
    s = [x for x in s]
    data = {"data": {"stops": s, "stops_times": st}}
    print(sys.getsizeof(data))

    def extended_encoder(x):
        if isinstance(x, Base):
            return x.to_dict()
        if isinstance(x, WKBElement):
            return mapping(to_shape(x))
        if isinstance(x, datetime):
            return x.isoformat()

    result = json.dumps(data, default=extended_encoder)
    return result


if __name__ == '__main__':
    a = GTFS_DB()
    a.load_data('file:///{0}'.format(
        os.path.join('/Users/arnon/Documents/SchoolProjects/FastLane/DB/MockData', 'israel-public-transportation.zip')))
    db = a.db
    Base.metadata.bind = db.engine
    DBSession = sessionmaker()
    session = DBSession()

    app.run(debug=True, host='0.0.0.0', port=3001)
