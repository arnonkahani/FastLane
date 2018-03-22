from SharedLayer.objects.Trip import Trip
from SharedLayer.objects.Stop import Stop
from enum import Enum


class PickupType(Enum):
    PICKUP = 0
    DROPOFF = 1


class DropoffType(Enum):
    DROPOFF = 0
    PICKUP = 1


class StopTime:
    def __init__(self, arrival_time: str, departure_time: str, stop_sequence: int, dropoff_type: DropoffType,
                 pickup_type: PickupType, trip: Trip, dist_from_first_stop: float,
                 stop: Stop):
        self.trip = trip
        self.stop = stop
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stop_sequnace = stop_sequence
        self.pickup_type = pickup_type
        self.dropoff_type = dropoff_type
        self.dist_from_first_stop = dist_from_first_stop
