from shapely.geometry import LineString,Point
import matplotlib.pyplot as plt
stop_loc_in_lin = {}

line = LineString([(0, 0), (0, 5), (5, 5)])
points = [Point(1, 4),Point(1, 2),Point(5, 4)]

# [(0.0, 0.0), (0.0, 2.0), (0.0, 4.0), (0.0, 5.0), (5.0, 5.0)]
# {0: 1, 1: 2, 2: 4}

def pairs(lst):
    for i in range(1, len(lst)):
        yield lst[i - 1], lst[i], i


def update_locs(new_loc):
    for key, value in stop_loc_in_lin.items():
        if value >= new_loc:
            stop_loc_in_lin[key] = value + 1


closeset_points = list(map(lambda stop: line.interpolate(line.project(stop)), points))
# for c_point in closeset_points:
#     print(c_point)
# print(list(map(lambda x: x.coords,closeset_points)))
old_line = list(zip(*line.coords.xy))
for stop_idx, point in enumerate(closeset_points):
    for first, second, idx in pairs(old_line):
        new_line = []
        if LineString([first, second]).contains(point):
            new_line = old_line[0:idx]
            new_line.append(list(zip(*point.coords.xy))[0])
            new_line += old_line[idx:]
            update_locs(idx)
            stop_loc_in_lin[stop_idx] = idx
            break
    if new_line == []:
        item_idx = old_line.index(list(zip(*point.coords.xy))[0])
        update_locs(item_idx)
        stop_loc_in_lin[stop_idx] = item_idx
    else:
        old_line = new_line
line = old_line

print(line)
print(stop_loc_in_lin)
final_lines = []

all_stop_loc = stop_loc_in_lin.items()
all_stop_loc = sorted(all_stop_loc , key=lambda x: x[1])
for idx,(station,station_idx) in enumerate(all_stop_loc):
    if idx == 0:
        points = line[0:station_idx+1]
        final_lines.append(points)
    else:
        points = line[all_stop_loc[idx-1][1]:station_idx+1]
        final_lines.append(points)

print(final_lines)