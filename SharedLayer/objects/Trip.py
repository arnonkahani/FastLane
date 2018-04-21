from enum import Enum
from typing import List
from SharedLayer.objects.Calender import Calender
from SharedLayer.objects.Path import Path


class Direction(Enum):
    TO = 0
    FROM = 1


class Trip:
    def __init__(self, id: str = None, headsign: str = None, direction: Direction = None,
                 calenders: List[Calender] = None, path: Path = None):
        self.id = id
        self.direction = direction
        self.headsign = headsign
        self.calenders = calenders
