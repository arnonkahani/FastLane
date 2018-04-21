import json
from flask import Flask, request
from geoalchemy2 import functions
from sqlalchemy.orm import sessionmaker
from DB.gtfsdb import Base
from DB.gtfsdb.gtfs_db import GTFS_DB
from DB.queries import *

app = Flask(__name__)

headers = {'Content-Type': 'application/json'}
url = "z"
result = []


def construct_linestring(geoJSONCoordinates):
    linestring = ""
    for geo_point in geoJSONCoordinates:
        linestring += str(geo_point[1]) + " " + str(geo_point[0]) + ","
    linestring = linestring[0:-2]
    return 'LINESTRING(' + linestring + ')'


@app.route('/stops_times/square', methods=['POST'])
def stoptimes_info_by_area():
    sq_area = construct_linestring(request.get_json()['coordinates'])
    return get_stoptimes_info_by_area(session=session,line_string_2pt=sq_area)


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


if __name__ == '__main__':
    a = GTFS_DB()
    db = a.db
    Base.metadata.bind = db.engine
    DBSession = sessionmaker()
    session = DBSession()

    app.run(debug=True, host='0.0.0.0', port=3001)
