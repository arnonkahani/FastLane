import inspect
import pickle
import sys

sys.path.append('../')
from flask import Flask, redirect, url_for, request, jsonify, json
from DP.logic import computeNumForBusStops, computeNumOfBusesForStation, computeTripsPath, computeV,process_analytics
from DP.data_access import getTrips, getTripsPaths, getStopsByPath,addAnalytics,getAnalytics
import os

demo_flag = False
app = Flask(__name__)

headers = {'Content-Type': 'application/json'}


@app.route('/compute/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))


@app.route('/compute')
def compute():
    frame = inspect.currentframe()

    function_name = inspect.getframeinfo(frame).function
    function_json = function_name + '.json'
    if not (demo_flag and os.path.isfile(function_json)):
        geoJson = request.get_json()
        data = getTrips(geoJson)
        print(data)
        res = computeNumOfBusesForStation(data)
        with open(function_json, 'w') as outfile:
            json.dump(res, outfile)
    else:
        with open(function_json, 'r') as handle:
            res = json.load(handle)
    print("end compute")
    return res


@app.route('/trips/path')
def trips_by_area():
    geoJson = request.get_json()
    data = getTripsPaths(geoJson)
    print(data)
    return computeTripsPath(data)


@app.route('/v/path')
def v_by_path():
    geoJson = request.get_json()
    markers = geoJson[0]
    data = getStopsByPath(markers)
    print(data)
    return computeV(data, geoJson)


@app.route('/coordinates')
def coordinates():
    geoJson = request.json
    print(geoJson)
    data = getTrips(geoJson)
    return jsonify(data)


@app.route('/analytics',methods=['POST'])
def add_analytics():
    analytics = request.json
    addAnalytics(analytics)
    return jsonify(analytics)

@app.route('/analytics',methods=['GET'])
def get_analytics():
    data = getAnalytics()
    processed_data = process_analytics(data)
    return processed_data



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002, debug=True, use_reloader=False)
