from enum import Enum
from typing import List
from SharedLayer.objects.Calender import Calender
from shapely.geometry import LineString

class Direction(Enum):
    TO = 0
    FROM = 1


class Trip:
    def __init__(self, id: str, headsign: str, direction: Direction,
                 calenders: List[Calender], path: LineString):
        self.id = id
        self.direction = direction
        self.headsign = headsign
        self.calenders = calenders
        self.path = path
