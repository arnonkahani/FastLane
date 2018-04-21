
import json
from flask import Flask, request
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


@app.route('/stops_times/path', methods=['POST'])
def stoptimes_info_by_path():
    map_path = construct_linestring(json.loads(request.get_json())['coordinates'])
    return get_stoptimes_info_by_path(session=session, line_string=map_path)



if __name__ == '__main__':
    a = GTFS_DB()
    db = a.db
    Base.metadata.bind = db.engine
    DBSession = sessionmaker()
    session = DBSession()

    app.run(debug=True, host='0.0.0.0', port=3001)
