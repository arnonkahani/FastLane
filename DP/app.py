from flask import Flask, redirect, url_for, request, jsonify
from logic import getTrips

app = Flask(__name__)

headers = {'Content-Type': 'application/json'}
url = "z"


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
    geoJson = request.json
    print geoJson
    data = getTrips(geoJson)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
