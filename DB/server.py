import sys
sys.path.append('../')

from sqlalchemy.orm import sessionmaker
from DB.db import Base
from DB.db.managers.db_manager import DBManager
import json
from flask import Flask, request
from DB.queries import *
import time
app = Flask(__name__)

headers = {'Content-Type': 'application/json'}
url = "z"
result = []



class Server:
    def __init__(self):
        print("inited server")
    def set_config(self,config):
        self.config = config
    def set_db_manger(self,db_manager = None):
        if db_manager == None:
            self.db_manager = DBManager(self.config)
        Base.metadata.bind = self.db_manager.db.engine
        DBSession = sessionmaker()
        self.session = DBSession()

server = Server()


def construct_linestring(geoJSONCoordinates):
    linestring = ""
    for geo_point in geoJSONCoordinates:
        linestring += str(geo_point[1]) + " " + str(geo_point[0]) + ","
    linestring = linestring[0:-2]
    return 'LINESTRING(' + linestring + ')'


@app.route('/stops_times/square', methods=['POST'])
def stoptimes_info_by_area():
    sq_area = construct_linestring(json.loads(request.get_json())['coordinates'])
    res = get_stoptimes_info_by_area(session=server.session,line_string_2pt=sq_area)
    return res

@app.route('/stops_times/path', methods=['POST'])
def stoptimes_info_by_path():
    map_path = construct_linestring(json.loads(request.get_json())['coordinates'])
    return get_stoptimes_info_by_path(session=server.session, line_string_path=map_path)

@app.route('/trips/area', methods=['POST'])
def trip_info_by_area():
    sq_area = construct_linestring(json.loads(request.get_json())['coordinates'])
    return get_trips_info_by_area(session=server.session, line_string_2pt=sq_area)
@app.route('/stop/path', methods=['POST'])
def v_info_by_path():
    map_path = construct_linestring(json.loads(request.get_json())['coordinates'])
    return get_v_info_by_path(session=server.session, line_string_path=map_path)

@app.route('/analytics', methods=['POST'])
def add_analytics():
    return add_user_data(session=server.session, user_data=request.get_json())

@app.route('/analytics', methods=['GET'])
def get_analytics():
    return get_all_analytics(server.session)

def start_server(config,db_managar=None):
    server.set_config(config)
    server.set_db_manger(db_managar)
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=3001,threaded=True)