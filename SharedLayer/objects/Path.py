from shapely.geometry import LineString

from typing import List


class Path:
    def __init__(self, total_dist: float = None, path_line: LineString = None):
        self.total_dist = total_dist
        self.path_points = path_line
