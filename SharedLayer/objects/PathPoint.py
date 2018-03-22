from shapely.geometry import Point


class PathPoint:
    def __init__(self, point: Point, dist_from_begining: float):
        self.point = point
        self.dist_from_beginning = dist_from_begining
