import sys
sys.path.append('../')
from flask import Flask, redirect, url_for, request, jsonify , json
from DP.logic import getTrips , computeNumForBusStops , computeNumOfBusesForStation,getTripsPaths,computeTripsPath

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
    geoJson = request.get_json()
    data = getTrips(geoJson)
    print(data)
    return computeNumOfBusesForStation(data)

@app.route('/trips/path')
def trips_by_area():
    geoJson = request.get_json()
    data = getTripsPaths(geoJson)
    print(data)
    return computeTripsPath(data)


@app.route('/coordinates')
def coordinates():
    geoJson = request.json
    print (geoJson)
    data = getTrips(geoJson)
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002, debug=True,use_reloader=False)
