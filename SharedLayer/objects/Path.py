from SharedLayer.objects.PathPoint import PathPoint
from typing import List


class Path:
    def __init__(self, total_dist: float, path_points: List[PathPoint]):
        self.total_dist = total_dist
        self.path_points = path_points