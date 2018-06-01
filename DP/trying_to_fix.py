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
from shapely.geometry import LineString as ShapelyLineString, Point,mapping
import requests
import numpy as np
import matplotlib.pyplot as plt






with open("testing_p.pkl", 'rb') as handle:
    stops = pickle.load(handle)
stop_loc_in_lin = {}
with open("testing_p.json", 'r') as handle:
    markers = json.load(handle)
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
mean = []

stops = list(filter(lambda stop: line.distance(Point(stop.location.xy[1][0],stop.location.xy[0][0])) < EPS,stops))

stop_locations = []
for stop in stops:
    stop_locations.append([stop.location.xy[0][0],stop.location.xy[1][0]])
print(len(stop_locations))



closeset_points = list(map(lambda stop: line.interpolate(line.project(Point(stop.location.xy[1][0],stop.location.xy[0][0]))), stops))




stop_locations_on_line = []
for p in closeset_points:
    stop_locations_on_line.append([p.xy[1][0],p.xy[0][0]])
print(len(stop_locations_on_line))

marked_path = []
old_line =list(zip(*line.coords.xy))
for x,y in old_line:
    marked_path.append([y,x])

stop_locations = np.array(stop_locations)
stop_locations_on_line = np.array(stop_locations_on_line)
marked_path = np.array(marked_path)


plt.scatter(stop_locations[:,0],stop_locations[:,1],color='red')
plt.scatter(stop_locations_on_line[:,0],stop_locations_on_line[:,1],color='blue')
plt.plot(marked_path[:,0],marked_path[:,1],color="green")
plt.show()

distances = []
for stop_idx, point in enumerate(stop_locations_on_line):
    shapely_point = Point(point)
    distances.append(ShapelyLineString(marked_path).distance(shapely_point))

print(np.max(distances))
counter = 0
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


plt.scatter(stop_locations[:,0],stop_locations[:,1],color='red')
plt.scatter(stop_locations_on_line[:,0],stop_locations_on_line[:,1],color='blue')
plt.plot(marked_line_with_stops[:,0],marked_line_with_stops[:,1],color="green")
plt.show()

final_lines = []
all_stop_loc = stop_loc_in_lin.items()
all_stop_loc = sorted(all_stop_loc, key=lambda x: x[1])
all_stop_loc = np.array(all_stop_loc)
plt.scatter(marked_line_with_stops[all_stop_loc[:,1]][:,0],marked_line_with_stops[all_stop_loc[:,1]][:,1],color='blue')
plt.plot(marked_line_with_stops[:,0],marked_line_with_stops[:,1],color="green")
plt.show()



sections = []
for idx, (station, station_idx) in enumerate(all_stop_loc):
    if idx == 0:
        points = marked_line_with_stops[0:station_idx + 1]
        sections.append(points)
    else:
        points = marked_line_with_stops[all_stop_loc[idx - 1][1]:station_idx + 1]
        sections.append(points)

colors = ['red','green','blue']
for idx,section in enumerate(sections):
    plt.plot(section[:, 0], section[:, 1], color=colors[idx%3])
plt.scatter(marked_line_with_stops[all_stop_loc[:,1]][:,0],marked_line_with_stops[all_stop_loc[:,1]][:,1],color='blue')
plt.show()
print(1)