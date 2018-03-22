from enum import Enum
from typing import List
from SharedLayer.objects.Trip import Trip


class RouteColor(Enum):
    SEA_LINE = '#3399FF'
    STUDENT_LINE = '#FF9933'
    REGULAR_LINE = ''
    TRAIN_LINE = '#33CC33'
    NIGHT_LINE = '#9933FF'
    CALL_LINE = '#8B4513'


class RouteType(Enum):
    BUS = 3
    TRAIN = 2
    LIGHT_TRAIN = 0


class Route:
    def __init__(self, id: str, short_name: str, long_name: str, description: str, color: RouteColor,
                 trips: List[Trip], route_type: RouteType):
        self.id = id
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.color = color
        self.trips = trips
        self.route_type = route_type
